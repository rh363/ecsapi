from ecsapi_client import Api

api = Api()

print(api.fetch_regions_available("ECS1"))
