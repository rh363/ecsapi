import os

import requests
from typing import Optional, Literal, Any, get_args, Dict

from ._server import _ServerListResponse, _ServerRetrieveResponse
from .errors import UnauthorizedError, NotFoundError, ClientError

AllowedVersions = Literal[2]
AllowedProtocols = Literal["http", "https"]

TOKEN_ENV_VAR = "ECSAPI_TOKEN"
HOST_ENV_VAR = "ECSAPI_HOST"
PORT_ENV_VAR = "ECSAPI_PORT"
PREFIX_ENV_VAR = "ECSAPI_PREFIX"
VERSION_ENV_VAR = "ECSAPI_VERSION"
PROTOCOL_ENV_VAR = "ECSAPI_PROTOCOL"

DEFAULT_HOST = "api.seeweb.it"
DEFAULT_PORT = 80
DEFAULT_PORT_SSL = 443
DEFAULT_PREFIX = "ecs"
DEFAULT_VERSION = 2
DEFAULT_PROTOCOL = "https"


def __initialize_env__(value: Any, default: Any, env_var: str):
    if value is not None:
        return value
    return os.getenv(env_var, default)


def __initialize_token__(token: Optional[str] = None):
    token = __initialize_env__(token, None, TOKEN_ENV_VAR)
    if token is None:
        raise ValueError("Token is required")
    return token


def __initialize_host__(host: Optional[str] = None):
    return __initialize_env__(host, DEFAULT_HOST, HOST_ENV_VAR)


def __initialize_prefix__(prefix: Optional[str] = None):
    return __initialize_env__(prefix, DEFAULT_PREFIX, PREFIX_ENV_VAR)


def __initialize_version__(
    version: Optional[AllowedVersions] = None,
) -> AllowedVersions:
    version = __initialize_env__(version, DEFAULT_VERSION, VERSION_ENV_VAR)
    if isinstance(version, str):
        if not version.isdigit():
            raise ValueError("Version must be a number")
        version = int(version)
    if version not in get_args(AllowedVersions):
        raise ValueError(f"Version must be in AllowedVersions: {AllowedVersions}")
    return version


def __initialize_protocol__(
    protocol: Optional[AllowedProtocols] = None,
) -> AllowedProtocols:
    protocol = __initialize_env__(protocol, DEFAULT_PROTOCOL, PROTOCOL_ENV_VAR)
    if protocol not in get_args(AllowedProtocols):
        raise ValueError(f"Protocol must be in AllowedProtocols: {AllowedProtocols}")
    return protocol


def __initialize_port__(
    port: Optional[int] = None, protocol: Optional[AllowedProtocols] = "https"
):
    if protocol == "https":
        port = __initialize_env__(port, DEFAULT_PORT_SSL, PORT_ENV_VAR)
    else:
        port = __initialize_env__(port, DEFAULT_PORT, PORT_ENV_VAR)
    if isinstance(port, str):
        if not port.isdigit():
            raise ValueError("Port must be a number")
        port = int(port)
    return port


class Api:

    def __init__(
        self,
        token: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        prefix: Optional[str] = None,
        version: Optional[AllowedVersions] = None,
        protocol: Optional[AllowedProtocols] = None,
        timeout: Optional[int] = 10,
    ):
        self.token = __initialize_token__(token)
        self._host = __initialize_host__(host)
        self._prefix = __initialize_prefix__(prefix)
        self._version: AllowedVersions = __initialize_version__(version)
        self._protocol: AllowedProtocols = __initialize_protocol__(protocol)
        self._port = __initialize_port__(port, self._protocol)
        self.timeout = timeout

    def __generate_base_url(self, include_version: bool = True) -> str:
        url = f"{self._protocol}://{self._host}:{self._port}/{self._prefix}"
        if include_version:
            url += f"/v{self._version}"
        return url

    def __generate_authentication_headers(self):
        return {"X-APITOKEN": f"{self.token}"}

    def __request(
        self,
        url,
        method,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        if timeout is None:
            timeout = self.timeout
        return requests.request(
            method, url, json=body, params=params, headers=headers, timeout=timeout
        )

    def __check_response(self, response):
        if response.status_code != 200:
            if response.status_code == 401:
                raise UnauthorizedError(response)
            if response.status_code == 404:
                raise NotFoundError(response)
            if 400 >= response.status_code <= 499:
                raise ClientError(response)
            if 500 >= response.status_code <= 599:
                raise ClientError(response)

    def __get(
        self,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        return self.__request(
            url,
            "GET",
            params=params,
            timeout=timeout,
            headers=headers,
        )

    def __post(
        self,
        url: str,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        return self.__request(
            url,
            "POST",
            params=params,
            body=body,
            timeout=timeout,
            headers=headers,
        )

    def __put(
        self,
        url: str,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        return self.__request(
            url,
            "PUT",
            params=params,
            body=body,
            timeout=timeout,
            headers=headers,
        )

    def __patch(
        self,
        url: str,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        return self.__request(
            url,
            "PATCH",
            params=params,
            body=body,
            timeout=timeout,
            headers=headers,
        )

    def __delete(
        self,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        return self.__request(
            url,
            "DELETE",
            params=params,
            timeout=timeout,
            headers=headers,
        )

    def fetch_servers(self):
        response = self.__get(
            f"{self.__generate_base_url()}/servers",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        servers_response = _ServerListResponse.model_validate_json(response.text)
        return servers_response.server

    def fetch_server(self, name: str):
        response = self.__get(
            f"{self.__generate_base_url()}/servers/{name}",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        server_response = _ServerRetrieveResponse.model_validate_json(response.text)
        return server_response.server
