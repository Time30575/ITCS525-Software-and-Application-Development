import math
import re
from collections import deque

from asteval import Interpreter

## Lec 5, 
## Previously history was in main.py
HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

## create new, this will return history
def get_history():
    return history

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")


def expand_percent(expr: str) -> str:
    """Handle A op B% and standalone N% patterns."""
    value = expr
    while True:
        match = _percent_pair.search(value)
        if not match:
            break
        a, op, b = match.group("a", "op", "b")
        if op in "+-":
            replacement = f"{a} {op} (({b}/100)*{a})"
        elif op == "*":
            replacement = f"{a} * ({b}/100)"
        else:
            replacement = f"{a} / ({b}/100)"
        value = value[:match.start()] + replacement + value[match.end():]

    return _number_percent.sub(lambda match: f"({match.group('n')}/100)", value)

### Lec 5, expand_percent as function for test_main to test.
def get_expand_percent():
    return expand_percent