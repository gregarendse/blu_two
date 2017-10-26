from typing import List

import click

from commander import CommanderImpl
from makeMKV.makeMKV import MakeMKV
from makeMKV.model.drive import Drive


@click.command()
@click.option('--rip', '-r', multiple=True, is_flag=True, help='Rip media from disc')
def hello(rip: bool):
    click.echo('Hello world')

    if rip:
        makeMKV: MakeMKV = MakeMKV(CommanderImpl())
        drives: List[Drive] = makeMKV.scan_drives()

        for drive in drives:
            drive = makeMKV.scan_disc(drive)

            for key, value in drive.disc.titles.items():
                makeMKV.rip_disc(drive, 'F:\\video', value.id)


if __name__ == '__main__':
    hello()
