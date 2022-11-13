import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.database.connection import get_db_sess
from pizza_place_insights.services.uploads import common

from . import controller  # , exceptions, schemas

log = logging.getLogger(__name__)

router = APIRouter(prefix="/pizza_types")


@router.put(
    "/",
    summary="Upload pizza types csv",
    description="Upload CSV containing pizza types",
    response_model=common.schemas.DefaultResponse,
)
async def update(
    file: UploadFile = File(..., description="CSV file"),
    db_sess: AsyncSession = Depends(get_db_sess),
) -> common.schemas.DefaultResponse:
    try:
        result = await controller.update(
            db_sess=db_sess,
            file=file,
        )
    except (
        ValidationError,
        common.exceptions.NotCsvError,
        common.exceptions.EmptyFileError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": f"{e}"}],
        )

    return result
