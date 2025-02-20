from ._api import Api
from ._plan import Plan, PlanListAdapter
from ._image import Image, ImageListAdapter
from ._region import Region, RegionListAdapter
from ._server import (
    Server,
    ServerListAdapter,
    ServerCreateRequestNetworkVlan,
    ServerCreateRequestNetwork,
    ServerCreateRequest,
)
from ._cloud_script import CloudScript, CloudScriptListAdapter
from ._discount_record import DiscountRecord, DiscountRecordListAdapter
from ._snapshot import Snapshot, SnapshotListAdapter
from ._server_support import ServerSupport, ServerSupportListAdapter
from ._action import Action, ActionListAdapter
from dotenv import load_dotenv
import os

DEFAULT_ECSAPI_ENV_FILE = "ECSAPI_ENV_FILE"


def __initialize_env_file():
    os.environ[DEFAULT_ECSAPI_ENV_FILE] = os.getenv(DEFAULT_ECSAPI_ENV_FILE, ".env")
    load_dotenv(os.getenv(DEFAULT_ECSAPI_ENV_FILE))


__initialize_env_file()

__all__ = (
    [
        "Api",
        "Plan",
        "Image",
        "Region",
        "Server",
        "CloudScript",
        "DiscountRecord",
        "Snapshot",
        "ServerSupport",
        "Action",
    ]
    + [
        "PlanListAdapter",
        "ImageListAdapter",
        "RegionListAdapter",
        "ServerListAdapter",
        "CloudScriptListAdapter",
        "DiscountRecordListAdapter",
        "SnapshotListAdapter",
        "ServerSupportListAdapter",
        "ActionListAdapter",
    ]
    + [
        "ServerCreateRequestNetworkVlan",
        "ServerCreateRequestNetwork",
        "ServerCreateRequest",
    ]
)
