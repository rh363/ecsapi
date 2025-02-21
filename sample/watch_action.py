from ecsapi import Api, ServerCreateRequest

api = Api()

print("start")
print("creating server...")
server, action = api.create_server(
    ServerCreateRequest(
        notes="test-watch", plan="ECS1", location="it-fr2", image="almalinux-9"
    )
)
print("creation action ...")
api.watch_action(
    action, on_fetch=lambda a, i: print(f"scanning action: {a.id} - retry: {i}")
)
print("action completed")
server = api.fetch_server(server.name)
print(f"server {server.name} created...")
print("cleaning all...")
print(f"deleting server {server.name}...")
action = api.delete_server(server.name)
api.watch_action(
    action.id,
    on_fetch=lambda a, i: print(f"scanning action: {a.id} - retry: {i}"),
    fetch_every=3,
)
print("action completed")
print("done")
