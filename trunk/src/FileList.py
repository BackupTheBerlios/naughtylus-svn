
import os

import pygtk
pygtk.require('2.0')

import gtk
import pango
import VFSModel

class FileList(gtk.TreeView):
    def __init__(self, path = None, entry = None, label = None, panel = None):
        self.__gobject_init__()

        if path is None:
            path = os.getcwd()

        model = VFSModel.VFSModel(path)

        column_names = model.get_column_names()
        self.columns = [None] * len(column_names)
        
        iconpb = gtk.CellRendererPixbuf()
        iconpb.set_property('xalign', 0.0)
        
        self.columns[0] = gtk.TreeViewColumn(column_names[0], iconpb, pixbuf = 0)
        cell = gtk.CellRendererText()
        cell.set_property('xalign', 0.0)
        
        self.columns[0].pack_end(cell, expand = True)
        self.columns[0].add_attribute(cell, 'markup', 1)
        font = pango.FontDescription('courier 10')
        cell.set_property('font-desc', font)
        
        self.append_column(self.columns[0])
        for n in range(1, len(column_names)):
            cell = gtk.CellRendererText()
            cell.set_property('xalign', 0.0)
            font = pango.FontDescription('courier 10')
            cell.set_property('font-desc', font)
            self.columns[n] = gtk.TreeViewColumn(column_names[n], cell, text = n + 1)
            self.append_column(self.columns[n])

        # set properties for columns
        for column in self.columns:
            column.set_property('expand', True)
            #column.set_property('resizable', True) # this sucks as hell
            #column.set_property('sizing', gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.connect('row_activated', self.on_row_activated)
        self.connect('key_press_event', self.on_key_press_event)
        self.connect('size-allocate', self.setColumnWidths)
        
        #self.set_property('fixed-height-mode', gtk.TRUE)
        self.set_property('enable-search', gtk.TRUE)
        self.set_property('search-column', 0)
        
        self.set_model(model)
        
        self.commandEntry = entry
        if panel is None:
            self.otherPanel = self
        else:
            self.otherPanel = self
        self.uriLabel = label

        #self.setColumnWidths()

        self.updateLabel()

    def setColumnWidths(self, widget, allocation):
        context = self.get_pango_context()
        metrics = context.get_metrics(pango.FontDescription('courier 10'))
        char_w = pango.PIXELS(metrics.get_approximate_char_width())

        total_w = allocation.width

        size_w = char_w * 9
        mode_w = char_w * 10
        date_w = char_w * 13
        name_w = total_w - (size_w + mode_w + date_w)

        l = (name_w, size_w, mode_w, date_w)

        print l, total_w, char_w

        for i in range(len(l)):
            self.columns[i].set_property('max-width', l[i] - char_w)
            self.columns[i].set_property('min-width', l[i] - char_w)
            #self.columns[i].set_property('fixed-width', l[i])

    def updateLabel(self):
        if self.uriLabel is not None:
            uri = str(self.get_model().uri)
            self.uriLabel.set_text(uri)

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
            print model.get_uri(selected[0])
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
            self.updateLabel()

    def goUp(self):
        parent = self.get_model().uri.parent
        if parent is not None:
            newModel = VFSModel.VFSModel(str(parent))
            self.set_model(newModel)
        

