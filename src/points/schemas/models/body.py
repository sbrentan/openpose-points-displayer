from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel
from sqlmodel import Field


class PartType(str, Enum):
    HEAD = "head"
    TRUNK = "trunk"
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"
    RIGHT_FOOT = "right_foot"
    LEFT_FOOT = "left_foot"


class BodyPart(BaseModel):
    x: float
    y: float
    part_type: PartType = Field(alias="partType")


class Skeleton(BaseModel):
    id: int
    datetime: datetime
    parts: List[BodyPart]
