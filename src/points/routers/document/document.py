import base64
import os
from io import StringIO

from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from common.schemas.models.message import SuccessMessage
from points.database.database import get_db, PointsDatabase
from points.schemas.crud.csv_document import CSVDocumentCreate
from points.schemas.models import CSVDocument

from points.routers.document._point import router as points_router
from points.settings import DOCUMENTS_FOLDER

router = APIRouter(
    prefix="/documents",
    tags=["document"]
)


@router.post("", response_model=CSVDocument, status_code=201, summary="Create a new document",
             description="Create a new document", response_description="The created document")
async def create_document(new_document: CSVDocumentCreate, db: PointsDatabase = Depends(get_db)):

    base64_decoded_file = StringIO(new_document.csv_file)
    contents = base64_decoded_file.read()

    # decode file_content_base64
    decoded_file_content = base64.b64decode(contents).decode('utf-8')

    # Specify the folder to save the file
    upload_folder = DOCUMENTS_FOLDER
    os.makedirs(upload_folder, exist_ok=True)

    # Construct the file path
    file_name = new_document.name + ".csv"
    file_path = os.path.join(upload_folder, file_name)

    # Write the file contents to the specified path
    with open(file_path, "wb") as f:
        print("saving document " + file_name)
        f.write(decoded_file_content.encode('utf-8'))

    document = CSVDocument(name=new_document.name, file_name=file_name)
    result = await db.document.create(document)
    return result


@router.get("", response_model=list[CSVDocument], summary="Read all documents",
            description="Read all documents", response_description="List of all documents")
async def read_documents(db: PointsDatabase = Depends(get_db)):
    result = await db.document.filter()
    return result


@router.get("/html", response_class=HTMLResponse, summary="Read all documents html",
            description="Read all documents html", response_description="List of all documents html")
async def get_documents_html(db: PointsDatabase = Depends(get_db)):
    result = await db.document.filter()
    options_documents = ""
    for document in result:
        options_documents += f"<option value='{document.id}'>{document.name}</option>"
    return HTMLResponse(content=options_documents, status_code=200)


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


router.include_router(points_router, tags=["points"], prefix="/{document_id}")
