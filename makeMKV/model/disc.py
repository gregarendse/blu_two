import re
from typing import Dict, List, Optional

from makeMKV.model.enum.disc_type import DiscType
from makeMKV.model.enum.item_attribute_id import ItemAttributeId
from makeMKV.model.enum.item_info import ItemInfo
from makeMKV.model.title import Title


class Disc(object):
    type: DiscType
    name: str
    meta_language_code: str
    meta_language_name: str
    tree_info: str
    panel_title: ItemInfo
    volume_name: str
    order_weight: int
    titles: Dict[int, Title]
    ordered_titles: List[Title]
    year: int
    location: str

    def __init__(self,
                 type=None,
                 name=None,
                 meta_language_code=None,
                 meta_language_name=None,
                 tree_info=None,
                 panel_title=None,
                 volume_name=None,
                 order_weight=None,
                 location=None):
        self.type: DiscType = type
        self.name: str = str(name)
        self.meta_language_code = meta_language_code
        self.meta_language_name = meta_language_name
        self.tree_info = tree_info
        self.panel_title = panel_title
        self.volume_name = volume_name
        self.order_weight = order_weight
        self.titles = {}
        self.ordered_titles: List[Title] = []
        self.year = None
        self.location = None

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        """
        CINFO:1,6209,"Blu-ray disc"
        :return:
        """

        if ItemAttributeId.Type == attributeId:
            self.type = DiscType(code)
        elif ItemAttributeId.Name == attributeId:
            self.name = value
        elif ItemAttributeId.MetadataLanguageCode == attributeId:
            self.meta_language_code = value
        elif ItemAttributeId.MetadataLanguageName == attributeId:
            self.meta_language_name = value
        elif ItemAttributeId.TreeInfo == attributeId:
            self.tree_info = value
        elif ItemAttributeId.PanelTitle == attributeId:
            self.panel_title = ItemInfo(code)
        elif ItemAttributeId.VolumeName == attributeId:
            self.volume_name = value
        elif ItemAttributeId.OrderWeight == attributeId:
            self.order_weight = int(value)
        else:
            raise Exception(
                'Unknown Item Attribute Id: {itemAttributeId}, code: {code}, input: {input}'
                    .format(itemAttributeId=attributeId, code=code, input=input))

    def setTitleAttribute(self, titleId: int, attributeId: ItemAttributeId, code: int, value: str) -> None:
        """
        TINFO:0,16,0,"00080.mpls"

        :return:
        """

        if self.titles.get(titleId) == None:
            self.titles[titleId] = Title(titleId)

        self.titles.get(titleId).setAttribute(attributeId=attributeId, code=code, value=value)

    def setStreamAttribute(self, titleId: int, streamId: int, attributeId: ItemAttributeId, code: int,
                           value: str) -> None:
        """

        SINFO:0,0,1,6201,"Video"

        :param titleId:
        :param streamId:
        :param code:
        :param value:
        :return:
        """

        if self.titles.get(titleId) == None:
            raise Exception('No title for stream: {titleId}, Stream Id: {streamId}, Code: {code}, Value: {value}'
                            .format(titleId=titleId, streamId=streamId, code=code, value=value))
        else:
            self.titles.get(titleId).setStreamAttribute(streamId, attributeId, code, value)

    def getTitleById(self, id: int) -> Optional[Title]:
        for key, title in self.titles.items():
            if title.id == id:
                return title

    def get_nice_title(self) -> str:
        regex = re.compile(r'(DISC[_ ]?(\d+))|(D[_ ]?(\d+))|(SEASON[_ ]?(\d+))|(S[_ ]?(\d+))', re.IGNORECASE)
        working = regex.sub("", self.name)  # Remove Season and disc
        working = re.sub(r'_', ' ', working)  # Replace '_' with spaces
        working = "".join(x for x in working if x.isalnum() or x in " _-")

        return working.strip()  # Remove trailing/leading spaces

    def is_series(self) -> bool:
        search = re.compile(r'(DISC[_ ]?(\d+))|(D[_ ]?(\d+))|(SEASON[_ ]?(\d+))|(S[_ ]?(\d+))', re.IGNORECASE)
        if search.search(self.name):
            return True
        else:
            return False

    def get_disc_number(self) -> int:
        search = re.compile(r'(DISC[_ ]?(\d+))|(D[_ ]?(\d+))', re.IGNORECASE)
        s = search.search(self.name)

        counter = 0
        while s.group(len(s.groups()) - counter) is None:
            counter = counter + 1

        return int(s.group(len(s.groups()) - counter))

    def get_season_number(self) -> int:
        search = re.compile(r'(SEASON[_ ]?(\d+))|(S[_ ]?(\d+))', re.IGNORECASE)
        s = search.search(self.name)

        counter = 0
        while s.group(len(s.groups()) - counter) is None:
            counter = counter + 1

        return int(s.group(len(s.groups()) - counter))

    def get_movie_title(self) -> Title:
        # return self.ordered_titles[0]

        title: Title = self.ordered_titles[0]
        for item in self.ordered_titles:
            if item.chapters > title.chapters:
                title = item
        return title
