from fastapi import APIRouter

router = APIRouter()


@router.get("/points", tags=["points"], summary="Read all points",
            description="Read all points", response_description="List of all points")
async def read_points(document_id: int):
    return {"message": "Read all points"}
