<!-- markdownlint-disable -->

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `concrete.ml.onnx.ops_impl`

ONNX ops implementation in python + numpy.

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `cast_to_float`

```python
cast_to_float(inputs)
```

Cast values to floating points.

**Args:**

- <b>`inputs`</b> (Tuple\[numpy.ndarray\]):  The values to consider.

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  The float values.

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `onnx_func_raw_args`

```python
onnx_func_raw_args(*args)
```

Decorate a numpy onnx function to flag the raw/non quantized inputs.

**Args:**

- <b>`*args (tuple[Any])`</b>:  function argument names

**Returns:**

- <b>`result`</b> (ONNXMixedFunction):  wrapped numpy function with a list of mixed arguments

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_where_body`

```python
numpy_where_body(c: ndarray, t: ndarray, f: Union[ndarray, int]) → ndarray
```

Compute the equivalent of numpy.where.

This function is not mapped to any ONNX operator (as opposed to numpy_where). It is usable by functions which are mapped to ONNX operators, e.g. numpy_div or numpy_where.

**Args:**

- <b>`c`</b> (numpy.ndarray):  Condition operand.
- <b>`t`</b> (numpy.ndarray):  True operand.
- <b>`f`</b> (numpy.ndarray):  False operand.

**Returns:**

- <b>`numpy.ndarray`</b>:  numpy.where(c, t, f)

# FIXME: can it be improved with a native numpy.where in Concrete Numpy? # https://github.com/zama-ai/concrete-numpy-internal/issues/1429

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_where`

```python
numpy_where(c: ndarray, t: ndarray, f: ndarray) → Tuple[ndarray]
```

Compute the equivalent of numpy.where.

**Args:**

- <b>`c`</b> (numpy.ndarray):  Condition operand.
- <b>`t`</b> (numpy.ndarray):  True operand.
- <b>`f`</b> (numpy.ndarray):  False operand.

**Returns:**

