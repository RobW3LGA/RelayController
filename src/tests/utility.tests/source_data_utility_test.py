import pytest
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from typing import List

from utilities import getDataSource


class MockData(BaseModel):

  input: str
  output: dict
  options: List[str]


def test001_sourceData_utility_getDataSource_inputValidPathAndModel_returnValidObjectData():

  testPath = "./tests/mocks/test_good_data.json"

  sut = getDataSource(path=testPath, source=MockData)

  assert str(type(sut)) == "<class 'source_data_utility_test.MockData'>"
  assert type(sut.input) == str
  assert sut.input == "goodData"
  assert type(sut.output) == dict
  assert sut.output == {"good": "data"}
  assert type(sut.options) == list
  assert sut.options == ["good", "data"]


def testEx01_sourceData_utility_getDataSource_inputInvalidData_throwValidationError():

  testPath = "./tests/mocks/test_bad_data.json"

  with pytest.raises(HTTPException) as sut:
    getDataSource(path=testPath, source=MockData)

  assert str(type(sut)) == "<class '_pytest._code.code.ExceptionInfo'>"
  assert str(sut) == "<ExceptionInfo HTTPException(status_code=503, detail={'error': 'test_bad_data', 'reason': 'data validation failure'}) tblen=2>"


def testEx02_sourceData_utility_getDataSource_inputInvalidPath_throwFileNotFoundError():

  testPath = "./tests/mocks/test_missing_data.json"

  with pytest.raises(HTTPException) as sut:
    getDataSource(path=testPath, source=MockData)

  assert str(type(sut)) == "<class '_pytest._code.code.ExceptionInfo'>"
  assert str(sut) == "<ExceptionInfo HTTPException(status_code=503, detail={'error': 'test_missing_data', 'reason': 'database unreachable'}) tblen=2>"
