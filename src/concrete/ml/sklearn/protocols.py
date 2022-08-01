"""Protocols.

Protocols are used to mix type hinting with duck-typing.
Indeed we don't always want to have an abstract parent class between all objects.
We are more interested in the behaviour of such objects.
Implementing a Protocol is a way to specify the behaviour of objects.

To read more about Protocol please read: https://peps.python.org/pep-0544
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

import numpy
import onnx
import sklearn
from concrete.numpy.compilation.artifacts import DebugArtifacts
from concrete.numpy.compilation.circuit import Circuit
from concrete.numpy.compilation.configuration import Configuration

# Disable pylint invalid name since scikit learn uses "X" as variable name for data
# pylint: disable=invalid-name


class Quantizer(Protocol):
    """Quantizer Protocol.

    To use to type hint a quantizer.
    """

    def quant(self, values: numpy.ndarray) -> numpy.ndarray:
        """Quantize some values.

        Args:
            values (numpy.ndarray): Values to quantize

        Returns: # noqa: DAR202
            numpy.ndarray: The quantized values
        """

    def dequant(self, X: numpy.ndarray) -> numpy.ndarray:
        """De-Quantize some values.

        Args:
            X (numpy.ndarray): Values to unquantize

        Returns: # noqa: DAR202
            numpy.ndarray: Unquantized values
        """


# Base typing object to describe a basic Estimator
class ConcreteBaseEstimatorProtocol(Protocol):
    """A Concrete Estimator Protocol."""

    n_bits: int
    fhe_circuit: Optional[Circuit]
    input_quantizers: List[Quantizer]
    output_quantizer: List[Quantizer]
    _onnx_model_: onnx.ModelProto
    post_processing_params: Dict[str, Any]
    base_estimator_type: Callable
    sklearn_alg: Callable[..., sklearn.base.BaseEstimator]
    sklearn_model: sklearn.base.BaseEstimator

    @property
    def quantize_input(self) -> Callable:
        """Quantize input function."""

    @property
    def onnx_model(self) -> onnx.ModelProto:
        """onnx_model.

        Results: # noqa: DAR202
            onnx.ModelProto
        """

    def post_processing(self, y_preds: numpy.ndarray) -> numpy.ndarray:
        """Post-process models predictions.

        Args:
            y_preds (numpy.ndarray): predicted values by model (clear-quantized)

        Returns: # noqa: DAR202
            numpy.ndarray: the post-processed predictions
        """

    def compile(
        self,
        X: numpy.ndarray,
        configuration: Optional[Configuration],
        compilation_artifacts: Optional[DebugArtifacts],
        show_mlir: bool,
        use_virtual_lib: bool,
        p_error: float,
    ) -> Circuit:
        """Compiles a model to a FHE Circuit.

        Args:
            X (numpy.ndarray): the unquantized dataset
            configuration (Optional[Configuration]): the options for
                compilation
            compilation_artifacts (Optional[DebugArtifacts]): artifacts object to fill
                during compilation
            show_mlir (bool): whether or not to show MLIR during the compilation
            use_virtual_lib (bool): whether to compile using the virtual library that allows higher
                bitwidths
            p_error (float): probability of error of a PBS


        Returns: # noqa: DAR202
            Circuit: the compiled Circuit.
        """

    def _update_post_processing_params(self):
        """Update post-processing params."""

    def fit(
        self, X: numpy.ndarray, y: numpy.ndarray, **fit_params
    ) -> ConcreteBaseEstimatorProtocol:
        """Initialize and fit the module.

        Args:
            X : training data
                By default, you should be able to pass:
                * numpy arrays
                * torch tensors
                * pandas DataFrame or Series
            y (numpy.ndarray): labels associated with training data
            **fit_params: additional parameters that can be used during training

        Returns: # noqa: DAR202
            ConcreteBaseEstimatorProto: the trained estimator
        """

    def fit_benchmark(
        self, X: numpy.ndarray, y: numpy.ndarray, *args, **kwargs
    ) -> Tuple[ConcreteBaseEstimatorProtocol, sklearn.base.BaseEstimator]:
        """Fit the quantized estimator and return reference estimator.

        This function returns both the quantized estimator (itself),
        but also a wrapper around the non-quantized trained NN. This is useful in order
        to compare performance between the quantized and fp32 versions of the classifier

        Args:
            X : training data
                By default, you should be able to pass:
                * numpy arrays
                * torch tensors
                * pandas DataFrame or Series
            y (numpy.ndarray): labels associated with training data
            *args: The arguments to pass to the underlying model.
            **kwargs: The keyword arguments to pass to the underlying model.

        Returns: # noqa: DAR202
            self: self fitted
            model: underlying estimator
        """


class ConcreteBaseClassifierProtocol(ConcreteBaseEstimatorProtocol, Protocol):
    """Concrete classifier protocol."""

    def predict(self, X: numpy.ndarray, execute_in_fhe: bool) -> numpy.ndarray:
        """Predicts for each sample the class with highest probability.

        Args:
            X (numpy.ndarray): Features
            execute_in_fhe (bool): Whether the inference should be done in fhe or not.

        Returns: # noqa: DAR202
            numpy.ndarray

        """

    def predict_proba(self, X: numpy.ndarray, execute_in_fhe: bool) -> numpy.ndarray:
        """Predicts for each sample the probability of each class.

        Args:
            X (numpy.ndarray): Features
            execute_in_fhe (bool): Whether the inference should be done in fhe or not.

        Returns: # noqa: DAR202
            numpy.ndarray

        """


class ConcreteBaseRegressorProtocol(ConcreteBaseEstimatorProtocol, Protocol):
    """Concrete regressor protocol."""

    def predict(self, X: numpy.ndarray, execute_in_fhe: bool) -> numpy.ndarray:
        """Predicts for each sample the expected value.

        Args:
            X (numpy.ndarray): Features
            execute_in_fhe (bool): Whether the inference should be done in fhe or not.

        Returns: # noqa: DAR202
            numpy.ndarray

        """
