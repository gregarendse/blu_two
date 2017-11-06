from copy import copy

from blu import Config
from commander import Commander, Response


class HandbrakeSettins(object):
    def __init__(self,
                 preset: str,
                 frameRate: float,
                 quality: int,
                 encoder: str,
                 encoderPreset: str,
                 encoderTune: str,
                 options: str):
        self.preset: str = preset
        self.preset: str = preset
        self.frameRate: str = frameRate
        self.quality: str = quality
        self.encoder: str = encoder
        self.encoderPreset: str = encoderPreset
        self.encoderTune: str = encoderTune
        self.options: str = options


class HandbrakeCLI(object):
    config: Config = Config()

    def __init__(self, commander: Commander):
        self.commander: Commander = commander
        self.executable: str = self.config.cfg['handbrake']['executable']
        self.defaultSettings = HandbrakeSettins(
            preset=self.config.cfg['handbrake']['preset'],
            frameRate=self.config.cfg['handbrake']['frame_rate'],
            quality=self.config.cfg['handbrake']['quality'],
            encoder=self.config.cfg['handbrake']['encoder']['encoder'],
            encoderPreset=self.config.cfg['handbrake']['encoder']['preset'],
            encoderTune=self.config.cfg['handbrake']['encoder']['tune'],
            options=self.config.cfg['handbrake']['options']
        )

    def compressFile(self, input_file: str, output_file: str, **kwargs):
        settings: HandbrakeSettins = copy(self.defaultSettings)

        if kwargs.get('frame_rate') is not None:
            settings.frameRate = kwargs.get('frame_rate')

        response: Response = self.commander.call(
            '{executable} --verbose --input="{input}" --output="{output}" --preset="{preset}" --rate={frameRate} --quality={quality} --encoder={encoder} --encoder-preset={encoderPreset} --encoder-tune={encoderTune} {options}'
                .format(executable=self.executable,
                        input=input_file,
                        output=output_file,
                        preset=settings.preset,
                        frameRate=settings.frameRate,
                        quality=settings.quality,
                        encoder=settings.encoder,
                        encoderPreset=settings.encoderPreset,
                        encoderTune=settings.encoderTune,
                        options=settings.options))

        if response.return_code != 0:
            print(response.std_err)
            raise Exception(response.return_code)
