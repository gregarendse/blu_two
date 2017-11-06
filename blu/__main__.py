import os
from typing import List

import click

from blu.config import Config
from commander import CommanderImpl
from handbrakeCLI.handbrakeCLI_impl import HandbrakeCLI
from identifier.identifier_impl import Identifier
from makeMKV.makeMKV import MakeMKV
from makeMKV.model.drive import Drive
from makeMKV.model.stream import VideoStream


@click.command()
@click.option('--rip', '-r', multiple=True, is_flag=True, help='Rip media from disc')
@click.option('--config', '-C', help='Config file location. Default blu.yml')
def blu(rip: bool, config_location: str):
    config: Config = Config()

    if config_location:
        config.load(config_location)
    else:
        config.load('./blu.yml')

    if rip:
        # makeMKV: MakeMKV = MakeMKV(MockCommander(0, 'F:\\workspace\\blu_two\\makeMKV\\tests\\scan_drives\\std_out',
        #                                          'F:\\workspace\\blu_two\\makeMKV\\tests\\scan_drives\\std_err'))
        makeMKV: MakeMKV = MakeMKV(CommanderImpl())
        drives: List[Drive] = makeMKV.scan_drives()
        identifier: Identifier = Identifier()
        # compressor: HandbrakeCLI = HandbrakeCLI(
        #     MockCommander(0, 'F:\\workspace\\blu_two\\handbrakeCLI\\tests\\compressFile\\std_out',
        #                   'F:\\workspace\\blu_two\\handbrakeCLI\\tests\\compressFile\\std_err'))
        compressor: HandbrakeCLI = HandbrakeCLI(CommanderImpl())

        for drive in drives:
            # makeMKV: MakeMKV = MakeMKV(MockCommander(0, 'F:\\workspace\\blu_two\\makeMKV\\tests\\scan_disc\\std_out',
            #                                      'F:\\workspace\\blu_two\\makeMKV\\tests\\scan_disc\\std_err'))
            drive = makeMKV.scan_disc(drive)
            identifier.identify(drive.disc)

            for key, value in drive.disc.titles.items():
                # makeMKV: MakeMKV = MakeMKV(MockCommander(0, 'F:\\workspace\\blu_two\\makeMKV\\tests\\rip_title\\std_out',
                #                                  'F:\\workspace\\blu_two\\makeMKV\\tests\\rip_title\\std_err'))
                value.raw_location = makeMKV.rip_disc(drive, config.cfg['general']['location']['raw'], value.id)
                video_stream: VideoStream = value.getVideoStream()

                output = os.path.join(config.cfg['general']['location']['compressed'],
                                      config.cfg['general']['filename_format'] \
                                      .format(series=value.series,
                                              season=value.season,
                                              episode=value.episode,
                                              name=value.name,
                                              source=drive.disc.type.toString(),
                                              resolution=video_stream.video_size.y))
                compressor.compressFile(value.raw_location, output)
                value.output = output


if __name__ == '__main__':
    blu()
