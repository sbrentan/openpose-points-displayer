from pydantic import BaseModel


class CSVDocumentCreate(BaseModel):
    name: str
