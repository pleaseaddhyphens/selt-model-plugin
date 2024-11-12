from seltmodelplugin.c4model import seltFile
from gaphor.C4Model.c4model import C4Container
from gaphor.diagram.iconname import get_default_icon_name, icon_name



@icon_name.register(C4Container)
def get_name_for_class(element):
    if element.type == "System":
        return "gaphor-c4-software-system-symbolic"
    elif element.type == "Sub-system":
        return "gaphor-c4-component-symbolic"
    elif element.type == "":
        return "gaphor-block-symbolic"
    return get_default_icon_name(element)

@icon_name.register(seltFile)
def get_file_icon_name(element):
    return "gaphor-send-signal-action-symbolic"
