"""The action definition for the selt Model toolbox."""

from functools import partial

from gaphas.item import SE

from gaphor.C4Model import c4model, diagramitems
from seltmodelplugin import c4model as seltmodel, diagramitems as seltdiagramitems

from gaphor.diagram.diagramtoolbox import (
    DiagramType,
    DiagramTypes,
    ElementCreateInfo,
    ToolboxDefinition,
    ToolDef,
    ToolSection,
    new_item_factory,
    general_tools
)
from gaphor.i18n import gettext, i18nize
from gaphor.UML.actions.actionstoolbox import actions
from gaphor.UML.classes.classestoolbox import classes
from gaphor.UML.interactions.interactionstoolbox import interactions
from gaphor.UML.states.statestoolbox import states
from gaphor.UML.toolboxconfig import default_namespace, namespace_config
from gaphor.UML.uml import (
    Activity,
    Class,
    Component,
    DataType,
    Enumeration,
    Interaction,
    Package,
    PrimitiveType,
    StateMachine,
)


def software_system_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "System"
    subject.name = new_item.diagram.gettext("New System")


def container_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Sub-system"
    subject.name = new_item.diagram.gettext("New sub-system")




def component_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Component"
    subject.name = new_item.diagram.gettext("New Component")

def uniblock_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Type"
    subject.name = new_item.diagram.gettext("New uniblock")

    


c4 = ToolSection(
    gettext("C4 Model"),
    (
        ToolDef(
            "c4-person",
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
            "c4-software-system",
            gettext("System"),
            "gaphor-c4-software-system-symbolic",
            "<Shift>S",
            new_item_factory(
                diagramitems.C4ContainerItem,
                c4model.C4Container,
                config_func=software_system_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "c4-container",
            gettext("Sub-system"),
            "gaphor-c4-container-symbolic",
            "<Shift>N",
            new_item_factory(
                diagramitems.C4ContainerItem,
                c4model.C4Container,
                config_func=container_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "c4-component",
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
            "selt-uniblock",
            gettext("Uniblock"),
            "gaphor-block-symbolic",
            "U",
            new_item_factory(
                diagramitems.C4ContainerItem,
                c4model.C4Container,
                config_func=uniblock_config,
            ),
            handle_index=SE,
        ),

        ToolDef(
            "c4-dependency",
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
            "<Shift>f",
            new_item_factory(seltdiagramitems.seltFileItem, seltmodel.seltFile),
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
    DiagramType("des", i18nize("New decision diagram"), (c4,)),
)

c4model_element_types = (
    ElementCreateInfo("activity", i18nize("New Activity"), Activity, (Package,)),
    ElementCreateInfo(
        "interaction", i18nize("New Interaction"), Interaction, (Package,)
    ),
    ElementCreateInfo(
        "statemachine", i18nize("New State Machine"), StateMachine, (Package,)
    ),
    ElementCreateInfo("class", i18nize("New Class"), Class, (Package,)),
    ElementCreateInfo("component", i18nize("New Component"), Component, (Package,)),
    ElementCreateInfo("datatype", i18nize("New Data Type"), DataType, (Package,)),
    ElementCreateInfo(
        "enumeration", i18nize("New Enumeration"), Enumeration, (Package,)
    ),
    ElementCreateInfo(
        "primitive", i18nize("New Primitive Type"), PrimitiveType, (Package,)
    ),
    ElementCreateInfo("person", i18nize("New Person"), c4model.C4Person, (Package,)),
)