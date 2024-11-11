import os

import pandas as pd
from gi.repository import Gtk

from gaphor import UML
from gaphor.abc import ActionProvider, Service
from gaphor.core import action, gettext

DEBUG = True

WATCHDOG_LIMIT = 15


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
    export_dailog(self)
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

    def shutdown(self):
        """
        Default function to shutdown the plugin.
        """
        self.tools_menu.remove_actions(self)

    def _get_stereotypes(self):
        """
        The function extract all the stereotypes, available in the diagram.

        Returns
        -------
        stereotypes : list[UML.Stereotype]
            A list of the available stereotypes.
        """

        stereotypes = [
            stereotype.name
            for stereotype in self.element_factory.select(UML.Stereotype)
        ]
        return stereotypes

    def _select_filepath(self, _button):
        """
        A callback function, called from the dialog window.

        Parameters
        ----------
        _button : Gtk.Button
            A "Select" button from dialog window.
        """

        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title(gettext("Export diagram to table"))

        def response(dialog, result):
            """
            A callback function, processing gthe path from the folder dialog
            window

            Parameters
            ----------
            dialog : Gtk.FileDialog
                A file dialog to receive the path from.
            result : Gtk.String
                A path from the dialog

            Returns
            -------
            None
            """

            if result.had_error():
                return
            else:
                path = dialog.select_folder_finish(result).get_path()
                file = self.entry.get_buffer().get_text()
                file = os.path.splitext(file)[0]
                if not file:
                    file = "output"
                table = self._export_backend()
                extension = self.extensions[self.extension.get_selected()].get_string()
                if extension == ".csv":
                    table.to_csv(os.path.join(path, file + extension), index=False)
                elif extension == ".xlsx":
                    table.to_excel(os.path.join(path, file + extension), index=False)
                elif extension == ".txt":
                    table.to_string(os.path.join(path, file + extension), index=False)
                else:
                    raise TypeError(
                        f"The file extension '{extension}' is not supported"
                    )

        file_dialog.select_folder(callback=response)
        self.dialog.close()

    def _export_backend(self) -> pd.DataFrame:
        """
        The main function, which converts the diagram to the table.

        Returns
        -------
        table : pd.DataFrame
            A table with all dependencies between choosen types of entities.
        """
        source = self.stereotypes[self.source_option.get_selected()].get_string()
        target = self.stereotypes[self.target_option.get_selected()].get_string()

        # Get all connections
        connections = []
        for dependency in self.element_factory.select(UML.Dependency):
            src = dependency.client
            tgt = dependency.supplier
            if src.appliedStereotype and tgt.appliedStereotype:
                connections.append({"source": src, "target": tgt})

        for association in self.element_factory.select(UML.Association):
            src = association.endType[0]
            tgt = association.endType[1]
            if src.appliedStereotype and tgt.appliedStereotype:
                connections.append({"source": src, "target": tgt})

        # Sort out links, which starts from soucre type of object
        links = []
        for i in range(len(connections)):
            src_type = connections[i]["source"].appliedStereotype[0].classifier[0].name
            if src_type == source:
                links.append(connections[i])

        for _ in range(WATCHDOG_LIMIT):
            if all(
                link["target"].appliedStereotype[0].classifier[0].name == target
                for link in links
            ):
                break
            new_links = []
            for link in links:
                for connection in connections:
                    # Add to list links with required source and target
                    if (
                        connection["target"].appliedStereotype[0].classifier[0].name
                        == target
                        and connection["source"].appliedStereotype[0].classifier[0].name
                        == source
                    ):
                        new_links.append(connection)
                    # Skip connection with an intermediate entity via source-target match
                    if link["target"] == connection["source"]:
                        new_links.append(
                            {"source": link["source"], "target": connection["target"]}
                        )
                    # All other connections are omitted
            # Update links
            links = new_links

        # Export everything
        table = pd.DataFrame(columns=[source, target])
        for i in range(len(links)):
            table.loc[i, :] = [links[i]["source"].name, links[i]["target"].name]

        table.rename(columns={"source": source, "target": target})
        table = table.drop_duplicates()
        return table

    @action(
        name="tableexporter",
        label=gettext("Export diagram to table"),
        tooltip=gettext("Export all the dependencies from the daigram to table"),
    )
    def export_dailog(self):
        """
        An fucntion, that declares the folder dialog widget.
        """

        self.dialog = Gtk.Window.new()
        self.dialog.set_title(gettext("Export daigram to table"))

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            hexpand=False,
            vexpand=False,
        )
        box.props.margin_start = 12
        box.props.margin_end = 12
        box.props.margin_top = 6
        box.props.margin_bottom = 6
        self.dialog.set_child(box)

        self.stereotypes = Gtk.StringList()
        for src in self._get_stereotypes():
            self.stereotypes.append(src)

        source_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=12, hexpand=True
        )
        box.append(source_box)
        source_label = Gtk.Label()
        source_label.set_label("Source stereotype:")
        source_box.append(source_label)

        self.source_option = Gtk.DropDown()
        self.source_option.props.model = self.stereotypes
        source_box.append(self.source_option)

        target_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=12, hexpand=True
        )
        box.append(target_box)
        target_label = Gtk.Label()
        target_label.set_label("Target stereotype:")
        target_box.append(target_label)

        self.target_option = Gtk.DropDown()
        self.target_option.props.model = self.stereotypes
        target_box.append(self.target_option)

        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            hexpand=True,
        )
        box.append(button_box)

        self.entry = Gtk.Entry()
        button_box.append(self.entry)

        self.extension = Gtk.DropDown()
        self.extensions = Gtk.StringList()
        self.extensions.append(".csv")
        self.extensions.append(".xlsx")
        self.extensions.append(".txt")
        self.extension.props.model = self.extensions
        button_box.append(self.extension)

        export_button = Gtk.Button(label="Export...")
        export_button.connect("clicked", self._select_filepath)
        button_box.append(export_button)

        self.dialog.present()
