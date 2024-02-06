from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from points.database.database import get_db, PointsDatabase
from points.schemas.crud.csv_document import SkeletonGraphGet, GraphVariable
from points.schemas.models import Skeleton, PartType
from plotly import graph_objs as go

router = APIRouter()


@router.get("/points", tags=["points"], summary="Read all points",
            description="Read all points", response_description="List of all points",
            response_model=list[Skeleton])
async def read_points(document_id: int, db: PointsDatabase = Depends(get_db)) -> list[Skeleton]:
    document = await db.document.get(document_id)
    skeleton_list = document.skeletons
    return skeleton_list


@router.get("/points/graph", tags=["points"], summary="Read all points",
            description="Read all points", response_description="List of all points",
            response_class=HTMLResponse)
async def read_points_graph(document_id: int, part_type: PartType, graph_variable: GraphVariable, db: PointsDatabase = Depends(get_db)) -> HTMLResponse:
    document = await db.document.get(document_id)
    skeleton_list = document.skeletons

    graph_input = SkeletonGraphGet(part_type=part_type, graph_variable=graph_variable)

    figure = go.Figure()

    values = []
    datetimes = []
    for skeleton in skeleton_list:
        datetimes.append([skeleton.datetime for part in skeleton.parts if part.part_type == graph_input.part_type][0])
        if graph_input.graph_variable == GraphVariable.variable_x:
            values.append([part.x for part in skeleton.parts if part.part_type == graph_input.part_type][0])
        else:
            values.append([part.y for part in skeleton.parts if part.part_type == graph_input.part_type][0])
    figure.add_trace(go.Scatter(x=datetimes, y=values, mode='lines+markers', name=str(document.name)))

    figure.update_layout(title='Points ' + graph_input.part_type.value, xaxis_title='X', yaxis_title='Y')

    return HTMLResponse(content=figure.to_html(), status_code=200)
