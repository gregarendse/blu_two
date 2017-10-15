import os

import fire

from commander import CommanderImpl, Response


class CLI(object):
    def __init__(self):
        self.sub_process = CommanderImpl()

    def CaptureProcess(self, command: str, capture_name):
        response: Response = self.sub_process.call(command)

        os.makedirs('./tests/{}'.format(capture_name), exist_ok=True)

        with open('./tests/{}/return_code'.format(capture_name), 'w') as file:
            file.write(str(response.return_code))

        with open('./tests/{}/std_out'.format(capture_name), 'w') as file:
            for line in response.std_out:
                file.write("{line}\n".format(line=line))

        with open('./tests/{}/std_err'.format(capture_name), 'w') as file:
            for line in response.std_err:
                file.write("{line}\n".format(line=line))

    def CaptureMakeMkv(self):
        self.CaptureProcess('makemkvcon -r info disc:-1', 'scan_drives')
        self.CaptureProcess('makemkvcon -r info disc:0 --minlength=900 --noscan', 'scan_disc')
        self.CaptureProcess('makemkvcon -r mkv disc:0 0 ./tests --minlength=900 --noscan', 'rip_title')


if __name__ == '__main__':
    fire.Fire(CLI)
