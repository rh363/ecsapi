class NotFoundError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Not Found({self.response.status_code}): {self.response.text}"


class ClientError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Client Error({self.response.status_code}): {self.response.text}"


class ServerError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Server Error({self.response.status_code}): {self.response.text}"


class UnauthorizedError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"User Unauthorized({self.response.status_code}): {self.response.text}"


class ActionMaxRetriesExceededError(Exception):
    def __init__(self, action_id: int, retry: int, last_status: str):
        self.action_id = action_id
        self.retry = retry
        self.last_status = last_status

    def __str__(self):
        return f"Max retry exceeded watching action `{self.action_id}` (retry: {self.retry}): exiting with status `{self.last_status}`"


class ActionExitStatusError(Exception):
    def __init__(self, action_id: int, retry: int, last_status: str):
        self.action_id = action_id
        self.retry = retry
        self.last_status = last_status

    def __str__(self):
        return f"Exit status encountered for `{self.action_id}` (retry: {self.retry}): exiting with status `{self.last_status}`"


class PlanNotAvailableError(Exception):
    def __init__(self, plan: str, region: str):
        self.plan = plan
        self.region = region

    def __str__(self):
        return f"Plan `{self.plan}` not available in region `{self.region}`"
