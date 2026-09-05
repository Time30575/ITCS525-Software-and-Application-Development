from datetime import datetime
from pydantic import BaseModel

from calculator import expand_percent

## Request body
class Expression(BaseModel):
    expr: str   ## add attribute : expr as str

    def expand_percent(self) -> str:    ## method, return expression after expanding the % symbol
        return expand_percent(self.expr)

## Response body
class CalculatorLog(BaseModel):     # add attribute timestamp,expr,result
    timestamp: datetime
    expr: str
    result: str
    