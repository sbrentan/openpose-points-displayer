from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from starlette.responses import HTMLResponse

from points.database.database import get_db, PointsDatabase
from points.schemas.crud.csv_document import SkeletonGraphGet, GraphType
from points.schemas.models import Skeleton, PartType
from plotly import graph_objs as go

router = APIRouter()


templates = Jinja2Templates(directory="src/points/templates")


@router.get("/points", tags=["points"], summary="Read all points",
            description="Read all points", response_description="List of all points",
            response_model=list[Skeleton])
async def read_points(document_id: int, db: PointsDatabase = Depends(get_db)) -> list[Skeleton]:
    document = await db.document.get(document_id)
    skeleton_list = document.skeletons
    return skeleton_list


@router.get("/points/analysis", tags=["analysis"], response_class=HTMLResponse)
async def get_points_analysis(request: Request, document_id: int, db: PointsDatabase = Depends(get_db)) -> HTMLResponse:
    document = await db.document.get(document_id)
    return templates.TemplateResponse("points_analysis.html", {"request": request, "document": document})


@router.get("/points/graph", tags=["points"], summary="Read all points", description="Read all points",
            response_description="List of all points", response_class=HTMLResponse)
async def read_points_graph(document_id: int,  # graph_input: SkeletonGraphGet,
                            graph_type: GraphType, part_type: PartType,
                            db: PointsDatabase = Depends(get_db)) -> HTMLResponse:
    document = await db.document.get(document_id)
    skeleton_list = document.skeletons

    graph_input = SkeletonGraphGet(partType=part_type, graphType=graph_type)

    figure = go.Figure()

    x_axis_values = []
    y_axis_values = []
    for skeleton in skeleton_list:
        if graph_input.graph_type == GraphType.X_TIME or graph_input.graph_type == GraphType.Y_TIME:
            x_axis_values.append([skeleton.datetime for part in skeleton.parts if part.part_type == graph_input.part_type][0])
            if graph_input.graph_type == GraphType.X_TIME:
                y_axis_values.append([part.x for part in skeleton.parts if part.part_type == graph_input.part_type][0])
            else:
                y_axis_values.append([part.y for part in skeleton.parts if part.part_type == graph_input.part_type][0])
        elif graph_input.graph_type == GraphType.X_Y:
            y_axis_values.append([part.x for part in skeleton.parts if part.part_type == graph_input.part_type][0])
            x_axis_values.append([part.y for part in skeleton.parts if part.part_type == graph_input.part_type][0])
        elif graph_input.graph_type == GraphType.Y_X:
            x_axis_values.append([part.x for part in skeleton.parts if part.part_type == graph_input.part_type][0])
            y_axis_values.append([part.y for part in skeleton.parts if part.part_type == graph_input.part_type][0])
    figure.add_trace(go.Scatter(x=x_axis_values, y=y_axis_values, mode='lines+markers', name=str(document.name)))

    axis_titles = graph_input.graph_type.value.split("_")
    figure.update_layout(title="Graph " + graph_input.graph_type.value, xaxis_title=axis_titles[1],
                         yaxis_title=axis_titles[0])

    return HTMLResponse(content=figure.to_html(), status_code=200)
