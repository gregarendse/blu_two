import os

from commander import Comander, Response


class MockCommander(Comander):
    def __init__(self, return_code: int, std_out_source: str, std_err_source: str):
        super().__init__()
        self.std_out_source = std_out_source
        self.std_err_source = std_err_source
        self.return_code = return_code

    def call(self, cmd: str) -> Response:
        with open(self.std_out_source) as file:
            std_out = file.read()

        with open(self.std_err_source) as file:
            std_err = file.read()

        return Response(self.return_code, std_out.split('\n'), std_err.split('\n'))
