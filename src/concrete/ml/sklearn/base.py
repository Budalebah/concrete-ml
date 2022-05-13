"""Module that contains base classes for our libraries estimators."""

# Disable pylint invalid name since scikit learn uses "X" as variable name for data
# pylint: disable=invalid-name

import copy

# Disable pylint to import hummingbird while ignoring the warnings
# pylint: disable=invalid-name,wrong-import-position,wrong-import-order,too-many-instance-attributes
import warnings
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy
import onnx
import sklearn
import torch
from concrete.numpy.compilation.artifacts import DebugArtifacts
from concrete.numpy.compilation.compiler import Compiler
from concrete.numpy.compilation.configuration import Configuration
from concrete.numpy.dtypes.integer import Integer

from ..common.debugging.custom_assert import assert_true
from ..common.utils import generate_proxy_function
from ..onnx.onnx_model_manipulations import simplify_onnx_model
from ..quantization import PostTrainingAffineQuantization, QuantizedArray
from ..torch import NumpyModule
from .tree_to_numpy import tree_to_numpy

# pylint: disable=wrong-import-position,wrong-import-order

# Silence hummingbird warnings
warnings.filterwarnings("ignore")
from hummingbird.ml import convert as hb_convert  # noqa: E402

# pylint: enable=wrong-import-position,wrong-import-order


