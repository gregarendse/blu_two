from commander import Response


class Commander():
    def call(self, cmd: str) -> Response:
        raise NotImplementedError()
