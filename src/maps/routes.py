# from fastapi import APIRouter, status, Path, Response
# from typing import Annotated
# from src.dependencies import MapsServiceDep
# from .schemas import MapLoad, MapUnload, MapCoreUnload

from fastapi import APIRouter, status, Path, Response
from typing import Annotated
from fastapi.responses import StreamingResponse  # <‑‑ добавили
from io import StringIO, BytesIO
import csv
from openpyxl import Workbook

from src.dependencies import MapsServiceDep
from .schemas import MapLoad, MapUnload, MapCoreUnload


router = APIRouter(
    tags=['maps']
)


@router.post(
    '/directions/{direction_id}/maps/load',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Educational map successfully loaded'},
        404: {'description': 'Direction not found'}
    },
    summary='Load the educational map into the database'
)
def load_map(direction_id: Annotated[int, Path(gt=0)], data: MapLoad, maps_service: MapsServiceDep) -> Response:
    maps_service.load_map(direction_id, data)
    return {'success': 'ok'}


@router.get(
    '/directions/{direction_id}/maps/unload',
    responses={
        200: {'description': 'Educational map successfully unloaded'},
        404: {'description': 'Direction not found'}
    },
    summary='Unload the educational map from the database'
)
def unload_map(direction_id: Annotated[int, Path(gt=0)], maps_service: MapsServiceDep) -> MapUnload:
    return maps_service.unload_map(direction_id)

@router.get(
    '/directions/{direction_id}/maps/export',
    responses={
        200: {'description': 'Educational map successfully exported (CSV file)'},
        404: {'description': 'Direction not found'}
    },
    summary='Export the educational map as CSV file'
)
# NEW NEW NEW
def export_map_csv(direction_id: Annotated[int, Path(gt=0)],
                   maps_service: MapsServiceDep) -> StreamingResponse:
    # 1. Берём те же данные, что и для JSON‑выгрузки
    map_data: MapUnload = maps_service.unload_map(direction_id)

    # 2. Формируем CSV в памяти
    output = StringIO()
    writer = csv.writer(output, delimiter=';')

    # TODO: заполни заголовки и строки под свою структуру MapUnload
    writer.writerow(['discipline_name', 'semester', 'ects'])
    for row in map_data.rows:      # пример, подстрой под реальное поле
        writer.writerow([row.discipline_name, row.semester, row.ects])

    output.seek(0)

    headers = {
        "Content-Disposition": 'attachment; filename=\"plan.csv\"',
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type='text/csv',
        headers=headers,
    )


@router.get(
    '/directions/{direction_id}/maps/export/excel',
    responses={
        200: {'description': 'Educational map successfully exported (Excel file)'},
        404: {'description': 'Direction not found'}
    },
    summary='Export the educational map as Excel file'
)
def export_map_excel(direction_id: Annotated[int, Path(gt=0)],
                     maps_service: MapsServiceDep) -> StreamingResponse:
    # 1. Get the same data as for JSON unload
    map_data: MapUnload = maps_service.unload_map(direction_id)

    # 2. Create Excel workbook in memory
    wb = Workbook()
    ws = wb.active
    ws.title = "Educational Plan"

    # Headers
    headers = ['Map Core', 'Discipline', 'Department', 'Credit Units', 'Control Type', 'Lecture Hours', 'Practice Hours', 'Lab Hours', 'Semester', 'Competencies']
    ws.append(headers)

    # Fill data
    for map_core in map_data.map_cors:
        for block in map_core.discipline_blocks:
            competencies_str = ', '.join([f"{comp.code}: {comp.name}" for comp in block.competencies])
            row = [
                map_core.name,
                block.discipline.name,
                block.discipline.department.name,
                block.credit_units,
                block.control_type.name,
                block.lecture_hours,
                block.practice_hours,
                block.lab_hours,
                block.semester_number,
                competencies_str
            ]
            ws.append(row)

    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    headers = {
        "Content-Disposition": 'attachment; filename="plan.xlsx"',
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers,
    )


@router.get(
    '/map-cors/{map_core_id}/unload',
    responses={
        200: {'description': 'Map core successfully unloaded'},
        404: {'description': 'Map core not found'}
    },
    summary='Unload the map core from the database'
)
def unload_map_core(map_core_id: Annotated[int, Path(gt=0)], maps_service: MapsServiceDep) -> MapCoreUnload:
    return maps_service.unload_map_core(map_core_id)
