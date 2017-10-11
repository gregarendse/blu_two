from commander import Response


class Comander():
    def __init__(self):
        pass

    def call(self, cmd: str) -> Response:
        raise NotImplementedError()
