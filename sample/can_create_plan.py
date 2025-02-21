from ecsapi import Api

api = Api()

print(api.can_create_plan(plan="ECS1GPU6", region="it-mi2"))  # False
print(api.can_create_plan(plan="eCS1", region="it-fr2"))  # True
