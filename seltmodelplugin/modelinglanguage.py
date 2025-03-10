"""C4 Model Language entrypoint."""

from collections.abc import Iterable

from gaphor.abc import ModelingLanguage
from seltmodelplugin import c4model, diagramitems
from seltmodelplugin.toolbox import (
    c4model_diagram_types,
    c4model_element_types,
    c4model_toolbox_actions,
)
from gaphor.core import gettext
from gaphor.diagram.diagramtoolbox import (
    DiagramType,
    ElementCreateInfo,
    ToolboxDefinition,
)


class seltModelLanguage(ModelingLanguage):
    @property
    def name(self) -> str:
        return gettext("SELT Model")

    @property
    def toolbox_definition(self) -> ToolboxDefinition:
        return c4model_toolbox_actions

    @property
    def diagram_types(self) -> Iterable[DiagramType]:
        yield from c4model_diagram_types

    @property
    def element_types(self) -> Iterable[ElementCreateInfo]:
        yield from c4model_element_types

    def lookup_element(self, name):
        return getattr(c4model, name, None) or getattr(diagramitems, name, None)
