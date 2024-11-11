from seltmodelplugin.c4model import C4Container, C4Dependency
from gaphor.diagram.iconname import get_default_icon_name, icon_name


@icon_name.register(C4Container)
def get_name_for_class(element):
    if element.type == "Software System":
        return "gaphor-c4-software-system-symbolic"
    elif element.type == "Component":
        return "gaphor-c4-component-symbolic"
    return get_default_icon_name(element)


@icon_name.register(C4Dependency)
def get_dependency_name(element):
    return "gaphor-dependency-symbolic"
