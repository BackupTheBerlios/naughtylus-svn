"""
commander-like file manager for GNOME with no name yet (clfmfgwnny)

Copyright (C) 2004 Krzysztof Luks <kluks@iq.pl>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

See COPYING file for details.

$Id$

"""

import new, types

import pygtk
pygtk.require('2.0')

import gtk
import gnome
import gtk.glade
import gnome.ui

import Config
import FileList

class MainWindow:
    def __init__(self):
        gnome.init('gnommander', Config.VERSION)
        self.widgetTree = gtk.glade.XML(Config.DATADIR + '/yaccfg.glade')

        self.leftTree = None
        self.rightTree = None
	
        callbacks = {}
        class_methods = self.__class__.__dict__
        for method_name in class_methods.keys():
            method = class_methods[method_name]
            if type(method) == types.FunctionType:
                callbacks[method_name] = new.instancemethod(
                        method, self, self.__class__)
        self.widgetTree.signal_autoconnect(callbacks)

        self.window = self.widgetTree.get_widget('yaccfg')
        self.notebook = self.widgetTree.get_widget('main_notebook')
        self.leftScroll = self.widgetTree.get_widget('left_scroll')
        self.rightScroll = self.widgetTree.get_widget('right_scroll')
        self.leftLabel = self.widgetTree.get_widget('left_label')
        self.rightLabel = self.widgetTree.get_widget('right_label')
        self.hPaned = self.widgetTree.get_widget('main_hpaned')
        self.commandEntry = self.widgetTree.get_widget('command_entry')

        self.initPanels()
        gtk.main()
		
    def initPanels(self):
        self.leftTree = FileList.FileList('/', self.commandEntry, self.leftLabel, self.rightTree)
        self.rightTree = FileList.FileList('/', self.commandEntry, self.rightLabel, self.leftTree)
        self.leftScroll.add(self.leftTree)
        self.rightScroll.add(self.rightTree)
        self.leftTree.show()
        self.rightTree.show()
        
    def handleGtkEvents(self):
        while gtk.events_pending():
            gtk.main_iteration()

    def on_yaccfg_destroy(self, widget):
        gtk.main_quit(0)

    def on_button_F10_clicked(self, widget):
        gtk.main_quit(0)

