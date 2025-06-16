import json
from pathlib import Path
from collections import defaultdict



from gaphor.C4Model import c4model
from gaphor.abc import ActionProvider, Service
from gaphor.core import action, gettext
from gaphor.ui.filedialog import save_file_dialog


DEBUG = True

JSON_FILTER = [(gettext("JSON files"), "*.json", "application/json")]


class TableExporter(Service, ActionProvider):
    """
    The following class perform diagram conversion to the table in CSV, XLSX or
    TXT format.

    Methods
    -------
    __init__(self, tools_menu=None, main_window=None, element_factory=None)
        Default method - initialize the exporting tool.
    shutdown(self)
        Default method - shutdown the tool
    save_dialog(self, data, title, ext, mime_type, handler)
        Launch the export dialog.
    """

    def __init__(self, tools_menu=None, main_window=None, element_factory=None):
        """
        The class builder

        Parameters
        ----------
        tools_menu=None
            The tool menu from the main program.
        main_window=None
            The main window of the program.
        element_factory=None
            The element factory of the exporting diagram.
        """

        self.tools_menu = tools_menu
        tools_menu.add_actions(self)
        self.main_window = main_window
        self.element_factory = element_factory
        self.filename: Path = Path("export").absolute()


    def shutdown(self):
        """
        Default function to shutdown the plugin.
        """
        self.tools_menu.remove_actions(self)

    def save_dialog(self, data, title, ext, mime_type, handler):
        """
        Use to call save dialog window
        """

        dot_ext = f".{ext}"
        filename = self.filename.with_name("export").with_suffix(dot_ext)

        def save_handler(filename):
            self.filename = filename
            handler(filename, data)

        save_file_dialog(
            title,
            filename,
            save_handler,
            parent=self.main_window.window,
            filters=[
                (gettext("All {ext} Files").format(ext=ext.upper()), dot_ext, mime_type)
            ],
        )

    def _export_backend(self) -> str:
        """
        The main function, which converts the diagram to the json.

        Returns
        -------
        json : str
            A json str with all model data.
        """

        # init dictionary
        elements_connections = defaultdict(lambda: {"sources" : [], "targets" : []})

        
        for dependency in self.element_factory.select(c4model.Dependency):
            src = dependency.client
            tgt = dependency.supplier
            connection_name = dependency.name if dependency.name else ""
            elements_connections[src]["sources"].append({"name": tgt.name, "connection": connection_name})
            elements_connections[tgt]["targets"].append({"name": src.name, "connection": connection_name})



        elements = []
        for e in self.element_factory.select(c4model.C4Container):
            elements.append({
                "Elem. name" : e.name,
                "description": e.description if e.description else "",
                "children" : [child.name for child in e.nestedPackage] if e.nestedPackage else [],
                "type": e.type,
                "presntation":[pres.diagram.name for pres in e.presentation] if e.presentation else [], 
                "connected as target": elements_connections[e]["targets"],
                "connected as source": elements_connections[e]["sources"]
                })


        return json.dumps(elements, indent = 4)

    @action(
        name="tableexporter",
        label=gettext("Export diagram to json"),
        tooltip=gettext("Export all the model to json"),
    )
    def save_json_action(self):
        """
        Handles saving 
        """
        data = self._export_backend()
        self.save_dialog(
            data, gettext("Export model as json"), "json", "application/json", self.save_json
        )

    def save_json(self, file_path,data):
        """
        Writes the json data into file
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            raise TypeError(f"Error saving file: {e}")
  
