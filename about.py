from gi.repository import Gtk, AppIndicator3 as AppIndicator, GLib


class DialogAbout(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "About", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Name: WildGuppy 1.0")
        label.set_markup("Name: WildGuppy 1.0 \nDeveloper: Bilegt\n <a href=\"http://www.twitter.com/billyboar\" "
                         "title=\"My Twitter\">My Twitter</a> ")
        box = self.get_content_area()
        box.add(label)
        self.show_all()
