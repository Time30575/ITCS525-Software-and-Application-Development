from fastapi import APIRouter, Depends, Query

from app.dependencies import get_history as get_history_dependency
## lec 5, now history come from dependencies file, every API function that use it need to pull from depencency file
from app.schemas import CalculatorLog

router = APIRouter()


@router.get("/history", response_model=list[CalculatorLog])
def get_history(
                limit: int = Query(50, ge=1, le=100),
                history=Depends(get_history_dependency),
            ) -> list[CalculatorLog]:
    return list(history)[:limit]


@router.delete("/history")
def clear_history(history=Depends(get_history_dependency)):
    history.clear()
    return {"ok": True, "message": "History cleared successfully"}
