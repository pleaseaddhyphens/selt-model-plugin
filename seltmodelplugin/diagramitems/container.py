from gaphor import UML
from seltmodelplugin import c4model
from gaphor.diagram.presentation import ElementPresentation, Named, text_name
from gaphor.diagram.shapes import Box, CssNode, Text, draw_border
from gaphor.diagram.support import represents
from gaphor.UML.compartments import text_stereotypes


@represents(c4model.C4Container)
class C4ContainerItem(Named, ElementPresentation):
    def __init__(self, diagram, id=None):
        super().__init__(diagram, id)

        self.watch("subject.name")
        self.watch("subject[C4Container].description")
        self.watch("subject.appliedStereotype.classifier.name")

        self.watch("children", self.update_shapes)

    def update_shapes(self, event=None):
        self.shape = Box(
            text_stereotypes(
                self,
                lambda: [self.diagram.gettext("profile")]
                if isinstance(self.subject, UML.Profile)
                else [],
            ),
            text_name(self),
            CssNode(
                "technology",
                self.subject,
                Text(
                    text=lambda: self.subject.technology
                    and f"[{self.subject.technology}]"
                ),
            ),
            *(
                ()
                if self.children
                else (
                    CssNode(
                        "description",
                        self.subject,
                        Text(text=lambda: self.subject.description or ""),
                    ),
                )
            ),
            draw=draw_border,
        )
