import json

from src.ecsapi_client.errors import UnauthorizedError, NotFoundError
from src.ecsapi_client._api import (
    __initialize_env__,
    __initialize_token__,
    __initialize_host__,
    __initialize_prefix__,
    __initialize_port__,
    __initialize_protocol__,
    __initialize_version__,
    TOKEN_ENV_VAR,
    HOST_ENV_VAR,
    PREFIX_ENV_VAR,
    PORT_ENV_VAR,
    PROTOCOL_ENV_VAR,
    VERSION_ENV_VAR,
    DEFAULT_HOST,
    DEFAULT_PREFIX,
    DEFAULT_PORT,
    DEFAULT_PORT_SSL,
    DEFAULT_PROTOCOL,
    DEFAULT_VERSION,
    Api,
)
import os
import pytest
from httmock import urlmatch, HTTMock
from urllib.parse import parse_qs

from tests.store import SERVERS_FETCH_RESPONSE, SERVER_FETCH_RESPONSE


@urlmatch(netloc=r"localhost:8080")
def mock_generic_response(url, request):
    body = None
    if request.body is not None:
        body = json.loads(request.body)
    parsed_parameters = None
    if url.query is not None:
        parameters = parse_qs(url.query)
        parsed_parameters = {}
        for p in parameters:
            parsed_parameters[p] = parameters[p][0]
    res = {
        "status_code": 200,
        "headers": dict(request.headers),
        "url": url,
        "method": request.method,
    }
    if body is not None:
        res = {**res, **body}
    if parsed_parameters is not None:
        res.update({"params": parsed_parameters})
    return json.dumps(dict(res))


@urlmatch(netloc=r"localhost:8080")
def mock_servers_fetch_response(url, request):
    if request.headers["X-APITOKEN"] != "abcde":
        return {"status_code": 401}
    if url.path.endswith("/servers/ec12345"):
        return {"status_code": 404}
    if url.path.endswith("/servers/ec200410"):
        return {"status_code": 200, "content": SERVER_FETCH_RESPONSE}
    return {"status_code": 200, "content": SERVERS_FETCH_RESPONSE}


def get_api():
    return Api(
        token="abcde",
        host="localhost",
        port=8080,
        prefix="api",
        version=2,
        protocol="https",
    )


def get_invalid_api():
    return Api(
        token="edcba",
        host="localhost",
        port=8080,
        prefix="api",
        version=2,
        protocol="https",
    )


def test____initialize_env__():
    os.environ.clear()
    os.environ["TEST"] = "TEST"

    # test manually inserted value
    assert __initialize_env__("TEST", "", "ENV") == "TEST"
    # test manually inserted default
    assert __initialize_env__(None, "TEST", "ENV") == "TEST"
    # test env var value
    assert __initialize_env__(None, None, "TEST") == "TEST"


def test___initialize_token__():
    os.environ.clear()
    token = "abcde"
    assert __initialize_token__(token) == token
    pytest.raises(ValueError, __initialize_token__, None)
    os.environ[TOKEN_ENV_VAR] = token
    assert __initialize_token__(None) == token


def test___initialize_host__():
    os.environ.clear()
    host = "localhost"
    assert __initialize_host__(host) == host
    assert __initialize_host__(None) == DEFAULT_HOST
    os.environ[HOST_ENV_VAR] = host
    assert __initialize_host__(None) == host


def test___initialize_prefix__():
    os.environ.clear()
    prefix = "api"
    assert __initialize_prefix__(prefix) == prefix
    assert __initialize_prefix__(None) == DEFAULT_PREFIX
    os.environ[PREFIX_ENV_VAR] = prefix
    assert __initialize_prefix__(None) == prefix


def test____initialize_version__():
    os.environ.clear()
    version = 2
    assert __initialize_version__(version) == version
    assert __initialize_version__(None) == DEFAULT_VERSION
    os.environ[VERSION_ENV_VAR] = str(version)
    assert __initialize_version__(None) == version


def test___initialize_protocol__():
    os.environ.clear()
    protocol = "http"
    assert __initialize_protocol__("http") == protocol
    assert __initialize_protocol__(None) == DEFAULT_PROTOCOL
    os.environ[PROTOCOL_ENV_VAR] = protocol
    assert __initialize_protocol__(None) == protocol


def test___initialize_port__():
    os.environ.clear()
    port = 8080
    assert __initialize_port__(port) == port
    assert __initialize_port__(None) == DEFAULT_PORT_SSL
    assert __initialize_port__(None, "https") == DEFAULT_PORT_SSL
    assert __initialize_port__(None, "http") == DEFAULT_PORT
    os.environ[PORT_ENV_VAR] = str(port)
    assert __initialize_port__(None) == port
    pytest.raises(ValueError, __initialize_port__, "wr")


