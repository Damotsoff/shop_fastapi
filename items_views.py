from typing import Annotated
from fastapi import APIRouter, Path

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}/")
async def get_item_by_id(item_id: Annotated[int, Path(ge=1, le=1000_000)]):
    return {"id": item_id}
