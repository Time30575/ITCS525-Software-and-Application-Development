from datetime import datetime

from pydantic import BaseModel


### Lec 5
## Idea of schemas.py file is to describe data only.
## Not doing calculation logic here

### note : previously Expression and Calculatorlog both have expr (duplicate field/purpose)
### move it to shared field location --> BaseExpression (Newly create)
### and create ExpressionIn for Expresion to use 'Expr' as input + remove the old Expression no use anymore.
### also create ExpressionOut for calculatorLog as return 'Expr' as output + remove old CalculatorLog no use anymore.


class BaseExpression(BaseModel):
    expr: str

class ExpressionIn(BaseExpression):
    pass
    ### move the expend_percent()
    ## so this ExpressionIn will return only 'expr' from BaseExpression

class ExpressionOut(ExpressionIn):
    ### the return data to user from API
    timestamp: datetime
    result: str
    ## also since ExpressionOut is inherits from ExpressionIn
    ## from Attribute resolution : it will return "expr" from ExpressionIn too.
    ## return : expr, timestamp,result


### since other file still call Expression and CalculatorLog, keep this to prevent unable to call.
Expression = ExpressionIn
CalculatorLog = ExpressionOut




### Lec 3
# class Expression(BaseModel):
#     expr: str

#     def expand_percent(self) -> str:
#         from app.dependencies import expand_percent

#         return expand_percent(self.expr)

# class CalculatorLog(BaseModel):
#     timestamp: datetime
#     expr: str
#     result: str



