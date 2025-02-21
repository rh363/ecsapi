import json

from src.ecsapi._server import (
    ServerCreateRequest,
    ServerCreateRequestNetwork,
    ServerCreateRequestNetworkVlan,
)
from src.ecsapi.errors import (
    UnauthorizedError,
    NotFoundError,
    ActionExitStatusError,
    ActionMaxRetriesExceededError,
)
from src.ecsapi._api import (
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
from httmock import urlmatch, HTTMock, all_requests
from urllib.parse import parse_qs

from tests.store import (
    SERVERS_FETCH_RESPONSE,
    SERVER_FETCH_RESPONSE,
    SERVER_STATUS_FETCH_RESPONSE,
    PLANS_FETCH_RESPONSE,
    PLANS_AVAILABLE_FETCH_RESPONSE,
    REGIONS_FETCH_RESPONSE,
    REGIONS_AVAILABLE_FETCH_RESPONSE,
    IMAGES_FETCH_RESPONSE,
    TEMPLATES_FETCH_RESPONSE,
    TEMPLATE_FETCH_RESPONSE,
    TEMPLATE_CREATE_RESPONSE,
    TEMPLATE_UPDATE_RESPONSE,
    TEMPLATE_DELETE_RESPONSE,
    CLOUDSCRIPTS_FETCH_RESPONSE,
    CLOUDSCRIPT_FETCH_RESPONSE,
    CLOUDSCRIPT_CREATE_RESPONSE,
    CLOUDSCRIPT_UPDATE_RESPONSE,
    SERVER_CREATE_RESPONSE,
    SERVER_UPDATE_RESPONSE,
    ACTIONS_FETCH_RESPONSE,
    ACTION_FETCH_RESPONSE,
    SERVER_DELETE_RESPONSE,
    SINGLE_ACTION_RESPONSE,
    SSH_KEYS_FETCH_RESPONSE,
    SSH_KEY_FETCH_RESPONSE,
    SSH_KEY_DELETE_RESPONSE,
    SSH_KEY_CREATE_RESPONSE,
)


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


@urlmatch(path=r"^/api/v2/servers$")
def mock_server_create_response(url, request):
    return {"status_code": 200, "content": SERVER_CREATE_RESPONSE}


@urlmatch(path=r"^/api/v2/plans/available")
def mock_server_create_plan_available_response(url, request):
    return {"status_code": 200, "content": PLANS_AVAILABLE_FETCH_RESPONSE}


@urlmatch(method="PUT")
def mock_server_update_response(url, request):
    return {"status_code": 200, "content": SERVER_UPDATE_RESPONSE}


@urlmatch(method="GET")
def mock_server_update_fetch_response(url, request):
    return {"status_code": 200, "content": SERVER_FETCH_RESPONSE}


@all_requests
def mock_server_delete_fetch_response(url, request):
    return {"status_code": 200, "content": SERVER_DELETE_RESPONSE}


@all_requests
def mock_server_action_response(url, request):
    return {"status_code": 200, "content": SINGLE_ACTION_RESPONSE}


@all_requests
def mock_server_status_fetch_response(url, request):
    return {"status_code": 200, "content": SERVER_STATUS_FETCH_RESPONSE}


@all_requests
def mock_plans_fetch_response(url, request):
    return {"status_code": 200, "content": PLANS_FETCH_RESPONSE}


@all_requests
def mock_plans_available_fetch_response(url, request):
    return {"status_code": 200, "content": PLANS_AVAILABLE_FETCH_RESPONSE}


@all_requests
def mock_regions_fetch_response(url, request):
    return {"status_code": 200, "content": REGIONS_FETCH_RESPONSE}


@all_requests
def mock_regions_available_fetch_response(url, request):
    return {"status_code": 200, "content": REGIONS_AVAILABLE_FETCH_RESPONSE}


@all_requests
def mock_images_fetch_response(url, request):
    return {"status_code": 200, "content": IMAGES_FETCH_RESPONSE}


@all_requests
def mock_templates_fetch_response(url, request):
    return {"status_code": 200, "content": TEMPLATES_FETCH_RESPONSE}


@all_requests
def mock_template_fetch_response(url, request):
    return {"status_code": 200, "content": TEMPLATE_FETCH_RESPONSE}


@all_requests
def mock_template_create_response(url, request):
    return {"status_code": 200, "content": TEMPLATE_CREATE_RESPONSE}


@all_requests
def mock_template_update_response(url, request):
    return {"status_code": 200, "content": TEMPLATE_UPDATE_RESPONSE}


@all_requests
def mock_template_delete_response(url, request):
    return {"status_code": 200, "content": TEMPLATE_DELETE_RESPONSE}


@all_requests
def mock_cloud_scripts_fetch_response(url, request):
    return {"status_code": 200, "content": CLOUDSCRIPTS_FETCH_RESPONSE}


@all_requests
def mock_cloud_script_fetch_response(url, request):
    return {"status_code": 200, "content": CLOUDSCRIPT_FETCH_RESPONSE}


@all_requests
def mock_cloud_script_create_response(url, request):
    return {"status_code": 200, "content": CLOUDSCRIPT_CREATE_RESPONSE}


@all_requests
def mock_cloud_script_update_response(url, request):
    return {"status_code": 200, "content": CLOUDSCRIPT_UPDATE_RESPONSE}


@all_requests
def mock_cloud_script_delete_response(url, request):
    return {"status_code": 200}


@all_requests
def mock_actions_fetch_response(url, request):
    return {"status_code": 200, "content": ACTIONS_FETCH_RESPONSE}


@all_requests
def mock_action_fetch_response(url, request):
    return {"status_code": 200, "content": ACTION_FETCH_RESPONSE}


@all_requests
def mock_ssh_keys_fetch_response(url, request):
    return {"status_code": 200, "content": SSH_KEYS_FETCH_RESPONSE}


@all_requests
def mock_ssh_key_fetch_response(url, request):
    return {"status_code": 200, "content": SSH_KEY_FETCH_RESPONSE}


@all_requests
def mock_ssh_key_delete_response(url, request):
    return {"status_code": 200, "content": SSH_KEY_DELETE_RESPONSE}


@urlmatch(method="POST")
def mock_ssh_key_create_response(url, request):
    return {"status_code": 200, "content": SSH_KEY_CREATE_RESPONSE}


@urlmatch(method="GET")
def mock_ssh_key_create_fetch_response(url, request):
    return {"status_code": 200, "content": SSH_KEYS_FETCH_RESPONSE}


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


def test_Api_create_server():
    api = get_api()

    def bad_vlan():
        _ = [ServerCreateRequestNetworkVlan(vlan_id=100, vlans="200-500")]

    def bad_vlan_2():
        _ = [ServerCreateRequestNetworkVlan(vlan_id=100, vlans="abcde")]

    pytest.raises(ValueError, bad_vlan)
    pytest.raises(ValueError, bad_vlan_2)
    vlans = [
        ServerCreateRequestNetworkVlan(vlan_id=100, pvid=True),
        ServerCreateRequestNetworkVlan(vlans="200-500"),
    ]
    network = ServerCreateRequestNetwork(name="net000001", vlans=vlans)
    with HTTMock(
        mock_server_create_response, mock_server_create_plan_available_response
    ):
        api.create_server(
            ServerCreateRequest(
                plan="eCS1",
                location="it-fr2",
                image="almalinux-9",
                notes="test",
                password="fOo123456789bAr",
                reserved_plan="M12PeCS1",
                support="global",
                group="eg12345",
                user_customize=12,
                user_customize_env='AUTHOR="alex"',
                ssh_key="my-secret-key",
                networks=[network],
            ),
            True,
        )
    assert True


def test_Api_update_server():
    api = get_api()
    with HTTMock(mock_server_update_response, mock_server_update_fetch_response):
        api.update_server("ec200410", "david martinez", "edgerunner")


def test_Api_delete_server():
    api = get_api()
    with HTTMock(mock_server_delete_fetch_response):
        api.delete_server("ec200410")


def test_Api_turn_on_server():
    api = get_api()
    with HTTMock(mock_server_action_response):
        api.turn_on_server("ec200410")


def test_Api_turn_off_server():
    api = get_api()
    with HTTMock(mock_server_action_response):
        api.turn_off_server("ec200410")


def test_Api_rollback_server():
    api = get_api()
    with HTTMock(mock_server_action_response):
        api.rollback_server("ec200410", 1234)


def test_Api_fetch_server_status():
    api = get_api()
    with HTTMock(mock_server_status_fetch_response):
        api.fetch_server_status("ec200410")
    assert True


def test_Api_fetch_plans():
    api = get_api()
    with HTTMock(mock_plans_fetch_response):
        api.fetch_plans()
    assert True


def test_Api_fetch_plan_available():
    api = get_api()
    with HTTMock(mock_plans_available_fetch_response):
        api.fetch_plans_available()
    assert True


def test_Api_fetch_regions():
    api = get_api()
    with HTTMock(mock_regions_fetch_response):
        api.fetch_regions()
    assert True


def test_Api_fetch_regions_available():
    api = get_api()
    with HTTMock(mock_regions_available_fetch_response):
        api.fetch_regions_available("ECS1")
    assert True


def test_Api_fetch_images_basics():
    api = get_api()
    with HTTMock(mock_images_fetch_response):
        api.fetch_images_basics()
    assert True


def test_Api_fetch_images_cloud():
    api = get_api()
    with HTTMock(mock_images_fetch_response):
        api.fetch_images_cloud()
    assert True


def test_Api_fetch_templates():
    api = get_api()
    with HTTMock(mock_templates_fetch_response):
        api.fetch_templates()
    assert True


def test_Api_fetch_template():
    api = get_api()
    with HTTMock(mock_template_fetch_response):
        api.fetch_template(593)
    assert True


def test_Api_create_template():
    api = get_api()
    with HTTMock(mock_template_create_response):
        pytest.raises(ValueError, api.create_template)
        pytest.raises(ValueError, api.create_template, server="ec200410", snapshot=153)
        api.create_template(server="ec200410")
    assert True


def test_Api_update_template():
    api = get_api()
    with HTTMock(mock_template_update_response):
        api.update_template(600, "dear", "stars")
    assert True


def test_Api_delete_template():
    api = get_api()
    with HTTMock(mock_template_delete_response):
        api.delete_template(600)
    assert True


def test_Api_fetch_scripts():
    api = get_api()
    with HTTMock(mock_cloud_scripts_fetch_response):
        api.fetch_scripts()
    assert True


def test_Api_fetch_script():
    api = get_api()
    with HTTMock(mock_cloud_script_fetch_response):
        api.fetch_script(15)
    assert True


def test_Api_create_script():
    api = get_api()
    with HTTMock(mock_cloud_script_create_response):
        api.create_script("title", "content", False)
    assert True


def test_Api_update_script():
    api = get_api()
    with HTTMock(mock_cloud_script_update_response):
        api.update_script(15, "title", "content", False)
    assert True


def test_Api_delete_script():
    api = get_api()
    with HTTMock(mock_cloud_script_delete_response):
        api.delete_script(15)
    assert True


def test_Api_can_create_plan():
    api = get_api()
    with HTTMock(mock_plans_available_fetch_response):
        assert api.can_create_plan("eCS1", "it-fr2")
        assert not api.can_create_plan("FAKEPLAN", "it-fr2")
        assert not api.can_create_plan("eCS1", "FAKEREGION")
        assert not api.can_create_plan("ECS1GPU6", "it-mi2")


def test_Api_fetch_actions():
    api = get_api()
    with HTTMock(mock_actions_fetch_response):
        api.fetch_actions(resource="test")


def test_Api_fetch_action():
    api = get_api()
    with HTTMock(mock_action_fetch_response):
        api.fetch_action(1234)


def test_Api_watch_action():
    api = get_api()

    def on_fetch(*args, **kwargs):
        print(args, kwargs)

    with HTTMock(mock_action_fetch_response):
        with pytest.raises(ActionExitStatusError):
            api.watch_action(
                1234, desired_status="not existing status", exit_on_status="completed"
            )
        with pytest.raises(ActionMaxRetriesExceededError):
            api.watch_action(
                1234,
                desired_status="not existing status",
                exit_on_status="not existing status",
                fetch_every=0.001,
                max_retry=10,
            )

        api.watch_action(1234, desired_status="completed", on_fetch=on_fetch)
    assert True


def test_Api_fetch_ssh_keys():
    api = get_api()
    with HTTMock(mock_ssh_keys_fetch_response):
        api.fetch_ssh_keys()
    assert True


def test_Api_fetch_ssh_key():
    api = get_api()
    with HTTMock(mock_ssh_key_fetch_response):
        api.fetch_ssh_key(123)
    assert True


def test_Api_create_ssh_key():
    api = get_api()
    with HTTMock(mock_ssh_key_create_response, mock_ssh_key_create_fetch_response):
        api.create_ssh_key("my-secret-key", "test-key")
    assert True


def test_Api_delete_ssh_key():
    api = get_api()
    with HTTMock(mock_ssh_key_delete_response):
        api.delete_ssh_key(1234)
    assert True