def test_Api__init__():
    os.environ.clear()
    token = "abcde"
    host = "localhost"
    prefix = "api"
    version = 2
    port = 8080

    # test explicit variables
    api = Api(token, host, port, prefix, version, "https")

    assert api.token == token
    assert api._host == host
    assert api._prefix == prefix
    assert api._version == version
    assert api._protocol == "https"
    assert api._port == port

    # test not inserted token
    pytest.raises(ValueError, Api)

    # test default vars

    api = Api(token)

    assert api.token == token
    assert api._host == DEFAULT_HOST
    assert api._prefix == DEFAULT_PREFIX
    assert api._version == DEFAULT_VERSION
    assert api._protocol == DEFAULT_PROTOCOL
    assert api._port == DEFAULT_PORT_SSL

    # test env vars

    os.environ[TOKEN_ENV_VAR] = token
    os.environ[HOST_ENV_VAR] = host
    os.environ[PREFIX_ENV_VAR] = prefix
    os.environ[VERSION_ENV_VAR] = str(version)
    os.environ[PROTOCOL_ENV_VAR] = "https"
    os.environ[PORT_ENV_VAR] = str(port)

    api = Api()

    assert api.token == token
    assert api._host == host
    assert api._prefix == prefix
    assert api._version == version
    assert api._protocol == "https"
    assert api._port == port


def test_Api__get_url__():
    os.environ.clear()
    token = "abcde"
    host = "localhost"
    prefix = "api"
    version = 2
    port = 8080
    api = Api(token, host, port, prefix, version, "https")
    assert api._Api__generate_base_url() == "https://localhost:8080/api/v2"


def test_Api__generate_authentication_headers():
    os.environ.clear()
    token = "abcde"
    host = "localhost"
    prefix = "api"
    version = 2
    port = 8080
    api = Api(token, host, port, prefix, version, "https")
    assert api._Api__generate_authentication_headers() == {"X-APITOKEN": "abcde"}


def test_Api__request():
    os.environ.clear()
    api = get_api()
    params = {"param1": "1", "param2": "2"}
    body = {"body1": 1, "body2": 2}
    headers = {"header1": "1", "header2": "2"}
    with HTTMock(mock_generic_response):
        r = api._Api__request(
            "http://localhost:8080", "GET", params=params, body=body, headers=headers
        )
    res = r.json()
    assert res["params"] == params
    assert res["body1"] == body["body1"]
    assert res["body2"] == body["body2"]
    assert res["headers"]["header1"] == headers["header1"]
    assert res["headers"]["header2"] == headers["header2"]
    assert res["method"] == "GET"


def test_Api__get():
    os.environ.clear()
    api = get_api()
    params = {"param1": "1", "param2": "2"}
    headers = {"header1": "1", "header2": "2"}
    with HTTMock(mock_generic_response):
        r = api._Api__get("http://localhost:8080", params=params, headers=headers)
    res = r.json()

    assert res["params"] == params
    assert res["headers"]["header1"] == headers["header1"]
    assert res["headers"]["header2"] == headers["header2"]
    assert res["method"] == "GET"


def test_Api__post():
    os.environ.clear()
    api = get_api()
    params = {"param1": "1", "param2": "2"}
    headers = {"header1": "1", "header2": "2"}
    body = {"body1": 1, "body2": 2}
    with HTTMock(mock_generic_response):
        r = api._Api__post(
            "http://localhost:8080", params=params, body=body, headers=headers
        )
    res = r.json()
    assert res["params"] == params
    assert res["body1"] == body["body1"]
    assert res["body2"] == body["body2"]
    assert res["headers"]["header1"] == headers["header1"]
    assert res["headers"]["header2"] == headers["header2"]
    assert res["method"] == "POST"


def test_Api__put():
    os.environ.clear()
    api = get_api()
    params = {"param1": "1", "param2": "2"}
    headers = {"header1": "1", "header2": "2"}
    body = {"body1": 1, "body2": 2}
    with HTTMock(mock_generic_response):
        r = api._Api__put(
            "http://localhost:8080", params=params, body=body, headers=headers
        )
    res = r.json()
    assert res["params"] == params
    assert res["body1"] == body["body1"]
    assert res["body2"] == body["body2"]
    assert res["headers"]["header1"] == headers["header1"]
    assert res["headers"]["header2"] == headers["header2"]
    assert res["method"] == "PUT"


def test_Api__patch():
    os.environ.clear()
    api = get_api()
    params = {"param1": "1", "param2": "2"}
    body = {"body1": 1, "body2": 2}
    headers = {"header1": "1", "header2": "2"}
    with HTTMock(mock_generic_response):
        r = api._Api__patch(
            "http://localhost:8080", params=params, body=body, headers=headers
        )
    res = r.json()
    assert res["params"] == params
    assert res["body1"] == body["body1"]
    assert res["body2"] == body["body2"]
    assert res["headers"]["header1"] == headers["header1"]
    assert res["headers"]["header2"] == headers["header2"]
    assert res["method"] == "PATCH"


def test_Api__delete():
    os.environ.clear()
    api = get_api()
    params = {"param1": "1", "param2": "2"}
    headers = {"header1": "1", "header2": "2"}
    with HTTMock(mock_generic_response):
        r = api._Api__delete("http://localhost:8080", params=params, headers=headers)
    res = r.json()
    assert res["params"] == params
    assert res["headers"]["header1"] == headers["header1"]
    assert res["headers"]["header2"] == headers["header2"]
    assert res["method"] == "DELETE"


def test_Api_fetch_servers():
    api = get_api()
    with HTTMock(mock_servers_fetch_response):
        api.fetch_servers()
    invalid_api = get_invalid_api()
    with HTTMock(mock_servers_fetch_response):
        pytest.raises(UnauthorizedError, invalid_api.fetch_servers)
    assert True


def test_Api_fetch_server():
    api = get_api()
    with HTTMock(mock_servers_fetch_response):
        pytest.raises(NotFoundError, api.fetch_server, "ec12345")
        api.fetch_server("ec200410")
    assert True
