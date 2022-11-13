import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.database.connection import get_db_sess
from pizza_place_insights.services.uploads import common

from . import controller, exceptions

log = logging.getLogger(__name__)

router = APIRouter(prefix="/orders")


@router.post(
    "/",
    summary="Upload orders and order details csvs",
    response_model=common.schemas.DefaultResponse,
)
async def create(
    files: list[UploadFile] = File(..., description="CSVs files"),
    db_sess: AsyncSession = Depends(get_db_sess),
) -> common.schemas.DefaultResponse:
    """This endpoint only accepts uploads containing 2 files.
    These files MUST be named:
    - orders.csv
    - order_details.csv

    Inserting orders that are already stored in the database will
    raise errors.
    """

    try:
        result = await controller.create(
            db_sess=db_sess,
            files=files,
        )
    except (
        ValidationError,
        common.exceptions.NotCsvError,
        common.exceptions.EmptyFileError,
        exceptions.InvalidFileCombinationError,
        exceptions.AlreadyExistsError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": f"{e}"}],
        )

    return result
