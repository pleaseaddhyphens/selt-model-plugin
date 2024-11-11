from datetime import datetime
from pathlib import Path
import logging
import os

from gaphor.core import gettext
from seltmodelplugin import c4model
from gaphor.core import Transaction
from gaphor.diagram.propertypages import (
    NamePropertyPage,
    PropertyPageBase,
    PropertyPages,
    handler_blocking,
    new_resource_builder,
    unsubscribe_all_on_destroy,
)
from gaphor.event import Notification
from gaphor.services.componentregistry import ComponentLookupError, ComponentRegistry
from gaphor.transaction import Transaction
from gaphor.ui.errorhandler import error_handler
from gaphor.ui.filedialog import open_file_dialog
from gaphor.ui.filemanager import FileManager

logger = logging.getLogger(__name__)


new_builder = new_resource_builder("seltmodelplugin")


PropertyPages.register(c4model.C4Dependency, NamePropertyPage)


@PropertyPages.register(c4model.C4Container)
@PropertyPages.register(c4model.C4Person)
class DescriptionPropertyPage(PropertyPageBase):
    order = 14

    def __init__(self, subject: c4model.C4Container | c4model.C4Person, event_manager):
        super().__init__()
        assert subject
        self.subject = subject
        self.event_manager = event_manager
        self.watcher = subject.watcher()

    def construct(self):
        builder = new_builder(
            "description-editor",
            "description-text-buffer",
        )
        subject = self.subject

        description = builder.get_object("description")

        buffer = builder.get_object("description-text-buffer")
        if subject.description:
            buffer.set_text(subject.description)

        @handler_blocking(buffer, "changed", self._on_description_changed)
        def text_handler(event):
            if not description.props.has_focus:
                buffer.set_text(event.new_value)

        self.watcher.watch("description", text_handler)

        return unsubscribe_all_on_destroy(
            builder.get_object("description-editor"), self.watcher
        )

    def _on_description_changed(self, buffer):
        with Transaction(self.event_manager):
            self.subject.description = buffer.get_text(
                buffer.get_start_iter(), buffer.get_end_iter(), False
            )


@PropertyPages.register(c4model.seltFile)
class FilePropertyPage(PropertyPageBase):
    """Specify file and allow opening it in file explorer."""

    def __init__(self, subject, event_manager, component_registry=ComponentRegistry):
        self.subject = subject
        self.event_manager = event_manager
        self.component_registry = component_registry
        self.watcher = subject and subject.watcher()
        self.builder = None

        try:
            file_manager = self.component_registry.get(FileManager, "file_manager")
            self.model_dir = (
                file_manager.filename.parent if file_manager.filename else Path.cwd()
            )
        except ComponentLookupError:
            self.model_dir = Path.cwd()

    def construct(self):
        subject = self.subject

        if not subject:
            return

        self.builder = new_builder(
            "file-editor",
            signals={
                "select-file": (self._on_select_file_clicked,),
                "show-in-explorer": (self._on_show_in_explorer_clicked,),
                "update-changes": (self._on_update_changes_clicked,),
            },
        )

        file_path_label = self.builder.get_object("file-path-label")
        last_modified_label = self.builder.get_object("last-modified-label")
        current_modified_label = self.builder.get_object("current-modified-label")

        try:
            if self.subject:
                file_path = self.subject.filePath
            else:
                file_path = None
        except AttributeError as e:
            # Log or handle the AttributeError in case it still occurs
            logger.error(f"Error accessing filePath: {e}")
            file_path = None

        if file_path:
            file_path_label.set_text(file_path or "No file selected")

            full_file_path = self.model_dir / file_path
            if full_file_path.exists():
                current_mtime = full_file_path.stat().st_mtime
                current_modified_label.set_text(
                    datetime.fromtimestamp(current_mtime).strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                current_modified_label.set_text("File not found")

            last_mtime = self.subject.lastModified

            if last_mtime:
                last_modified_label.set_text(
                    datetime.fromtimestamp(last_mtime).strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                last_modified_label.set_text("Unknown")
        else:
            file_path_label.set_text("No file selected")
            last_modified_label.set_text("")
            current_modified_label.set_text("")

        return self.builder.get_object("file-editor")

    def _on_select_file_clicked(self, button):
        open_file_dialog(
            gettext("Select a file from the directory"),
            self.open_file,
            image_filter=False,
            parent=button.get_root(),
            multiple=False,
        )

    def open_file(self, filename):
        selected_file = Path(filename)
        try:
            relative_path = selected_file.relative_to(self.model_dir)
            path = str(relative_path)
        except ValueError:
            path = str(selected_file)

        with Transaction(self.event_manager):
            self.subject.name = str(os.path.basename(path))
            self.subject.filePath = str(path)
            self.subject.lastModified = int(selected_file.stat().st_mtime)

        # Check if builder exists and update the UI to reflect the selected file path
        if self.builder:
            file_path_label = self.builder.get_object("file-path-label")
            file_path_label.set_text(self.subject.filePath)

            last_modified_label = self.builder.get_object("last-modified-label")
            last_modified_label.set_text(
                datetime.fromtimestamp(self.subject.lastModified).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

    def _on_update_changes_clicked(self, button):
        try:
            with Transaction(self.event_manager):
                file_path = Path(self.subject.filePath)
                file_path = self.model_dir / file_path

                # Attempt to retrieve the last modified time
                self.subject.lastModified = int(file_path.stat().st_mtime)

                if self.subject:
                    self.subject.modified = False

                # Update the UI if the builder exists
                if self.builder:
                    last_modified_label = self.builder.get_object("last-modified-label")
                    last_modified_label.set_text(
                        datetime.fromtimestamp(
                            self.subject.lastModified
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    )
        except (FileNotFoundError, OSError) as e:
            # Log the error for debugging
            logger.error(f"File '{file_path}' not found or cannot be accessed: {e}")

            # Trigger a notification to inform the user
            self.event_manager.handle(
                Notification(
                    gettext(
                        f"The system cannot find the file specified:\n{file_path}\n"
                    )
                )
            )

    def _on_show_in_explorer_clicked(self, button):
        # Open the file explorer with filepath
        if self.subject.filePath:
            relative_file_path = Path(self.subject.filePath)
            absolute_file_path = self.model_dir / relative_file_path
            open_file_in_explorer(absolute_file_path)


def open_file_in_explorer(file_path):
    import platform
    import subprocess

    # Ensure the file path is valid
    if file_path.exists():
        if platform.system() == "Windows":
            subprocess.run(f'explorer /select,"{file_path}"', check=False)
        elif platform.system() == "Darwin":
            subprocess.run(["open", "-R", file_path], check=False)
        else:
            subprocess.run(["xdg-open", file_path.parent], check=False)
    else:
        pass