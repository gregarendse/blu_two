from commander import Response


class Commander():
    def __init__(self):
        pass

    def call(self, cmd: str) -> Response:
        raise NotImplementedError()
