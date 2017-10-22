from typing import List, Dict

from makeMKV.model.enum import ItemAttributeId
from makeMKV.model.enum.disc_type import DiscType
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

    def __init__(self,
                 type=None,
                 name=None,
                 meta_language_code=None,
                 meta_language_name=None,
                 tree_info=None,
                 panel_title=None,
                 volume_name=None,
                 order_weight=None):
        self.type = type
        self.name = name
        self.meta_language_code = meta_language_code
        self.meta_language_name = meta_language_name
        self.tree_info = tree_info
        self.panel_title = panel_title
        self.volume_name = volume_name
        self.order_weight = order_weight
        self.titles = {}

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        """
        CINFO:1,6209,"Blu-ray disc"

        :param input:
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


        :param input:
        :return:
        """
        # parts: List[str] = str(input).split(',', maxsplit=3)
        # title_index: int = int(parts[0])
        # attribute_id: ItemAttributeId = ItemAttributeId(int(parts[1]))
        # code: int = int(parts[2])
        # value: str = str(parts[3]).strip('\"')

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
