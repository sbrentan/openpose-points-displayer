from fastapi import APIRouter, Depends

from common.schemas.models.message import SuccessMessage
from points.database.database import get_db, PointsDatabase
from points.schemas.crud.csv_document import CSVDocumentCreate
from points.schemas.models import CSVDocument

from points.routers.document._point import router as points_router

router = APIRouter(
    prefix="/documents",
    tags=["document"]
)


@router.post("", response_model=CSVDocument, status_code=201, summary="Create a new document",
             description="Create a new document", response_description="The created document")
async def create_document(new_document: CSVDocumentCreate, db: PointsDatabase = Depends(get_db)):
    document = CSVDocument(**new_document.model_dump())
    result = await db.document.create(document)
    return result


@router.get("", response_model=list[CSVDocument], summary="Read all documents",
            description="Read all documents", response_description="List of all documents")
async def read_documents(db: PointsDatabase = Depends(get_db)):
    result = await db.document.filter()
    return result


@router.get("/{document_id}", response_model=CSVDocument, summary="Read a document",
            description="Read a document", response_description="The requested document")
async def read_document(document_id: int, db: PointsDatabase = Depends(get_db)):
    result = await db.document.get(document_id)
    return result


@router.delete("/{document_id}", response_model=SuccessMessage, summary="Delete a document",
               description="Delete a document", response_description="True if the document was deleted")
async def delete_document(document_id: int, db: PointsDatabase = Depends(get_db)):
    result = await db.document.delete(document_id)
    return SuccessMessage(success=result, message="CSVDocument deleted", data={"document_id": document_id})


router.include_router(points_router, tags=["points"], prefix="/{document_id}/points")
