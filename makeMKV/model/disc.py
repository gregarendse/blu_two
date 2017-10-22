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

    def setAttribute(self, input: str) -> None:
        """
        CINFO:1,6209,"Blu-ray disc"

        :param input:
        :return:
        """

        parts: List[str] = str(input).split(',')

        if len(parts) < 3:
            raise Exception('Expected at least 3 parts to line')

        itemAttribute: ItemAttributeId = ItemAttributeId(int(parts[0]))
        code: int = int(parts[1])
        value: str = str(parts[2]).strip('\"')

        if ItemAttributeId.Type == itemAttribute:
            self.type = DiscType(code)
        elif ItemAttributeId.Name == itemAttribute:
            self.name = value
        elif ItemAttributeId.MetadataLanguageCode == itemAttribute:
            self.meta_language_code = value
        elif ItemAttributeId.MetadataLanguageName == itemAttribute:
            self.meta_language_name = value
        elif ItemAttributeId.TreeInfo == itemAttribute:
            self.tree_info = value
        elif ItemAttributeId.PanelTitle == itemAttribute:
            self.panel_title = ItemInfo(code)
        elif ItemAttributeId.VolumeName == itemAttribute:
            self.volume_name = value
        elif ItemAttributeId.OrderWeight == itemAttribute:
            self.order_weight = int(value)
        else:
            raise Exception(
                'Unknown Item Attribute Id: {itemAttributeId}, input: {input}'
                    .format(itemAttributeId=itemAttribute, input=input))

    def setTitleAttribute(self, input: str) -> None:
        """
        TINFO:0,2,0,"Friends Season 10 Disc 1"
        TINFO:0,8,0,"4"
        TINFO:0,9,0,"0:22:56"
        TINFO:0,10,0,"2.9 GB"
        TINFO:0,11,0,"3130791936"
        TINFO:0,16,0,"00080.mpls"
        TINFO:0,25,0,"1"
        TINFO:0,26,0,"71"
        TINFO:0,27,0,"Friends_Season_10_Disc_1_t00.mkv"
        TINFO:0,28,0,"eng"
        TINFO:0,29,0,"English"
        TINFO:0,30,0,"Friends Season 10 Disc 1 - 4 chapter(s) , 2.9 GB"
        TINFO:0,31,6120,"<b>Title information</b><br>"
        TINFO:0,33,0,"0"

        :param input:
        :return:
        """
        parts: List[str] = str(input).split(',', maxsplit=3)
        title_index: int = int(parts[0])
        attribute_id: ItemAttributeId = ItemAttributeId(int(parts[1]))
        code: int = int(parts[2])
        value: str = str(parts[3]).strip('\"')

        if self.titles.get(title_index) == None:
            self.titles[title_index] = Title(title_index)

        self.titles.get(title_index).setAttribute(attributeId=attribute_id, code=code, value=value)
