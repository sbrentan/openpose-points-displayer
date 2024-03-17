from fastapi import APIRouter, Depends

from common.schemas.models.message import SuccessMessage
from points.database.database import get_db, PointsDatabase
from points.schemas.models import Skeleton, BodyPart, PartType

router = APIRouter(
    prefix="/skeleton",
    tags=["skeleton"]
)


@router.post("", response_model=SuccessMessage, summary="Create a skeleton",
            description="Create a skeleton using open pose points", response_description="Success if skeleton created")
async def create_skeleton(skeleton: SkeletonCreate, db: PointsDatabase = Depends(get_db)):
    db.skeleton.create(skeleton)
    return result
