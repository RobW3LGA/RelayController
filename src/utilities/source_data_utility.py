from fastapi import HTTPException
from pydantic import ValidationError


def getDataSource(path: str, source: callable) -> callable:

  databaseName: str = ((path.split("/"))[-1].split("."))[0]
  try:
    return source.parse_file(path=path)

  except ValidationError as exception:
    raise HTTPException(status_code=503, detail={"error": databaseName, "reason": "data validation failure"})

  except FileNotFoundError:
    raise HTTPException(status_code=503, detail={"error": databaseName, "reason": "database unreachable"})
