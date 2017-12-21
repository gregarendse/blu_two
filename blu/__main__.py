import logging
import logging.config
import os
from typing import List

import click
import yaml

from blu.config import Config
from commander import CommanderImpl, MockCommander
from handbrakeCLI.handbrakeCLI_impl import HandbrakeCLI
from identifier.identifier_impl import Identifier
from makeMKV.makeMKV import MakeMKV
from makeMKV.model.drive import Drive
from makeMKV.model.enum.disc_type import DiscType
from makeMKV.model.stream import VideoStream
from makeMKV.model.title import Title

logger = logging.getLogger(__name__)


@click.command()
@click.option('--rip', '-r', multiple=True, is_flag=True, help='Rip media from disc')
@click.option('--config_location', '-C', help='Config file location. Default blu.yml')
@click.option('--log_config', '-L', help='Logging configuration file. Default logging.yml')
@click.option('--re-run', '-R', help='Re-run a previous run using output files', is_flag=True)
def blu(rip: bool, config_location: str, log_config: str, re_run: bool = False):
    setup_logging(default_path=log_config)
    config: Config = Config()

    if config_location:
        config.load(config_location)
    else:
        config.load('./blu.yml')

    if rip:

        if re_run:
            makeMKV: MakeMKV = MakeMKV(MockCommander())
            compressor: HandbrakeCLI = HandbrakeCLI(MockCommander())
        else:
            makeMKV: MakeMKV = MakeMKV(CommanderImpl())
            compressor: HandbrakeCLI = HandbrakeCLI(CommanderImpl())

        drives: List[Drive] = makeMKV.scan_drives()
        identifier: Identifier = Identifier()

        for drive in drives:
            drive = makeMKV.scan_disc(drive)
            identifier.identify(drive.disc)

            if drive.disc.is_series():
                ripSeries(compressor, config, drive, makeMKV, re_run)
            else:
                ripMovie(compressor, config, drive, makeMKV, re_run)


def ripMovie(compressor, config, drive, makeMKV, re_run):
    value: Title = drive.disc.get_movie_title()
    video_stream: VideoStream = value.getVideoStream()
    container: str = str(config.cfg['general']['movies']['container'])
    # str(config.cfg['general']['movies']['filename_format'] \
    file_name: str = ('{title} ({year}) - {source} {resolution}p'
        .format(title=drive.disc.get_nice_title(),
                year=drive.disc.year,
                source=drive.disc.type.toString(),
                resolution=video_stream.video_size.y)) + "." + container
    raw_dir: str = str(config.cfg['general']['movies']['location']['raw'])
    compress_dir: str = str(config.cfg['general']['movies']['location']['compressed'])

    if not re_run:
        os.makedirs(compress_dir, exist_ok=True)
        os.makedirs(raw_dir, exist_ok=True)

    output = os.path.join(compress_dir, file_name)

    raw_location = makeMKV.rip_disc(drive, raw_dir, value.id)
    value.raw_location = os.path.join(raw_dir, file_name)

    if not re_run:
        os.replace(raw_location, value.raw_location)

    # compressor.compressFile(input_file=value.raw_location,
    #                         output_file=output,
    #                         frame_rate=video_stream.frame_rate,
    #                         width=video_stream.video_size.x,
    #                         height=video_stream.video_size.y,
    #                         quality=getQuality(config, drive))
    value.output = output


def ripSeries(compressor, config, drive, makeMKV, re_run):
    for key, value in drive.disc.titles.items():
        video_stream: VideoStream = value.getVideoStream()
        container: str = str(config.cfg['general']['series']['container'])
        file_name: str = str(config.cfg['general']['series']['filename_format'] \
                             .format(series=value.series,
                                     season=value.season,
                                     episode=value.episode,
                                     name=value.name,
                                     source=drive.disc.type.toString(),
                                     resolution=video_stream.video_size.y)) + "." + container
        raw_dir: str = str(config.cfg['general']['series']['location']['raw'])
        compress_dir: str = str(config.cfg['general']['series']['location']['compressed'])

        if not re_run:
            os.makedirs(compress_dir, exist_ok=True)
            os.makedirs(raw_dir, exist_ok=True)

        output = os.path.join(compress_dir, file_name)

        raw_location = makeMKV.rip_disc(drive, raw_dir, value.id)
        value.raw_location = os.path.join(raw_dir, file_name)

        if not re_run:
            os.replace(raw_location, value.raw_location)

        compressor.compressFile(input_file=value.raw_location,
                                output_file=output,
                                frame_rate=video_stream.frame_rate,
                                width=video_stream.video_size.x,
                                height=video_stream.video_size.y,
                                quality=getQuality(config, drive))
        value.output = output


def getQuality(config, drive):
    quality: int = int(config.cfg['handbrake']['quality']['default'])
    if drive.disc.type == DiscType.BRAY_TYPE_DISK:
        quality = int(config.cfg['handbrake']['quality']['bluray'])
    elif drive.disc.type == DiscType.DVD_TYPE_DISK:
        quality = int(config.cfg['handbrake']['quality']['dvd'])
    return quality


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    blu()
