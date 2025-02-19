class NotFoundError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Not Found: {self.response.text}"


class ClientError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Client Error: {self.response.text}"


class ServerError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Server Error: {self.response.text}"


class UnauthorizedError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"User Unauthorized: {self.response.text}"
