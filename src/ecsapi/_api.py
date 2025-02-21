import os
from time import sleep

import requests
from typing import Optional, Literal, Any, get_args, Dict, Union, Callable

from ._action import Action, _ActionListResponse, _ActionRetrieveResponse
from ._cloud_script import (
    _CloudScriptListResponse,
    _CloudScriptRetrieveResponse,
    _CloudScriptCreateRequest,
    _CloudScriptCreateResponse,
    _CloudScriptUpdateResponse,
)
from ._image import (
    _ImageListResponse,
    _CloudImageListResponse,
    _TemplateListResponse,
    _TemplateRetrieveResponse,
    _TemplateCreateRequest,
    _TemplateCreateResponse,
    _TemplateUpdateRequest,
    _TemplateUpdateResponse,
    _TemplateDeleteResponse,
)
from ._plan import _PlanListResponse, _PlanAvailableListResponse
from ._region import (
    _RegionListResponse,
    _RegionAvailableRequest,
    _RegionAvailableResponse,
)
from ._server import (
    _ServerListResponse,
    _ServerRetrieveResponse,
    _ServerRetrieveStatusResponse,
    ServerCreateRequest,
    _ServerCreateRequestResponse,
    _ServerUpdateRequest,
    _ServerActionRequest,
    _ServerDeleteResponse,
)
from .errors import (
    UnauthorizedError,
    NotFoundError,
    ClientError,
    ActionExitStatusError,
    ActionMaxRetriesExceededError,
    ServerError,
)

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

# region private init vars


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


