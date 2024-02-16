from enum import Enum

from pydantic import BaseModel, Field

from points.schemas.models import PartType


class CSVDocumentCreate(BaseModel):
    name: str
    csv_file: str = Field(alias="csvFile")


class GraphType(Enum):
    X_Y: str = "x_y"
    Y_X: str = "y_x"
    X_TIME: str = "x_time"
    Y_TIME: str = "y_time"


class SkeletonGraphGet(BaseModel):

    part_type: PartType = Field(alias="partType")
    graph_type: GraphType = Field(alias="graphType")
