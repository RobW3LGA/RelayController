import pytest
import httpx
from httpx import AsyncClient, Client, Response, Headers
from pytest_httpx import httpx_mock, HTTPXMock
from fastapi import FastAPI, APIRouter
from tests.mocks import deviceSource, taskSource, isAuthenticated

from components import invokeApiRoutes


@pytest.fixture
def app_mockService():

  def getRoutes(apiRoutes: callable, hasValidAuth: bool):

    testRouter: APIRouter = APIRouter()
    apiRoutes(apiRouter=testRouter, deviceSource=deviceSource, taskSource=taskSource, isAuthenticated=hasValidAuth)

    testAPI: FastAPI = FastAPI()
    testAPI.include_router(router=testRouter, prefix="/api")
    return testAPI

  return getRoutes


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testurl"]  # LOWERCASED!!!


@pytest.mark.asyncio
async def test001_apiRouter_component_getDeviceStatus_requestAllDevices_returnArrayOfDevices(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/all"
  testValidAuth: bool = True
  httpx_mock.add_response(status_code=200, json={"relays": ["false"], "inputs": ["false"], "analog": 123.4})

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert (httpx_mock.get_requests())[0].url.raw_path == b"/api/status?key=Sup3rS3kr3tK3y"
  assert (httpx_mock.get_requests())[1].url.raw_path == b"/api/status?key=Sup3rS3kr3tK3y"
  assert sut.status_code == 200
  assert '[{"statusCode":200,"response":{"device":"testDeviceOne","state":{"relays":[{"relay":1,"name":"testRelayOneOne","isEnabled":false}],"inputs":[{"input":1,"name":"testInputOneOne","isTriggered":false}],"shelterTemp":123.4}' in sut.text
  assert '{"statusCode":200,"response":{"device":"testDeviceTwo","state":{"relays":[{"relay":1,"name":"testRelayTwoOne","isEnabled":false}],"inputs":[{"input":1,"name":"testInputTwoOne","isTriggered":false}],"shelterTemp":123.4}' in sut.text


@pytest.mark.asyncio
async def test002_apiRouter_component_getDeviceStatus_requestAllDevices_returnArrayContainingOneUnexpectedDeviceResponse(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/all"
  testValidAuth: bool = True
  httpx_mock.add_response(status_code=204, json={"unexpected": "response"})

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 204
  assert '[{"statusCode":204,"response":{"device":"testDeviceOne","error":204,"reason":"{\\"unexpected\\": \\"response\\"}"' in sut.text


@pytest.mark.asyncio
async def test003_apiRouter_component_getDeviceStatus_requestValidDevice_returnSingleValidDevice(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/testDeviceOne"
  testValidAuth: bool = True
  httpx_mock.add_response(status_code=200, json={"relays": ["false"], "inputs": ["false"], "analog": 123.4})

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 200
  assert '{"device":"testDeviceOne","state":{"relays":[{"relay":1,"name":"testRelayOneOne","isEnabled":false}],"inputs":[{"input":1,"name":"testInputOneOne","isTriggered":false}],"shelterTemp":123.4}' in sut.text


@pytest.mark.asyncio
async def testEx01_apiRouter_component_getDeviceStatus_requestValidDevice_returnErrorFourZeroFourUnreachable(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/testDeviceOne"
  testValidAuth: bool = True

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 404
  assert sut.text == '{"device":"testDeviceOne","address":"1.2.3.4","reason":"unreachable"}'


@pytest.mark.asyncio
async def testEx02_apiRouter_component_getDeviceStatus_requestInvalidDevice_returnFourZeroZeroError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/badDevice"
  testValidAuth: bool = True

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 400
  assert sut.text == '{"detail":{"error":"badDevice","reason":"invalid device"}}'


@pytest.mark.asyncio
async def testEx03_apiRouter_component_getDeviceStatus_missingAuthenticationHeader_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  # testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/testDevice"
  testValidAuth: bool = True

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":"Not authenticated"}'


@pytest.mark.asyncio
async def testEx04_apiRouter_component_getDeviceStatus_badAuthCredentialsWithAllDevices_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/all"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":{"error":"test@email.local","reason":"authentication failure"}}'


@pytest.mark.asyncio
async def testEx05_apiRouter_component_getDeviceStatus_badAuthCredentialsWithValidDevice_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/getDeviceStatus/testDeviceOne"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":{"error":"test@email.local","reason":"authentication failure"}}'


@pytest.mark.asyncio
async def test004_apiRouter_component_enableTestTask_enableAllDevicesRelay_returnArrayOfDevices(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableTestTaskOne/all"
  testValidAuth: bool = True
  httpx_mock.add_response(status_code=200, json={"relays": ["true"], "inputs": ["false"], "analog": 123.4})

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert (httpx_mock.get_requests())[0].url.raw_path == b"/api/relay/on?relay=1&key=Sup3rS3kr3tK3y"
  assert (httpx_mock.get_requests())[1].url.raw_path == b"/api/relay/on?relay=1&key=Sup3rS3kr3tK3y"
  assert sut.status_code == 201
  assert '[{"statusCode":201,"response":{"device":"testDeviceOne","state":{"relays":[{"relay":1,"name":"testRelayOneOne","isEnabled":true}],"inputs":[{"input":1,"name":"testInputOneOne","isTriggered":false}],"shelterTemp":123.4}' in sut.text
  assert '{"statusCode":201,"response":{"device":"testDeviceTwo","state":{"relays":[{"relay":1,"name":"testRelayTwoOne","isEnabled":true}],"inputs":[{"input":1,"name":"testInputTwoOne","isTriggered":false}],"shelterTemp":123.4}' in sut.text


@pytest.mark.asyncio
async def test005_apiRouter_component_enableTestRelay_enableValidDeviceRelay_returnSingleValidDevice(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableTestRelayOneOne/testDeviceOne"
  testValidAuth: bool = True
  httpx_mock.add_response(status_code=200, json={"relays": ["true"], "inputs": ["false"], "analog": 123.4})

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert (httpx_mock.get_request()).url.raw_path == b"/api/relay/on?relay=1&key=Sup3rS3kr3tK3y"
  assert sut.status_code == 201
  assert '{"device":"testDeviceOne","state":{"relays":[{"relay":1,"name":"testRelayOneOne","isEnabled":true}],"inputs":[{"input":1,"name":"testInputOneOne","isTriggered":false}],"shelterTemp":123.4}' in sut.text


@pytest.mark.asyncio
async def test006_apiRouter_component_disableTestRelay_disableValidDeviceRelay_returnSingleValidDevice(httpx_mock: HTTPXMock, app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/disableTestRelayOneOne/testDeviceOne"
  testValidAuth: bool = True
  httpx_mock.add_response(status_code=200, json={"relays": ["false"], "inputs": ["false"], "analog": 123.4})

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert (httpx_mock.get_request()).url.raw_path == b"/api/relay/off?relay=1&key=Sup3rS3kr3tK3y"
  assert sut.status_code == 201
  assert '{"device":"testDeviceOne","state":{"relays":[{"relay":1,"name":"testRelayOneOne","isEnabled":false}],"inputs":[{"input":1,"name":"testInputOneOne","isTriggered":false}],"shelterTemp":123.4},' in sut.text


@pytest.mark.asyncio
async def testEx06_apiRouter_component_enableTestRelay_requestInvalidDevice_returnFourZeroZeroError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableTestRelayOneOne/badDevice"
  testValidAuth: bool = True

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 400
  assert sut.text == '{"detail":{"error":"badDevice","reason":"invalid device"}}'


@pytest.mark.asyncio
async def testEx07_apiRouter_component_enableTestRelay_missingAuthenticationHeader_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  # testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableTestRelay/testDevice"
  testValidAuth: bool = True

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":"Not authenticated"}'


@pytest.mark.asyncio
async def testEx08_apiRouter_component_enableTestTask_badAuthCredentialsWithAllDevices_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableTestTaskOne/all"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":{"error":"test@email.local","reason":"authentication failure"}}'


@pytest.mark.asyncio
async def testEx09_apiRouter_component_enableTestRelay_badAuthCredentialsWithValidDevice_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableTestRelayOneOne/testDeviceOne"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":{"error":"test@email.local","reason":"authentication failure"}}'


@pytest.mark.asyncio
async def testEx10_apiRouter_component_enableTestRelay_unauthorizedUser_returnFourZeroOneError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic ZG9ub3RlbnRlckBlbWFpbC5sb2NhbDpQQHNzdzByZA=="}
  testTargetUrl: str = "/api/enableTestRelayOneOne/testDeviceOne"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 401
  assert sut.text == '{"detail":{"error":"donotenter@email.local","reason":"authorization failure"}}'


@pytest.mark.asyncio
async def testEx11_apiRouter_component_invalidTaskVerbiage_enterInvalidTaskStructure_returnFourZeroZeroError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/disgruntledTestRelay/testDevice"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 400
  assert sut.text == '{"detail":{"error":"disgruntledTestRelay","reason":"invalid task"}}'


@pytest.mark.asyncio
async def testEx12_apiRouter_component_invalidTask_enterInvalidTask_returnFourZeroZeroError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableInvalidTask/all"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 400
  assert sut.text == '{"detail":{"error":"enableInvalidTask","reason":"invalid task request"}}'


@pytest.mark.asyncio
async def testEx13_apiRouter_component_invalidRelay_enterInvalidRelay_returnFourZeroZeroError(app_mockService: callable):

  testBaseUrl: str = "http://testurl"
  testAuthHeader: dict = {"authorization": "Basic dGVzdEBlbWFpbC5sb2NhbDp0M3N0VDBrM24="}
  testTargetUrl: str = "/api/enableInvalidRelay/testDevice"
  testValidAuth: bool = False

  async with AsyncClient(app=app_mockService(apiRoutes=invokeApiRoutes, hasValidAuth=isAuthenticated(testValidAuth)), base_url=testBaseUrl, headers=Headers(testAuthHeader)) as client:

    sut: Response = await client.get(testTargetUrl)

  assert sut.status_code == 400
  assert sut.text == '{"detail":{"error":"enableInvalidRelay","reason":"invalid device request"}}'