# endregion


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

    # region private utility

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
        if response.status_code == 401:
            raise UnauthorizedError(response)
        if response.status_code == 404:
            raise NotFoundError(response)
        if 400 <= response.status_code <= 499:
            raise ClientError(response)
        if 500 <= response.status_code <= 599:
            raise ServerError(response)

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

    # endregion
    # region servers
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

    def fetch_server_status(self, name: str):
        response = self.__get(
            f"{self.__generate_base_url()}/servers/{name}/status",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        server_status_response = _ServerRetrieveStatusResponse.model_validate_json(
            response.text
        )
        return server_status_response.server.current_status

    def create_server(self, request: ServerCreateRequest):
        response = self.__post(
            f"{self.__generate_base_url()}/servers",
            body=request.model_dump(exclude_none=True),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        server_response = _ServerCreateRequestResponse.model_validate_json(
            response.text
        )
        return server_response.server, server_response.action_id

    def update_server(
        self,
        server_name: str,
        notes: str = None,
        group: Union[str, Literal["nogroup"]] = None,
    ):
        # TODO: Add test
        body = _ServerUpdateRequest(notes=notes, group=group)
        response = self.__put(
            f"{self.__generate_base_url()}/servers/{server_name}",
            body=body.model_dump(exclude_none=True),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        return self.fetch_server(server_name)

    def __send_server_action(
        self,
        server_name: str,
        action: Literal["rollback", "console", "power_on", "power_off"],
        add_body: dict = None,
    ):
        # TODO: Add test
        body = {"type": action, **add_body}
        body = _ServerActionRequest.model_validate(body)
        response = self.__post(
            f"{self.__generate_base_url()}/servers/{server_name}/actions",
            body=body.model_dump(exclude_none=True),
            headers=self.__generate_authentication_headers(),
        )
        action_response = Action.model_validate_json(response.text)
        return action_response

    def turn_on_server(self, server_name: str):
        # TODO: Add test
        return self.__send_server_action(server_name, "power_on")

    def turn_off_server(self, server_name: str):
        # TODO: Add test
        return self.__send_server_action(server_name, "power_off")

    def rollback_server(self, server_name: str, snapshot_id: int):
        # TODO: Add test
        return self.__send_server_action(
            server_name, "rollback", {"snapshot": snapshot_id}
        )

    def delete_server(self, server_name: str):
        response = self.__delete(
            f"{self.__generate_base_url()}/servers/{server_name}",
            headers=self.__generate_authentication_headers(),
        )
        action_response = _ServerDeleteResponse.model_validate_json(response.text)
        return action_response.action

    # endregion
    # region actions
    def fetch_actions(self, start=0, length=50, resource: str = None):
        params = {"start": start, "length": length}
        if resource is not None:
            params.update({"resource": resource})
        response = self.__get(
            f"{self.__generate_base_url()}/actions",
            params=params,
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        actions_response = _ActionListResponse.model_validate_json(response.text)
        return actions_response.actions, actions_response.total_actions

    def fetch_action(self, action_id: Union[int, Action]):
        if isinstance(action_id, Action):
            action_id = action_id.id
        response = self.__get(
            f"{self.__generate_base_url()}/actions/{action_id}",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        actions_response = _ActionRetrieveResponse.model_validate_json(response.text)
        return actions_response.action

    def watch_action(
        self,
        action_id: Union[int, Action],
        desired_status="completed",
        exit_on_status="failed",
        fetch_every=1,
        max_retry: int = None,
        on_fetch: Callable[[Action, int], None] = None,
    ):
        # TODO: Add tests
        retry = 0
        while True:
            action = self.fetch_action(action_id)
            if on_fetch is not None:
                on_fetch(action, retry)
            if action.status == desired_status:
                return action
            elif action.status == exit_on_status:
                raise ActionExitStatusError(
                    action_id=action_id, last_status=action.status, retry=retry
                )
            elif max_retry is not None and retry >= max_retry:
                raise ActionMaxRetriesExceededError(
                    action_id=action_id, last_status=action.status, retry=retry
                )
            else:
                retry += 1
                sleep(fetch_every)

    # endregion
    # region plans
    def fetch_plans(self):
        """
        Fetches the list of all plans from the API.

        This method sends a GET request to the plans endpoint of the API, utilizing
        authentication headers generated by the internal helper method. It validates
        the response from the server and parses it into a structured
        response object.
        """
        response = self.__get(
            f"{self.__generate_base_url()}/plans",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        plans_response = _PlanListResponse.model_validate_json(response.text)
        return plans_response.plans

    def fetch_plans_available(self):
        """
        Fetches and returns the plans currently available in the system.

        Similar to ``fetch_plans`` but return only the plans that are currently available
        and can be activated.
        It return a different object who specify all image who can be used for a plan, a list of
        all regions available for a plan, a list of server already active in each server (is used by web app
        for manage server isolations proposal).
        """
        response = self.__get(
            f"{self.__generate_base_url()}/plans/availables",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        plans_response = _PlanAvailableListResponse.model_validate_json(response.text)
        return plans_response.plans

    # endregion plans
    # region regions
    def fetch_regions(self):
        response = self.__get(
            f"{self.__generate_base_url()}/regions",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        regions_response = _RegionListResponse.model_validate_json(response.text)
        return regions_response.regions

    def fetch_regions_available(self, plan: str):
        body = _RegionAvailableRequest(plan=plan)
        response = self.__post(
            f"{self.__generate_base_url()}/regions/availables",
            body=body.model_dump(),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        regions_response = _RegionAvailableResponse.model_validate_json(response.text)
        return regions_response.regions

    # endregion
    # region images
    def fetch_images_basics(self):
        response = self.__get(
            f"{self.__generate_base_url()}/images/basics",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        images_response = _ImageListResponse.model_validate_json(response.text)
        return images_response.images

    def fetch_images_cloud(self):
        response = self.__get(
            f"{self.__generate_base_url()}/images/cloud-images",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        images_response = _CloudImageListResponse.model_validate_json(response.text)
        return images_response.images

    # endregion
    # region templates
    def fetch_templates(self):
        response = self.__get(
            f"{self.__generate_base_url()}/templates",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        templates_response = _TemplateListResponse.model_validate_json(response.text)
        return templates_response.templates

    def fetch_template(self, template_id: int):
        response = self.__get(
            f"{self.__generate_base_url()}/templates/{template_id}",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        template_response = _TemplateRetrieveResponse.model_validate_json(response.text)
        return template_response.template

    def create_template(
        self,
        server: Optional[str] = None,
        snapshot: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        if server is None and snapshot is None:
            raise ValueError("server or snapshot must be provided")
        if server is not None and snapshot is not None:
            raise ValueError("server and snapshot cannot be provided at the same time")
        body = _TemplateCreateRequest(
            server=server, snapshot=snapshot, description=description, notes=notes
        )
        response = self.__post(
            f"{self.__generate_base_url()}/templates",
            body=body.model_dump(),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        template_response = _TemplateCreateResponse.model_validate_json(response.text)
        return template_response.template, template_response.action_id

    def update_template(
        self,
        template_id: int,
        description: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        body = _TemplateUpdateRequest(description=description, notes=notes)
        response = self.__patch(
            f"{self.__generate_base_url()}/templates/{template_id}",
            body=body.model_dump(),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        template_response = _TemplateUpdateResponse.model_validate_json(response.text)
        return template_response.template

    def delete_template(self, template_id: int):
        response = self.__delete(
            f"{self.__generate_base_url()}/templates/{template_id}",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        action_response = _TemplateDeleteResponse.model_validate_json(response.text)
        return action_response.action

    # endregion

    # region cloud_script

    def fetch_scripts(self):
        response = self.__get(
            f"{self.__generate_base_url()}/scripts",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        scripts_response = _CloudScriptListResponse.model_validate_json(response.text)
        return scripts_response.scripts

    def fetch_script(self, script_id: int):
        response = self.__get(
            f"{self.__generate_base_url()}/scripts/{script_id}",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        script_response = _CloudScriptRetrieveResponse.model_validate_json(
            response.text
        )
        return script_response.script

    def create_script(
        self,
        title: str,
        content: str,
        windows=False,
    ):
        body = _CloudScriptCreateRequest(title=title, content=content, windows=windows)
        response = self.__post(
            f"{self.__generate_base_url()}/scripts",
            body=body.model_dump(),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        script_response = _CloudScriptCreateResponse.model_validate_json(response.text)
        return script_response

    def update_script(self, script_id: int, title: str, content: str, windows: bool):
        body = _CloudScriptCreateRequest(title=title, content=content, windows=windows)
        response = self.__patch(
            f"{self.__generate_base_url()}/scripts/{script_id}",
            body=body.model_dump(),
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        script_response = _CloudScriptUpdateResponse.model_validate_json(response.text)
        return script_response.script

    def delete_script(self, script_id: int):
        response = self.__delete(
            f"{self.__generate_base_url()}/scripts/{script_id}",
            headers=self.__generate_authentication_headers(),
        )
        self.__check_response(response)
        return

    # endregion


# TODO: Add optional timeout to each request
