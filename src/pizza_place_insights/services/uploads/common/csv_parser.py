import csv
from io import StringIO
from typing import Type, TypeVar

from fastapi import UploadFile
from pydantic import BaseModel, parse_obj_as

from . import csv_parser, exceptions

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


async def _parse_rows(file: UploadFile, model: Type[PydanticModel]) -> list[PydanticModel]:
    f = StringIO(str(await file.read(), "utf-8", "backslashreplace"))

    reader = csv.DictReader(
        f,
        delimiter=",",
    )

    rows = [row for row in reader]

    return parse_obj_as(list[model], rows, type_name=model.__name__)  # type: ignore


async def parse_and_check(file: UploadFile, model: Type[PydanticModel]) -> list[PydanticModel]:
    if not file.filename.lower().endswith(".csv"):
        raise exceptions.NotCsvError("Invalid file extension. File extension must be '.csv'")

    rows = await csv_parser._parse_rows(file, model)

    if not rows:
        raise exceptions.EmptyFileError("No data was found in the file")

    return rows
