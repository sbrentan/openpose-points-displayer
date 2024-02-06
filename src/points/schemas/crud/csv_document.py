from enum import Enum

from pydantic import BaseModel, Field

from points.schemas.models import PartType


class CSVDocumentCreate(BaseModel):
    name: str
    csv_file: str = Field(alias="csvFile")


class GraphVariable(Enum):
    variable_x: str = "x"
    variable_y: str = "y"


class SkeletonGraphGet(BaseModel):

    part_type: PartType
    graph_variable: GraphVariable
