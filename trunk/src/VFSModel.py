
"""

zawiera kod z tutoriala i z http://cvs.gnome.org/viewcvs/gnome-python/gnome-python/examples/vfs/shell.py?rev=1.3&view=auto

"""

import pygtk
pygtk.require('2.0')

import os, time, re

import gtk
import gobject
import gnomevfs
import gnome.ui

import Config

class VFSModel(gtk.GenericTreeModel):
    column_types = (gtk.gdk.Pixbuf, str, long, str, str)
    column_names = ['Name', 'Size', 'Mode', 'Last Changed']
    types = ('unknown', 'regular', 'directory', 'fifo', 'socket', 'chardev', 'blockdev', 'symlink')

    def __init__(self, uri = None):
        gtk.GenericTreeModel.__init__(self)

        if uri:
            self.uri = gnomevfs.URI(uri)
        else:
            self.uri = gnomevfs.URI(os.getcwd())
        if str(self.uri)[-1] != '/':
            self.uri = self.uri.append_string('/')

        self.files = {}
        dhandle = gnomevfs.open_directory(self.uri)

        dirs = []
        files = []
        self.fileInfos = {}
        
        for entry in dhandle:
            file = self.uri.resolve_relative(entry.name)
            info = gnomevfs.get_file_info(file, gnomevfs.FILE_INFO_GET_MIME_TYPE)
            self.fileInfos[entry.name] = info
            
            if entry.type == gnomevfs.FILE_TYPE_DIRECTORY:
                dirs.append(entry.name)
            elif entry.type == gnomevfs.FILE_TYPE_SYMBOLIC_LINK:
                # FIXME: check if it points to dir or file
                files.append(entry.name)
            else:
                files.append(entry.name)
        
        dirs = dirs[2:] # getrid of . and ..
        dirs.sort()
        files.sort()
        self.files = dirs + files

        self.iconTheme = gtk.icon_theme_get_default()
        self.iconFactory = gnome.ui.ThumbnailFactory(gnome.ui.THUMBNAIL_SIZE_NORMAL)

    def get_uri(self, path):
        return self.uri.resolve_relative(self.files[path[0]])

    def is_directory(self, path):
        info = self.fileInfos[self.files[path[0]]]
        return self.types[info.type] == 'directory'

    def get_column_names(self):
        return self.column_names

    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY | gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.column_types)

    def on_get_column_type(self, index):
        return self.column_types[index]
    
    def on_get_iter(self, path):
        return self.files[path[0]]
    
    def on_get_path(self, rowref):
        return self.files.index(rowref)
    
    def on_get_value(self, rowref, column):
        # do we have info for this file cached?
        info = self.fileInfos[rowref]
        
        type = None
        try:
            type = self.types[info.type]
        except:
            pass

        mime = None
        try:
            mime = info.mime_type
        except:
            pass
        
        if column is 0:
            uri_str = str(self.uri.resolve_relative(rowref))
            result, flags = gnome.ui.icon_lookup(self.iconTheme, self.iconFactory, uri_str, '', gnome.ui.ICON_LOOKUP_FLAGS_NONE, mime, info)
            if flags != 0:
                print flags
            try:
                pb = self.iconTheme.load_icon(result, 16, gtk.ICON_LOOKUP_NO_SVG)
            except gobject.GError:
                pb = None
            return pb
        elif column is 1:
            nm = info.name
            if type == 'directory':
                nm = '<b>%s</b>' % nm
            return nm
        elif column is 2:
            size = '???'
            try:
                size = info.size
            except:
                pass
            return size
        elif column is 3:
            mode = '???'
            try:
                mode = info.permissions
            except:
                pass
            return mode #oct(stat.S_IMODE(mode))
        elif column is 4:
            mtime = '???'
            try:
                mtime = info.mtime
            except:
                pass
            return time.ctime(mtime)

    def on_iter_next(self, rowref):
        try:
            i = self.files.index(rowref) + 1
            return self.files[i]
        except IndexError:
            return None
    
    def on_iter_children(self, parent):
        if rowref:
            return None
        return self.files[0]
    
    def on_iter_has_child(self, rowref):
        return False

    def on_iter_n_children(self, rowref):
        if rowref:
            return 0
        return len(self.files)
    
    def on_iter_nth_child(self, rowref, n):
        if rowref:
            return None
        try:
            return self.files[n]
        except IndexError:
            return None

    def on_iter_parent(self, child):
        return None

