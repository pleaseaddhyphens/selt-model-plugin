import logging
from pathlib import Path

from gaphor.abc import ActionProvider, Service
from gaphor.core import Transaction
from gaphor.core.eventmanager import event_handler
from seltModelPlugin.c4model import seltFile
from gaphor.event import ModelSaved

logger = logging.getLogger(__name__)


class ObserverService(ActionProvider, Service):
    """Monitor changes for the file attached"""

    def __init__(self, event_manager, element_factory):
        self.event_manager = event_manager
        self.element_factory = element_factory
        self.event_manager.subscribe(self.on_model_saved)

    def shutdown(self) -> None:
        self.event_manager.unsubscribe(self.on_model_saved)

    @event_handler(ModelSaved)
    def on_model_saved(self, event: ModelSaved) -> None:
        self.trigger_function(event.filename)

    def trigger_function(self, filename):
        model_dir = filename.parent if filename else Path.cwd()

        for element in self.element_factory.select(seltFile):
            file_path = Path(element.filePath)
            file_path = model_dir / file_path

            stored_last_modified = int(element.lastModified)

            if file_path.exists():
                # File exists, compare its modification time
                actual_last_modified = int(file_path.stat().st_mtime)

                if stored_last_modified != actual_last_modified:
                    # If the file has been modified, enter a transaction and mark the element as modified
                    try:
                        with Transaction(self.event_manager):
                            element.modified = True
                        logger.info(f"File '{file_path}' modified. Element updated.")
                    except Exception as e:
                        logger.error(
                            f"Error updating element for file '{file_path}': {e}"
                        )
            else:
                logger.warning(
                    f"File '{file_path}' not found. Marking element as modified."
                )

                try:
                    with Transaction(self.event_manager):
                        element.modified = True
                except Exception as e:
                    logger.error(
                        f"Failed to update element for missing file '{file_path}': {e}"
                    )
