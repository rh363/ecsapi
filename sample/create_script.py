from ecsapi import Api

api = Api()

print(api.create_script("test", 'echo "test content" > /root/test.txt', False))
