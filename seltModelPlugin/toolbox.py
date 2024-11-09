"""The action definition for the C4 Model toolbox."""

from functools import partial

from gaphas.item import SE

from gaphor.C4Model import c4model, diagramitems
from gaphor.diagram.diagramtoolbox import (
    DiagramTypes,
    ElementCreateInfo,
    ToolboxDefinition,
    ToolDef,
    ToolSection,
    general_tools,
    new_item_factory,
)
from gaphor.i18n import gettext, i18nize
from gaphor.UML.toolboxconfig import default_namespace, namespace_config
from gaphor.UML.uml import (
    Component,
    Package,
)


def software_system_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Software System"
    subject.name = new_item.diagram.gettext("New Software System")


def container_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Container"
    subject.name = new_item.diagram.gettext("New Container")


def container_database_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Container"
    subject.technology = new_item.diagram.gettext("Database")
    subject.name = new_item.diagram.gettext("New Database")


def component_config(new_item):
    default_namespace(new_item)
    subject = new_item.subject
    subject.type = "Component"
    subject.name = new_item.diagram.gettext("New Component")


c4 = ToolSection(
    gettext("Modeling"),
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
            "c4-dependency",
            gettext("Dependency"),
            "gaphor-dependency-symbolic",
            "d",
            new_item_factory(diagramitems.C4DependencyItem),
            handle_index=0,
        ),
    ),
)


c4model_toolbox_actions: ToolboxDefinition = (
    general_tools,
    c4,
)

c4model_diagram_types: DiagramTypes = ()

c4model_element_types = (
    ElementCreateInfo("component", i18nize("New Component"), Component, (Package,)),
    ElementCreateInfo("person", i18nize("New Person"), c4model.C4Person, (Package,)),
)
