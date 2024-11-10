"""FileItem diagram item."""

import os

from seltModelPlugin.c4model import seltFile
from gaphor.diagram.presentation import ElementPresentation, text_name
from gaphor.diagram.shapes import Box, CssNode, Text, stroke
from gaphor.diagram.support import represents



@represents(seltFile)
class seltFileItem(ElementPresentation):
    """Class is used to handle file attachment feature presentation"""

    def __init__(self, diagram, id=None):
        super().__init__(diagram, id)

        self.height = 50
        self.width = 100

        # Define the shape to resemble a file icon with text and border
        self.shape = Box(
            CssNode(
                "body",
                None,
                # Display the file path or name on the icon
                Text(
                    text=lambda: os.path.basename(self.subject.filePath)
                    if self.subject.filePath
                    else "No file",
                ),
            ),
            draw=self.draw_border,
        )

        self.watch("subject[seltFile].filePath")  # Watch for changes for filePath
        self.watch("subject[seltFile].modified")  # Watch for changes for filePath

    def draw_border(self, box, context, bounding_box):
        cr = context.cairo
        x, y, w, h = bounding_box
        _, padding_right, _, padding_left = context.style.get("padding", (4, 16, 4, 4))
        ear = max(padding_right - padding_left, padding_left)
        line_to = cr.line_to
        cr.move_to(w - ear, y)
        line_to(w - ear, y + ear)
        line_to(w, y + ear)
        line_to(w - ear, y)
        line_to(x, y)
        line_to(x, h)
        line_to(w, h)
        line_to(w, y + ear)
        stroke(context, fill=True)

        if self.subject and self.subject.modified:
            cr.set_font_size(20)  # Adjust the font size for the exclamation mark
            cr.move_to(
                x + 5, y + 20
            )  # Position the exclamation mark near the top-left corner
            cr.show_text("!")  # Draw the exclamation mark
            cr.stroke()
