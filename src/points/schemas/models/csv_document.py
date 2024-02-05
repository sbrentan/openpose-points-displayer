from datetime import datetime
from typing import List

from sqlmodel import SQLModel, Field

import global_variables
from points.schemas.models.body import Skeleton


class CSVDocument(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    created_at: datetime = Field(default=datetime.now)

    @property
    def skeletons(self) -> List[Skeleton]:
        if self.id in global_variables.point_variables.document_skeletons:
            return global_variables.point_variables.document_skeletons[self.id]
        else:
            # TODO: read CSV file and return the skeletons
            skeleton_list = []
            global_variables.point_variables.document_skeletons[self.id] = skeleton_list
            return skeleton_list
