
import os

import pygtk
pygtk.require('2.0')

import gtk
import VFSModel

class FileList(gtk.TreeView):
    def __init__(self, path = None):
        self.__gobject_init__()

        if path is None:
            path = os.getcwd()

        model = VFSModel.VFSModel(path)

        column_names = model.get_column_names()
        self.columns = [None] * len(column_names)
        iconpb = gtk.CellRendererPixbuf()
        self.columns[0] = gtk.TreeViewColumn(column_names[0], iconpb, pixbuf = 0)
        #self.columns[0] = gtk.TreeViewColumn(column_names[0], iconpb)
        cell = gtk.CellRendererText()
        
        self.columns[0].pack_start(cell, False)
        self.columns[0].add_attribute(cell, 'markup', 1)
        
        self.append_column(self.columns[0])
        for n in range(1, len(column_names)):
            cell = gtk.CellRendererText()
            self.columns[n] = gtk.TreeViewColumn(column_names[n], cell, text = n + 1)
            self.append_column(self.columns[n])

        self.connect("row_activated", self.on_row_activated)
        self.connect("key_press_event", self.on_key_press_event)
        
        self.set_fixed_height_mode = True
        
        self.set_model(model)
        
        self.commandEntry = None
        self.otherPanel = self

    def setOtherPanel(self, panel):
        self.otherPanel = panel

    def setCommandEntry(self, entry):
        self.commandEntry = entry

    def on_key_press_event(self, widget, event):
        keyval = gtk.gdk.keyval_name(event.keyval)
        #print keyval

        if event.string != '':
            if ord(event.string) == 13: # return - find a better way to detect it
                return gtk.FALSE
            self.commandEntry.insert_text(event.string, -1)
            self.commandEntry.grab_focus()
            self.commandEntry.select_region(0, 0)
            self.commandEntry.set_position(-1) # redundant?
            return gtk.TRUE
        elif keyval == 'BackSpace':
            # go to parent folder
            self.goUp()
        elif keyval in ('F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'):
            #print 'Funkcyjny', event.string
            selection = self.get_selection()
            model, selected = selection.get_selected_rows()
            print selected
            return gtk.TRUE
        elif keyval == 'Tab':
            self.otherPanel.grab_focus()
            """
            if self.leftTree.is_focus():
                self.rightTree.grab_focus()
            elif self.rightTree.is_focus():
                self.leftTree.grab_focus()
            """
            return gtk.TRUE

    def on_row_activated(self, tree, path, user_data):
        model = self.get_model()

        if model.is_directory(path):
            uri = model.get_uri(path)
            newModel = VFSModel.VFSModel(str(uri))
            self.set_model(newModel)

    def goUp(self):
        parent =self.get_model().uri.parent
        if parent is not None:
            newModel = VFSModel.VFSModel(str(parent))
            self.set_model(newModel)
        

