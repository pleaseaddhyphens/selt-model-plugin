"""The action definition for the C4 Model toolbox."""

from functools import partial

from gaphas.item import SE

from seltmodelplugin import c4model, diagramitems

from gaphor.diagram.diagramtoolbox import (
    DiagramTypes,
    ElementCreateInfo,
    ToolboxDefinition,
    ToolDef,
    ToolSection,
    general_tools,
    new_item_factory,
    DiagramType
)
from gaphor.i18n import gettext, i18nize
from gaphor.UML.toolboxconfig import default_namespace, namespace_config
from gaphor.UML.uml import (
    Component,
    Package,
)

def component_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Component"
    subject.name = new_item.diagram.gettext("New Component")


c4 = ToolSection(
    gettext("Modeling"),
    (
        ToolDef(
            "selt-person",
            gettext("Person"),
            "gaphor-c4-person-symbolic",
            "P",
            new_item_factory(
                diagramitems.C4PersonItem,
                c4model.C4Person,
                config_func=partial(namespace_config, name=i18nize("Person")),
            ),
            handle_index=SE,
        ),
        ToolDef(
            "с4-component",
            gettext("Component"),
            "gaphor-c4-component-symbolic",
            "<Shift>X",
            new_item_factory(
                diagramitems.C4ContainerItem,
                c4model.C4Container,
                config_func=component_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "selt-dependency",
            gettext("Dependency"),
            "gaphor-dependency-symbolic",
            "d",
            new_item_factory(diagramitems.C4DependencyItem),
            handle_index=0,
                    ),
        ToolDef(
            "toolbox-selt-file",
            gettext("File"),
            "gaphor-send-signal-action-symbolic",
            None,
            new_item_factory(diagramitems.seltFileItem, c4model.seltFile),
        ),
    ),
)


c4model_toolbox_actions: ToolboxDefinition = (
    general_tools,
    c4,
)

c4model_diagram_types: DiagramTypes = (
    DiagramType("stk", i18nize("New stakeholder diagram"), (c4,)),
    DiagramType("use", i18nize("New use-case diagram"), (c4,)),
    DiagramType("pad", i18nize("New component diagram"), (c4,)),
    DiagramType("des", i18nize("New descision diagram"), (c4,)),



)

c4model_element_types = (
    ElementCreateInfo("component", i18nize("New Component"), Component, (Package,)),
    ElementCreateInfo("person", i18nize("New Person"), c4model.C4Person, (Package,)),
)