- <b>`numpy.ndarray`</b>:  numpy.where(c, t, f)

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_add`

```python
numpy_add(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute add in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Add-13

**Args:**

- <b>`a`</b> (numpy.ndarray):  First operand.
- <b>`b`</b> (numpy.ndarray):  Second operand.

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Result, has same element type as two inputs

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L191"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_constant`

```python
numpy_constant(**kwargs)
```

Return the constant passed as a kwarg.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Constant-13

**Args:**

- <b>`**kwargs`</b>:  keyword arguments

**Returns:**

- <b>`Any`</b>:  The stored constant.

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_matmul`

```python
numpy_matmul(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute matmul in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#MatMul-13

**Args:**

- <b>`a`</b> (numpy.ndarray):  N-dimensional matrix A
- <b>`b`</b> (numpy.ndarray):  N-dimensional matrix B

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Matrix multiply results from A * B

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L299"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_relu`

```python
numpy_relu(x: ndarray) → Tuple[ndarray]
```

Compute relu in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Relu-14

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L313"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_sigmoid`

```python
numpy_sigmoid(x: ndarray) → Tuple[ndarray]
```

Compute sigmoid in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Sigmoid-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L327"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_cos`

```python
numpy_cos(x: ndarray) → Tuple[ndarray]
```

Compute cos in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Cos-7

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_cosh`

```python
numpy_cosh(x: ndarray) → Tuple[ndarray]
```

Compute cosh in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Cosh-9

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_sin`

```python
numpy_sin(x: ndarray) → Tuple[ndarray]
```

Compute sin in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Sin-7

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L369"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_sinh`

```python
numpy_sinh(x: ndarray) → Tuple[ndarray]
```

Compute sinh in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Sinh-9

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L383"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_tan`

```python
numpy_tan(x: ndarray) → Tuple[ndarray]
```

Compute tan in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Tan-7

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L397"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_tanh`

```python
numpy_tanh(x: ndarray) → Tuple[ndarray]
```

Compute tanh in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Tanh-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_acos`

```python
numpy_acos(x: ndarray) → Tuple[ndarray]
```

Compute acos in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Acos-7

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L425"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_acosh`

```python
numpy_acosh(x: ndarray) → Tuple[ndarray]
```

Compute acosh in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Acosh-9

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L439"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_asin`

```python
numpy_asin(x: ndarray) → Tuple[ndarray]
```

Compute asin in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Asin-7

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L453"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_asinh`

```python
numpy_asinh(x: ndarray) → Tuple[ndarray]
```

Compute sinh in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Asinh-9

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L467"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_atan`

```python
numpy_atan(x: ndarray) → Tuple[ndarray]
```

Compute atan in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Atan-7

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L481"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_atanh`

```python
numpy_atanh(x: ndarray) → Tuple[ndarray]
```

Compute atanh in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Atanh-9

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L495"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_elu`

```python
numpy_elu(x: ndarray, alpha: float = 1) → Tuple[ndarray]
```

Compute elu in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Elu-6

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`alpha`</b> (float):  Coefficient

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L511"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_selu`

```python
numpy_selu(
    x: ndarray,
    alpha: float = 1.6732632423543772,
    gamma: float = 1.0507009873554805
) → Tuple[ndarray]
```

Compute selu in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Selu-6

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`alpha`</b> (float):  Coefficient
- <b>`gamma`</b> (float):  Coefficient

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L534"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_celu`

```python
numpy_celu(x: ndarray, alpha: float = 1) → Tuple[ndarray]
```

Compute celu in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Celu-12

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`alpha`</b> (float):  Coefficient

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L550"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_leakyrelu`

```python
numpy_leakyrelu(x: ndarray, alpha: float = 0.01) → Tuple[ndarray]
```

Compute leakyrelu in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#LeakyRelu-6

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`alpha`</b> (float):  Coefficient

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L566"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_thresholdedrelu`

```python
numpy_thresholdedrelu(x: ndarray, alpha: float = 1) → Tuple[ndarray]
```

Compute thresholdedrelu in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#ThresholdedRelu-10

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`alpha`</b> (float):  Coefficient

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L585"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_hardsigmoid`

```python
numpy_hardsigmoid(
    x: ndarray,
    alpha: float = 0.2,
    beta: float = 0.5
) → Tuple[ndarray]
```

Compute hardsigmoid in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#HardSigmoid-6

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`alpha`</b> (float):  Coefficient
- <b>`beta`</b> (float):  Coefficient

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L604"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_softplus`

```python
numpy_softplus(x: ndarray) → Tuple[ndarray]
```

Compute softplus in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Softplus-1

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L619"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_abs`

```python
numpy_abs(x: ndarray) → Tuple[ndarray]
```

Compute abs in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Abs-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L634"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_div`

```python
numpy_div(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute div in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Div-14

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor
- <b>`b`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L655"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_mul`

```python
numpy_mul(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute mul in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Mul-14

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor
- <b>`b`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L671"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_sub`

```python
numpy_sub(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute sub in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Sub-14

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor
- <b>`b`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L687"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_log`

```python
numpy_log(x: ndarray) → Tuple[ndarray]
```

Compute log in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Log-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L725"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_erf`

```python
numpy_erf(x: ndarray) → Tuple[ndarray]
```

Compute erf in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Erf-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L740"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_hardswish`

```python
numpy_hardswish(x: ndarray) → Tuple[ndarray]
```

Compute hardswish in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#hardswish-14

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L759"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_exp`

```python
numpy_exp(x: ndarray) → Tuple[ndarray]
```

Compute exponential in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Exp-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  The exponential of the input tensor computed element-wise

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L774"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_equal`

```python
numpy_equal(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute equal in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Equal-11

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L790"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_not`

```python
numpy_not(x: ndarray) → Tuple[ndarray]
```

Compute not in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Not-1

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L806"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_not_float`

```python
numpy_not_float(x: ndarray) → Tuple[ndarray]
```

Compute not in numpy according to ONNX spec and cast outputs to floats.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Not-1

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L821"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_greater`

```python
numpy_greater(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute greater in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Greater-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L838"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_greater_float`

```python
numpy_greater_float(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute greater in numpy according to ONNX spec and cast outputs to floats.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Greater-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L854"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_greater_or_equal`

```python
numpy_greater_or_equal(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute greater or equal in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#GreaterOrEqual-12

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L871"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_greater_or_equal_float`

```python
numpy_greater_or_equal_float(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute greater or equal in numpy according to ONNX specs and cast outputs to floats.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#GreaterOrEqual-12

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L887"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_less`

```python
numpy_less(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute less in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Less-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L904"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_less_float`

```python
numpy_less_float(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute less in numpy according to ONNX spec and cast outputs to floats.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Less-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L920"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_less_or_equal`

```python
numpy_less_or_equal(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute less or equal in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#LessOrEqual-12

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L937"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_less_or_equal_float`

```python
numpy_less_or_equal_float(x: ndarray, y: ndarray) → Tuple[ndarray]
```

Compute less or equal in numpy according to ONNX spec and cast outputs to floats.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#LessOrEqual-12

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`y`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L953"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_identity`

```python
numpy_identity(x: ndarray) → Tuple[ndarray]
```

Compute identity in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Identity-14

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L989"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_transpose`

```python
numpy_transpose(x: ndarray, perm=None) → Tuple[ndarray]
```

Transpose in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Transpose-13

**Args:**

- <b>`x`</b> (numpy.ndarray):  Input tensor
- <b>`perm`</b> (numpy.ndarray):  Permutation of the axes

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1071"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `torch_avgpool`

```python
torch_avgpool(
    x: ndarray,
    ceil_mode: int,
    kernel_shape: Tuple[int, ],
    pads: Tuple[int, ],
    strides: Tuple[int, ]
) → Tuple[ndarray]
```

Compute Average Pooling using Torch.

Currently supports 2d average pooling with torch semantics. This function is ONNX compatible.

See: https://github.com/onnx/onnx/blob/main/docs/Operators.md#AveragePool

**Args:**

- <b>`x`</b> (numpy.ndarray):  input data (many dtypes are supported). Shape is N x C x H x W for 2d
- <b>`ceil_mode`</b> (int):  ONNX rounding parameter, expected 0 (torch style dimension computation)
- <b>`kernel_shape`</b> (Tuple\[int\]):  shape of the kernel. Should have 2 elements for 2d conv
- <b>`pads`</b> (Tuple\[int\]):  padding in ONNX format (begin, end) on each axis
- <b>`strides`</b> (Tuple\[int\]):  stride of the convolution on each axis

**Returns:**

- <b>`res`</b> (numpy.ndarray):  a tensor of size (N x InChannels x OutHeight x OutWidth).
- <b>`See https`</b>: //pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html

**Raises:**

- <b>`AssertionError`</b>:  if the pooling arguments are wrong

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_cast`

```python
numpy_cast(data: ndarray, to: int) → Tuple[ndarray]
```

Execute ONNX cast in Numpy.

Supports only booleans for now, which are converted to integers.

See: https://github.com/onnx/onnx/blob/main/docs/Operators.md#Cast

**Args:**

- <b>`data`</b> (numpy.ndarray):  Input encrypted tensor
- <b>`to`</b> (int):  integer value of the onnx.TensorProto DataType enum

**Returns:**

- <b>`result`</b> (numpy.ndarray):  a tensor with the required data type

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_batchnorm`

```python
numpy_batchnorm(
    x: ndarray,
    scale: ndarray,
    bias: ndarray,
    input_mean: ndarray,
    input_var: ndarray,
    epsilon=1e-05,
    momentum=0.9,
    training_mode=0
) → Tuple[ndarray]
```

Compute the batch normalization of the input tensor.

This can be expressed as:

Y = (X - input_mean) / sqrt(input_var + epsilon) * scale + B

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#BatchNormalization-14

**Args:**

- <b>`x`</b> (numpy.ndarray):  tensor to normalize, dimensions are in the form of (N,C,D1,D2,...,Dn),  where N is the batch size, C is the number of channels.
- <b>`scale`</b> (numpy.ndarray):  scale tensor of shape (C,)
- <b>`bias`</b> (numpy.ndarray):  bias tensor of shape (C,)
- <b>`input_mean`</b> (numpy.ndarray):  mean values to use for each input channel, shape (C,)
- <b>`input_var`</b> (numpy.ndarray):  variance values to use for each input channel, shape (C,)
- <b>`epsilon`</b> (float):  avoids division by zero
- <b>`momentum`</b> (float):  momentum used during training of the mean/variance, not used in inference
- <b>`training_mode`</b> (int):  if the model was exported in training mode this is set to 1, else 0

**Returns:**

- <b>`numpy.ndarray`</b>:  Normalized tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_flatten`

```python
numpy_flatten(x: ndarray, axis: int = 1) → Tuple[ndarray]
```

Flatten a tensor into a 2d array.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Flatten-13.

**Args:**

- <b>`x`</b> (numpy.ndarray):  tensor to flatten
- <b>`axis`</b> (int):  axis after which all dimensions will be flattened (axis=0 gives a 1D output)

**Returns:**

- <b>`result`</b>:  flattened tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1269"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_or`

```python
numpy_or(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute or in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Or-7

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor
- <b>`b`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1285"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_or_float`

```python
numpy_or_float(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute or in numpy according to ONNX spec and cast outputs to floats.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Or-7

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor
- <b>`b`</b> (numpy.ndarray):  Input tensor

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1300"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_round`

```python
numpy_round(a: ndarray) → Tuple[ndarray]
```

Compute round in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Round-11 Remark that ONNX Round operator is actually a rint, since the number of decimals is forced to be 0

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor whose elements to be rounded.

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor with rounded input elements.

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L1317"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `numpy_pow`

```python
numpy_pow(a: ndarray, b: ndarray) → Tuple[ndarray]
```

Compute pow in numpy according to ONNX spec.

See https://github.com/onnx/onnx/blob/main/docs/Changelog.md#Pow-13

**Args:**

- <b>`a`</b> (numpy.ndarray):  Input tensor whose elements to be raised.
- <b>`b`</b> (numpy.ndarray):  The power to which we want to raise.

**Returns:**

- <b>`Tuple[numpy.ndarray]`</b>:  Output tensor.

______________________________________________________________________

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ONNXMixedFunction`

A mixed quantized-raw valued onnx function.

ONNX functions will take inputs which can be either quantized or float. Some functions only take quantized inputs, but some functions take both types. For mixed functions we need to tag the parameters that do not need quantization. Thus quantized ops can know which inputs are not QuantizedArray and we avoid unnecessary wrapping of float values as QuantizedArrays.

<a href="https://github.com/zama-ai/concrete-ml-internal/tree/main/src/concrete/ml/onnx/ops_impl.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(function, non_quant_params: Set[str])
```

Create the mixed function and raw parameter list.

**Args:**

- <b>`function`</b> (Any):  function to be decorated
- <b>`non_quant_params`</b>:  Set\[str\]: set of parameters that will not be quantized (stored  as numpy.ndarray)