class QuantizedTorchEstimatorMixin:
    """Mixin that provides quantization for a torch module and follows the Estimator API.

    This class should be mixed in with another that provides the full Estimator API. This class
    only provides modifiers for .fit() (with quantization) and .predict() (optionally in FHE)
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # The quantized module variable appends "_" so that it is not registered as a sklearn
        # parameter. Only training parameters should register, to enable easy cloning of un-trained
        # estimator
        self.quantized_module_ = None

    @property
    @abstractmethod
    def base_estimator_type(self):
        """Get the sklearn estimator that should be trained by the child class."""

    def get_params_for_benchmark(self):
        """Get the parameters to instantiate the sklearn estimator trained by the child class.

        Returns:
            params (dict): dictionary with parameters that will initialize a new Estimator
        """
        return self.get_params()

    @property
    @abstractmethod
    def base_module_to_compile(self):
        """Get the Torch module that should be compiled to FHE."""

    @property
    @abstractmethod
    def n_bits_quant(self):
        """Get the number of quantization bits."""

    def compile(
        self,
        X: numpy.ndarray,
        configuration: Optional[Configuration] = None,
        compilation_artifacts: Optional[DebugArtifacts] = None,
        show_mlir: bool = False,
        use_virtual_lib: bool = False,
    ):
        """Compile the model.

        Args:
            X (numpy.ndarray): the unquantized dataset
            configuration (Optional[Configuration]): the options for
                compilation
            compilation_artifacts (Optional[DebugArtifacts]): artifacts object to fill
                during compilation
            show_mlir (bool): whether or not to show MLIR during the compilation
            use_virtual_lib (bool): whether to compile using the virtual library that allows higher
                bitwidths

        Raises:
            ValueError: if called before the model is trained
        """
        if self.quantized_module_ is None:
            raise ValueError(
                "The classifier needs to be calibrated before compilation,"
                " please call .fit() first!"
            )

        # Quantize the compilation input set using the quantization parameters computed in .fit()
        quantized_numpy_inputset = copy.deepcopy(self.quantized_module_.q_inputs[0])
        quantized_numpy_inputset.update_values(X)

        # Call the compilation backend to produce the FHE inference circuit
        self.quantized_module_.compile(
            quantized_numpy_inputset,
            configuration=configuration,
            compilation_artifacts=compilation_artifacts,
            show_mlir=show_mlir,
            use_virtual_lib=use_virtual_lib,
        )

    def fit(self, X, y, **fit_params):
        """Initialize and fit the module.

        If the module was already initialized, by calling fit, the
        module will be re-initialized (unless ``warm_start`` is True). In addition to the
        torch training step, this method performs quantization of the trained torch model.

        Args:
            X : training data, compatible with skorch.dataset.Dataset
                By default, you should be able to pass:
                * numpy arrays
                * torch tensors
                * pandas DataFrame or Series
                * scipy sparse CSR matrices
                * a dictionary of the former three
                * a list/tuple of the former three
                * a Dataset
                If this doesn't work with your data, you have to pass a
                ``Dataset`` that can deal with the data.
            y (numpy.ndarray): labels associated with training data
            **fit_params: additional parameters that can be used during training, these are passed
                to the torch training interface

        Returns:
            self: the trained quantized estimator
        """
        # Reset the quantized module since quantization is lost during refit
        # This will make the .infer() function call into the Torch nn.Module
        # Instead of the quantized module
        self.quantized_module_ = None

        # Call skorch fit that will train the network
        super().fit(X, y, **fit_params)

        # Create corresponding numpy model
        numpy_model = NumpyModule(self.base_module_to_compile, torch.tensor(X[0, ::]))

        # Get the number of bits used in model creation (used to setup pruning)
        n_bits = self.n_bits_quant

        # Quantize with post-training static method, to have a model with integer weights
        post_training_quant = PostTrainingAffineQuantization(n_bits, numpy_model, is_signed=True)
        self.quantized_module_ = post_training_quant.quantize_module(X)
        return self

    # Disable pylint here because we add an additional argument to .predict,
    # with respect to the base class .predict method.
    # pylint: disable=arguments-differ
    def predict(self, X, execute_in_fhe=False):
        """Predict on user provided data.

        Predicts using the quantized clear or FHE classifier

        Args:
            X : input data, a numpy array of raw values (non quantized)
            execute_in_fhe : whether to execute the inference in FHE or in the clear

        Returns:
            y_pred : numpy ndarray with predictions

        """

        # By default, just return the result of predict_proba
        # which for linear models with no non-linearity applied simply returns
        # the decision function value
        return self.predict_proba(X, execute_in_fhe=execute_in_fhe)

    def predict_proba(self, X, execute_in_fhe=False):
        """Predict on user provided data, returning probabilities.

        Predicts using the quantized clear or FHE classifier

        Args:
            X : input data, a numpy array of raw values (non quantized)
            execute_in_fhe : whether to execute the inference in FHE or in the clear

        Returns:
            y_pred : numpy ndarray with probabilities (if applicable)

        Raises:
            ValueError: if the estimator was not yet trained or compiled
        """

        if execute_in_fhe:
            if self.quantized_module_ is None:
                raise ValueError(
                    "The classifier needs to be calibrated before compilation,"
                    " please call .fit() first!"
                )
            if not self.quantized_module_.is_compiled:
                raise ValueError(
                    "The classifier is not yet compiled to FHE, please call .compile() first"
                )

            # Run over each element of X individually and aggregate predictions in a vector
            if X.ndim == 1:
                X = X.reshape((1, -1))
            y_pred = None
            for idx, x in enumerate(X):
                q_x = self.quantized_module_.quantize_input(x).reshape(1, -1)
                q_pred = self.quantized_module_.forward_fhe.encrypt_run_decrypt(q_x)
                if y_pred is None:
                    assert_true(
                        isinstance(q_pred, numpy.ndarray),
                        f"bad type {q_pred}, expected np.ndarray",
                    )
                    # pylint is lost: Instance of 'tuple' has no 'size' member (no-member)
                    # because it doesn't understand the Union in encrypt_run_decrypt
                    # pylint: disable=no-member
                    y_pred = numpy.zeros((X.shape[0], q_pred.size), numpy.float32)
                    # pylint: enable=no-member
                y_pred[idx, :] = self.quantized_module_.dequantize_output(q_pred)

            nonlin = self._get_predict_nonlinearity()
            y_pred = nonlin(torch.from_numpy(y_pred)).numpy()

            return y_pred

        # For prediction in the clear we call the super class which, in turn,
        # will end up calling .infer of this class
        return super().predict_proba(X)

    # pylint: enable=arguments-differ

    def fit_benchmark(self, X, y):
        """Fit the quantized estimator and return reference estimator.

        This function returns both the quantized estimator (itself),
        but also a wrapper around the non-quantized trained NN. This is useful in order
        to compare performance between the quantized and fp32 versions of the classifier

        Args:
            X : training data, compatible with skorch.dataset.Dataset
                By default, you should be able to pass:
                * numpy arrays
                * torch tensors
                * pandas DataFrame or Series
                * scipy sparse CSR matrices
                * a dictionary of the former three
                * a list/tuple of the former three
                * a Dataset
                If this doesn't work with your data, you have to pass a
                ``Dataset`` that can deal with the data.
            y (numpy.ndarray): labels associated with training data

        Returns:
            self: the trained quantized estimator
            fp32_model: trained raw (fp32) wrapped NN estimator
        """

        self.fit(X, y)

        # Create a skorch estimator with the same training parameters as this one
        # Follow sklearn.base.clone: copy.deepcopy parameters obtained with get_params()
        # and pass them to the constructor

        # sklearn docs: "Clone does a deep copy of the model in an estimator without actually
        # copying  attached data. It returns a new estimator with the same parameters
        # that has not been fitted on any data."
        # see: https://scikit-learn.org/stable/modules/generated/sklearn.base.clone.html
        new_object_params = self.get_params_for_benchmark()

        for name, param in new_object_params.items():
            new_object_params[name] = copy.deepcopy(param)

        klass = self.base_estimator_type
        module_copy = copy.deepcopy(self.base_module_to_compile)

        # Construct with the fp32 network already trained for this quantized estimator
        # Need to remove the `module` parameter as we pass the trained instance here
        # This key is only present for NeuralNetClassifiers that don't fix the module type
        # Else this key may be removed already, e.g. by the FixedTypeSkorchNeuralNet
        if "module" in new_object_params:
            new_object_params.pop("module")
        fp32_model = klass(module_copy, **new_object_params)

        # Don't fit the new estimator, it is already trained. We just need to call initialize() to
        # signal to the skorch estimator that it is already trained
        fp32_model.initialize()

        return self, fp32_model


class BaseTreeEstimatorMixin(sklearn.base.BaseEstimator):
    """Mixin class for tree-based estimators.

    This class is used to add functionality to tree-based estimators, such as
    the tree-based classifier.
    """

    q_x_byfeatures: List[QuantizedArray]
    n_bits: int
    q_y: QuantizedArray
    init_args: Dict[str, Any]
    random_state: Optional[Union[numpy.random.RandomState, int]]  # pylint: disable=no-member
    sklearn_alg: Any
    sklearn_model: Any
    _tensor_tree_predict: Optional[Callable]
    framework: str
    class_mapping_: Optional[dict] = None
    classes_: str
    n_classes_: int

    def __init__(self, n_bits: int):
        """Initialize the TreeBasedEstimatorMixin.

        Args:
            n_bits (int): number of bits used for quantization
        """
        self.n_bits = n_bits
        self.q_x_byfeatures = []
        self.n_bits = n_bits
        self.fhe_tree = None
        self._onnx_model = None

    def quantize_input(self, X: numpy.ndarray):
        """Quantize the input.

        Args:
            X (numpy.ndarray): the input

        Returns:
            the quantized input
        """
        qX = numpy.zeros_like(X)
        # Quantize using the learned quantization parameters for each feature
        for i, q_x_ in enumerate(self.q_x_byfeatures):
            qX[:, i] = q_x_.update_values(X[:, i])
        return qX.astype(numpy.int32)

    def fit(self, X: numpy.ndarray, y: numpy.ndarray, **kwargs) -> Any:
        """Fit the tree-based estimator.

        Args:
            X (numpy.ndarray): The input data.
            y (numpy.ndarray): The target data.
            **kwargs: args for super().fit

        Returns:
            Any: The fitted model.
        """
        # mypy
        assert self.n_bits is not None

        qX = numpy.zeros_like(X)
        self.q_x_byfeatures = []

        self.n_classes_ = len(numpy.unique(y))

        # If classes are not starting from 0 and/or increasing by 1
        # we need to map them to values 0, 1, ..., n_classes - 1
        self.classes_ = numpy.unique(y)
        if not numpy.array_equal(numpy.arange(len(self.classes_)), self.classes_):
            self.class_mapping_ = dict(enumerate(self.classes_))

        # Register the number of classes
        self.n_classes_ = len(self.classes_)

        # Quantization of each feature in X
        for i in range(X.shape[1]):
            q_x_ = QuantizedArray(n_bits=self.n_bits, values=X[:, i])
            self.q_x_byfeatures.append(q_x_)
            qX[:, i] = q_x_.qvalues.astype(numpy.int32)

        # Initialize the sklearn model
        params = self.get_params()
        params.pop("n_bits", None)

        self.sklearn_model = self.sklearn_alg(**params)

        self.sklearn_model.fit(qX, y, **kwargs)

        # Tree ensemble inference to numpy
        self._tensor_tree_predict, self.q_y, self._onnx_model = tree_to_numpy(
            self.sklearn_model,
            qX,
            framework=self.framework,
            output_n_bits=self.n_bits,
        )
        return self

    def predict(self, X: numpy.ndarray, execute_in_fhe: bool = False) -> numpy.ndarray:
        """Predict the target values.

        Args:
            X (numpy.ndarray): The input data.
            execute_in_fhe (bool): Whether to execute in FHE. Defaults to False.

        Returns:
            numpy.ndarray: The predicted target values.
        """
        y_preds = self.predict_proba(X, execute_in_fhe=execute_in_fhe)
        y_preds = numpy.argmax(y_preds, axis=1)
        if self.class_mapping_ is not None:
            y_preds = numpy.array([self.class_mapping_[y_pred] for y_pred in y_preds])
        return y_preds

    def predict_proba(self, X: numpy.ndarray, execute_in_fhe: bool = False) -> numpy.ndarray:
        """Predict the probabilities.

        Args:
            X (numpy.ndarray): The input data.
            execute_in_fhe (bool): Whether to execute in FHE. Defaults to False.

        Returns:
            numpy.ndarray: The predicted probabilities.
        """
        # mypy
        assert self._tensor_tree_predict is not None
        qX = self.quantize_input(X)
        if execute_in_fhe:
            y_preds = self._execute_in_fhe(qX)
        else:
            y_preds = self._tensor_tree_predict(qX)[0]
        y_preds = self.post_processing(y_preds)
        return y_preds

    def post_processing(self, y_preds: numpy.ndarray) -> numpy.ndarray:
        """Apply post-processing to the predictions.

        Args:
            y_preds (numpy.ndarray): The predictions.

        Returns:
            numpy.ndarray: The post-processed predictions.
        """
        # mypy
        assert self.q_y is not None
        y_preds = self.q_y.update_quantized_values(y_preds)
        # Sum all tree outputs.
        y_preds = numpy.sum(y_preds, axis=0)
        assert_true(y_preds.ndim == 2, "y_preds should be a 2D array")
        # FIXME transpose workaround see #292
        y_preds = numpy.transpose(y_preds)
        return y_preds

    def fit_benchmark(
        self,
        X: numpy.ndarray,
        y: numpy.ndarray,
        *args,
        random_state: Optional[int] = None,
        **kwargs,
    ) -> Tuple[Any, Any]:
        """Fit the sklearn tree-based model and the FHE tree-based model.

        Args:
            X (numpy.ndarray): The input data.
            y (numpy.ndarray): The target data.
            random_state (Optional[Union[int, numpy.random.RandomState, None]]):
                The random state. Defaults to None.
            *args: args for super().fit
            **kwargs: kwargs for super().fit

        Returns:
            Tuple[ConcreteEstimators, SklearnEstimators]:
                                                The FHE and sklearn tree-based models.
        """

        params = self.get_params()  # type: ignore
        params.pop("n_bits", None)

        # Make sure the random_state is set or both algorithms will diverge
        # due to randomness in the training.
        if random_state is not None:
            params["random_state"] = random_state
        elif self.random_state is not None:
            params["random_state"] = self.random_state
        else:
            params["random_state"] = numpy.random.randint(0, 2**15)

        # Train the sklearn model without X quantized
        sklearn_model = self.sklearn_alg(**params)
        sklearn_model.fit(X, y, *args, **kwargs)

        # Train the FHE model
        self.__init__(n_bits=self.n_bits, **params)  # type: ignore
        self.fit(X, y, *args, **kwargs)
        return self, sklearn_model

    def _execute_in_fhe(self, qX: numpy.ndarray) -> numpy.ndarray:
        """Execute the FHE inference on the input data.

        Args:
            qX (numpy.ndarray): the input data quantized

        Returns:
            numpy.ndarray: the prediction as ordinals
        """
        # Check that self.fhe_tree is not None
        # mypy
        assert self.fhe_tree is not None, (
            f"You must call {self.compile.__name__} "
            f"before calling {self.predict.__name__} with execute_in_fhe=True."
        )
        # mypy
        assert self.fhe_tree is not None

        y_preds = []
        for qX_i in qX:
            # expected x shape is (n_features, n_samples)
            fhe_pred = self.fhe_tree.encrypt_run_decrypt(
                qX_i.astype(numpy.uint8).reshape(1, qX_i.shape[0])
            )
            y_preds.append(fhe_pred)
        y_preds_array = numpy.concatenate(y_preds, axis=-1)

        return y_preds_array

    def compile(
        self,
        X: numpy.ndarray,
        configuration: Optional[Configuration] = None,
        compilation_artifacts: Optional[DebugArtifacts] = None,
        show_mlir: bool = False,
        use_virtual_lib: bool = False,
    ):
        """Compile the model.

        Args:
            X (numpy.ndarray): the unquantized dataset
            configuration (Optional[Configuration]): the options for
                compilation
            compilation_artifacts (Optional[DebugArtifacts]): artifacts object to fill
                during compilation
            show_mlir (bool): whether or not to show MLIR during the compilation
            use_virtual_lib (bool): set to True to use the so called virtual lib
                simulating FHE computation. Defaults to False.
        """
        # Make sure that self.tree_predict is not None
        assert_true(
            self._tensor_tree_predict is not None, "You must fit the model before compiling it."
        )

        # mypy bug fix
        assert self._tensor_tree_predict is not None
        _tensor_tree_predict_proxy, parameters_mapping = generate_proxy_function(
            self._tensor_tree_predict, ["inputs"]
        )

        X = self.quantize_input(X)
        compiler = Compiler(
            _tensor_tree_predict_proxy,
            {parameters_mapping["inputs"]: "encrypted"},
        )
        self.fhe_tree = compiler.compile(
            (sample.reshape(1, sample.shape[0]) for sample in X),
            configuration=configuration,
            artifacts=compilation_artifacts,
            show_mlir=show_mlir,
            virtual=use_virtual_lib,
        )
        # mypy
        assert self.fhe_tree is not None
        output_graph = self.fhe_tree.graph.ordered_outputs()
        assert_true(
            len(output_graph) == 1,
            "graph has too many outputs",
        )
        assert_true(
            isinstance(dtype_output := output_graph[0].output.dtype, Integer),
            f"output is {dtype_output} but an Integer is expected.",
        )

    def get_onnx(self):
        """Return ONNX model.

        Returns:
            ONNX model
        """
        return self._onnx_model


# pytlint: disable=invalid-name,too-many-instance-attributes
class SklearnLinearModelMixin(sklearn.base.BaseEstimator):
    """A Mixin class for sklearn linear models with FHE."""

    sklearn_alg: Callable

    def __init__(self, *args, n_bits: Union[int, Dict] = 2, **kwargs):
        """Initialize the FHE linear model.

        Args:
            n_bits (int, Dict): Number of bits to quantize the model. If an int is passed for
                n_bits, the value will be used for activation, inputs and weights. If a dict is
                passed, then it should contain "inputs", "weights" and "outputs" keys with
                corresponding number of quantization bits for:
                - inputs : any input data to any layers
                - weights: learned parameters or constants in the network
                - outputs: final model output
                Default to 2.
            *args: The arguments to pass to the sklearn linear model.
            **kwargs: The keyword arguments to pass to the sklearn linear model.
        """
        super().__init__(*args, **kwargs)
        self.n_bits = n_bits

    def fit(self, X: numpy.ndarray, y: numpy.ndarray, *args, **kwargs) -> None:
        """Fit the FHE linear model.

        Args:
            X (numpy.ndarray): The input data.
            y (numpy.ndarray): The target data.
            *args: The arguments to pass to the sklearn linear model.
            **kwargs: The keyword arguments to pass to the sklearn linear model.
        """
        # Copy X
        X = copy.deepcopy(X)

        # Train

        # Initialize the model
        params = self.get_params()  # type: ignore
        params.pop("n_bits", None)
        self.sklearn_model = self.sklearn_alg(**params)

        # Fit the sklearn model
        self.sklearn_model.fit(X, y, *args, **kwargs)

        # Convert to onnx
        onnx_model = hb_convert(self.sklearn_model, backend="onnx", test_input=X).model

        # Remove Cast nodes
        onnx_model = self.clean_graph(onnx_model)

        # Create NumpyModule from onnx model
        numpy_module = NumpyModule(onnx_model)
        self._onnx_model = onnx_model

        # Apply post-training quantization
        post_training = PostTrainingAffineQuantization(
            n_bits=self.n_bits, numpy_model=numpy_module, is_signed=True
        )

        # Calibrate and create quantize module
        self.quantized_module = post_training.quantize_module(X)

    # clean_graph is used by inheritance and the calling self is needed.
    # pylint does not see it and complains that clean_graph should use @staticmethod
    # thus we need to ignore the warning.
    # pylint: disable=no-self-use

    def clean_graph(self, onnx_model: onnx.ModelProto):
        """Clean the graph of the onnx model.

        This will remove the Cast node in the onnx.graph since they
        have no use in the quantized/FHE model.

        Args:
            onnx_model (onnx.ModelProto): the onnx model

        Returns:
            onnx.ModelProto: the cleaned onnx model
        """
        op_type_to_remove = {"Cast", "Softmax", "ArgMax"}

        # Remove the input and output nodes
        for node_index, node in enumerate(onnx_model.graph.node):
            if node.op_type in op_type_to_remove:
                if node.op_type == "Cast":
                    assert_true(len(node.attribute) == 1, "Cast node has more than one attribute")
                    node_attribute = node.attribute[0]
                    assert_true(
                        (node_attribute.name == "to") & (node_attribute.i == onnx.TensorProto.FLOAT)
                    )
                new_node = onnx.helper.make_node(
                    "Identity",
                    inputs=[str(node.input[0])],
                    outputs=node.output,
                )
                # Update current node with new_node
                onnx_model.graph.node[node_index].CopyFrom(new_node)

        simplify_onnx_model(onnx_model)
        return onnx_model

    # pylint: enable=no-self-use

    def fit_benchmark(
        self, X: numpy.ndarray, y: numpy.ndarray, *args, **kwargs
    ) -> Tuple["SklearnLinearModelMixin", sklearn.linear_model.LinearRegression]:
        """Fit the sklearn linear model and the FHE linear model.

        Args:
            X (numpy.ndarray): The input data.
            y (numpy.ndarray): The target data.
            *args: The arguments to pass to the sklearn linear model.
            **kwargs: The keyword arguments to pass to the sklearn linear model.

        Returns:
            Tuple[SklearnLinearModelMixin, sklearn.linear_model.LinearRegression]:
                The FHE and sklearn LinearRegression.
        """
        # Train the sklearn model without X quantized
        sklearn_model = self.sklearn_alg(*args, **kwargs)
        sklearn_model.fit(X, y, *args, **kwargs)

        # Train the FHE model
        SklearnLinearModelMixin.fit(self, X, y, *args, **kwargs)
        return self, sklearn_model

    def predict(self, X: numpy.ndarray, execute_in_fhe: bool = False) -> numpy.ndarray:
        """Predict on user data.

        Predict on user data using either the quantized clear model,
        implemented with tensors, or, if execute_in_fhe is set, using the compiled FHE circuit

        Args:
            X (numpy.ndarray): the input data
            execute_in_fhe (bool): whether to execute the inference in FHE

        Returns:
            numpy.ndarray: the prediction as ordinals
        """
        # Quantize the input
        qX = self.quantized_module.quantize_input(X)

        # mypy
        assert isinstance(qX, numpy.ndarray)

        if execute_in_fhe:

            # Make sure the model is compiled
            assert_true(
                self.quantized_module.is_compiled,
                "The model is not compiled. Please run compile(...) first.",
            )

            # mypy
            assert self.quantized_module.forward_fhe is not None
            # mypy does not see the self.coef_ from sklearn.linear_model.LinearRegression.
            # Need to ignore with mypy warning.
            n_targets = (
                1 if self.sklearn_model.coef_.ndim == 1 else self.sklearn_model.coef_.shape[0]
            )
            y_preds = numpy.zeros(shape=(X.shape[0], n_targets))
            # Execute the compiled FHE circuit
            # Create a numpy array with the expected shape: (n_samples, n_classes)
            for i, qX_i in enumerate(qX):
                fhe_pred = self.quantized_module.forward_fhe.encrypt_run_decrypt(
                    qX_i.astype(numpy.uint8).reshape(1, qX_i.shape[0])
                )
                y_preds[i, :] = fhe_pred[0]
            # Convert to numpy array
            y_preds = self.quantized_module.dequantize_output(y_preds)
        else:
            y_preds = self.quantized_module.forward_and_dequant(qX)
        return y_preds

    def compile(
        self,
        X: numpy.ndarray,
        configuration: Optional[Configuration] = None,
        compilation_artifacts: Optional[DebugArtifacts] = None,
        show_mlir: bool = False,
        use_virtual_lib: bool = False,
    ) -> None:
        """Compile the FHE linear model.

        Args:
            X (numpy.ndarray): The input data.
            configuration (Optional[Configuration]): Configuration object
                to use during compilation
            compilation_artifacts (Optional[DebugArtifacts]): Artifacts object to fill during
                compilation
            show_mlir (bool): if set, the MLIR produced by the converter and which is
                going to be sent to the compiler backend is shown on the screen, e.g., for debugging
                or demo. Defaults to False.
            use_virtual_lib (bool): whether to compile using the virtual library that allows higher
                bitwidths with simulated FHE computation. Defaults to False
        """
        # Quantize the input
        quantized_numpy_inputset = copy.deepcopy(self.quantized_module.q_inputs[0])
        quantized_numpy_inputset.update_values(X)

        # Compile the model
        self.quantized_module.compile(
            quantized_numpy_inputset,
            configuration,
            compilation_artifacts,
            show_mlir=show_mlir,
            use_virtual_lib=use_virtual_lib,
        )

    def get_onnx(self):
        """Return ONNX model.

        Returns:
            ONNX model
        """
        return self._onnx_model
