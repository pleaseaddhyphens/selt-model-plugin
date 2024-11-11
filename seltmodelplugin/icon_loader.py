from gi.repository import Gtk, Gdk
import importlib.resources

def init_plugin_icon_theme():
    icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
    plugin_icon_path = importlib.resources.files("seltmodelplugin.icons")
    if icon_theme:
        icon_theme.add_search_path(str(plugin_icon_path))
