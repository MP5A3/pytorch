from dataclasses import dataclass
from typing import Optional, Union, Sequence, Set, List, Tuple, Dict

from tools.codegen.api.types import *
from tools.codegen.model import *

# Represents a saved variable invovled in backward calculation.
# Note that it can be a derived property of an input argument, e.g.:
# we could save `other.scalar_type()` instead of the entire `other` tensor.
@dataclass(frozen=True)
class Variable:
    # Name of the saved variable.
    # Suffix is appended if it's derived property, e.g.: `other_scalar_type`
    name: str

    # The cpp type string.
    # TODO: change from raw string to model.Type
    type: str

    # The expression to read the derived property at save time, e.g.:
    # `other.scalar_type()`.
    expr: str

# Represents a backward formula that calculates derivatives for one
# or more tensors.
@dataclass(frozen=True)
class Derivative:
    # The formula string (legit C++ expression).
    # Note that expressions against input arguments are replaced with the
    # corresponding saved variables.
    # E.g.: `mul_tensor_backward(grad, self, other.scalar_type())`
    #    -> `mul_tensor_backward(grad, self, other_scalar_type)`
    formula: str

    # Names of the arguments for which this formula calculates derivatives.
    var_names: Tuple[str, ...]

    # Saved inputs that are referenced by the formula.
    saved_inputs: Tuple[Variable, ...]

    # Saved outputs that are referenced by the formula.
    saved_outputs: Tuple[Variable, ...]

# Represents differentiability info for a NativeFunction.
@dataclass(frozen=True)
class DifferentiabilityInfo:
    # The base name read from derivatives.yaml.
    name: str

    # The matching native function.
    func: NativeFunction

    # The name of the generated autograd function.
    # It's set only if we will calculate a derivative, i.e.
    # 'args_with_derivatives' is not empty.
    op: Optional[str]

    # The derivatives formulae for this function.
    derivatives: Sequence[Derivative]

    # The union of 'saved_inputs' of all 'derivatives'.
    all_saved_inputs: Sequence[Variable]

    # The union of 'saved_outputs' of all 'derivatives'.
    all_saved_outputs: Sequence[Variable]

    # The function's input arguments for which it calculates derivatives.
    # It's the union of 'var_names' of all 'derivatives', sorted by the
    # argument order in the function schema.
    args_with_derivatives: Sequence[CppArgument]

    # Names of arguments whose derivative formula is 'non_differentiable'.
    non_differentiable_arg_names: Sequence[str]

    # Raw data read from derivatives.yaml.
    output_differentiability: Optional[List[bool]]
