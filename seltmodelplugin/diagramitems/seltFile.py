"""FileItem diagram item."""

import os
from pathlib import Path

from seltmodelplugin.c4model import seltFile
from gaphor.diagram.presentation import ElementPresentation, text_name
from gaphor.diagram.shapes import Box, CssNode, Text, stroke
from gaphor.diagram.support import represents

from gaphor.abc import Service

import cairo
from PIL import Image
import logging

logger = logging.getLogger(__name__)

@represents(seltFile)
class seltFileItem(ElementPresentation):
    """Class for handling file attachment presentation with image rendering support."""

    def __init__(self, diagram, id=None):
        super().__init__(diagram, id)

        self.height = 80  # Updated height for image rendering
        self.width = 160  # Updated width for image rendering  

        def get_file_name():
            if self.subject and self.subject.filePath:
                file_path = Path(self.subject.filePath)
                if file_path.suffix.lower() in {
                    '.png', '.jpg', '.jpeg', '.bmp', '.gif', 
                    '.tiff', '.tif', '.webp', '.ppm', '.pgm', 
                    '.pbm', '.pnm'
                }:
                    return ""  # Empty string for supported image formats
                return file_path.name  # File name with extension
            return "No file"  # Render "No file" if filePath doesn't exist

        self.shape = Box(
            CssNode(
                "body",
                None,
                Text(
                    text=get_file_name,
                ),
            ),
            draw=self.draw_content,
        )
        
        self.watch("subject[seltFile].filePath")  # Watch for changes to filePath
        self.watch("subject[seltFile].modified")  # Watch for changes to modified flag



    def draw_content(self, box, context, bounding_box):
        cr = context.cairo
        x, y, w, h = bounding_box
        scale_xy, surface = self.create_image_surface()

        if surface:
            cr.save()
            cr.translate(x, y)
            cr.scale(scale_xy, scale_xy)
            cr.set_source_surface(surface, 0, 0)
            cr.paint()
            cr.restore()
        else:
            # Default behavior if no valid image is found
            self.draw_border(box, context, bounding_box)

    def create_image_surface(self):
        """Create a surface from the attached image file."""
        if not self.subject or not self.subject.filePath:
            logger.warning("No file path found for rendering.")
            return None, None

        file_path = Path(self.subject.filePath)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None, None

        try:
            # Open the image and create a Cairo surface
            image = Image.open(file_path)
            surface = self._from_pil(image)

            # Calculate scaling factors
            surface_width, surface_height = surface.get_width(), surface.get_height()
            width_ratio, height_ratio = self.width / surface_width, self.height / surface_height
            scale_xy = min(width_ratio, height_ratio)

            return scale_xy, surface
        except Exception as e:
            logger.error(f"Error loading image from {file_path}: {e}")
            return None, None

    def _from_pil(self, im, alpha=1.0, format=cairo.FORMAT_ARGB32):
        """Create a Cairo surface from a Pillow Image."""
        if "A" not in im.getbands():
            im.putalpha(int(alpha * 256.0))
        arr = bytearray(im.tobytes("raw", "BGRa"))
        return cairo.ImageSurface.create_for_data(arr, format, im.width, im.height)

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

