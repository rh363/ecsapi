from ecsapi import Api
from ecsapi._server import (
    ServerCreateRequest,
)

api = Api()

# vlans = [
#     ServerCreateRequestNetworkVlan(vlan_id=100, pvid=True),
#     ServerCreateRequestNetworkVlan(vlans="200-500"),
# ]
# network = ServerCreateRequestNetwork(name="net000001", vlans=vlans)
# networks = [network]
networks = None
print(
    api.create_server(
        ServerCreateRequest(
            plan="ECS1",
            location="it-fr2",
            image="almalinux-9",
            notes="test",
            # password="fOo123456789bAr",
            # reserved_plan="M12PeCS1",
            # support="global",
            # group="eg12345",
            # user_customize=12,
            # user_customize_env='AUTHOR="alex"',
            # ssh_key="my-secret-key",
            # networks=networks,
        )
    )
)
