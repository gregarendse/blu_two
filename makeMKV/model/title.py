from typing import List

from makeMKV.model import Stream


class Title(object):
    id: int
    name: str
    chapters: int
    duration: int
    bytes: int
    source_file_name: str
    segments_count: int
    segments_map: int
    output_file_name: str
    metadata_language_code: str
    metadata_language_name: str
    tree_info: str
    panel_title: str
    order_weight: int

    streams: List[Stream]

    def __init__(self,
                 id=None,
                 name=None,
                 chapters=None,
                 duration=None,
                 bytes=None,
                 source_file_name=None,
                 segments_count=None,
                 segments_map=None,
                 output_file_name=None,
                 metadata_language_code=None,
                 metadata_language_name=None,
                 tree_info=None,
                 panel_title=None,
                 order_weight=None):
        self.id = id
        self.name = name
        self.chapters = chapters
        self.duration = duration
        self.bytes = bytes
        self.source_file_name = source_file_name
        self.segments_count = segments_count
        self.segments_map = segments_map
        self.output_file_name = output_file_name
        self.metadata_language_code = metadata_language_code
        self.metadata_language_name = metadata_language_name
        self.tree_info = tree_info
        self.panel_title = panel_title
        self.order_weight = order_weight

        self.streams = []
