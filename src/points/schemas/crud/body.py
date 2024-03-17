from enum import Enum

from pydantic import BaseModel, Field

from common.schemas.crud.common import create_crud_model
from points.schemas.models import Skeleton


SkeletonCreate = create_crud_model(
    Skeleton,
    CRUD.CREATE,
    excluded=["id"]
)
