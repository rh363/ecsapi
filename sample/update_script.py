from ecsapi import Api

api = Api()

print(
    api.update_script(
        52, "test updated", 'echo "test updated content" > /root/test.txt', False
    )
)
