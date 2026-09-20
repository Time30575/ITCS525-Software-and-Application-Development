from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies import aeval, get_expand_percent, get_history 
## get_expand_percent is function not a value, this will make it able to test via pytest
from app.schemas import Expression

router = APIRouter()

## Lec 5, now the calculate should route input from dependency file
@router.post("/calculate")
def calculate(expression: Expression,
              expand_percent=Depends(get_expand_percent),
              history=Depends(get_history),
              ):
    expr = expression.expr

    try:
        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            message = "; ".join(str(error.get_error()) for error in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": message}

        history.appendleft(
            {
                "expr": expr,
                "result": str(result),
                "timestamp": datetime.now().isoformat(),
            }
        )

        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as error:
        return {"ok": False, "expr": expr, "error": str(error)}
