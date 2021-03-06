#!/usr/bin/env python3
# Simple utility with GUI to copy directory trees, typically between PC and USB
# Copyright (c) 2021, Iwan van der Kleijn (iwanvanderkleijn@gmail.com)
# This is Free Software (BSD). See the file LICENSE.txt
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys, os, os.path
from distutils.dir_util import copy_tree

icon_image = os.path.join(os.path.dirname(__file__), "icon.png")
ui_file = os.path.join(os.path.dirname(__file__), "sneakernet-ui.glade")

if len(sys.argv) == 3:
    pc_dir = sys.argv[1]
    remote_dir = sys.argv[2]
else:
    print("Usage: sneakernet.py «pc» «remote/device»")
    sys.exit(0)

class Handlers:
    def on_pc2usb_button_clicked(self, widget):
        self.copy_folder(f"You want to copy from\n\n{pc_dir}\n\nto\n\n{remote_dir}", pc_dir, remote_dir)

    def on_usb2pc_button_clicked(self, widget):
        self.copy_folder(f"You want to copy from\n\n{remote_dir}\n\nto\n\n{pc_dir}", remote_dir, pc_dir)

    def show_dialog(self, name, message):
        dialog = builder.get_object(name)
        dialog.set_markup(message)
        dialog.run()
        dialog.hide()

    def copy_folder(self, message, origin, destination):
        self.data = {"origin": origin, "destination": destination}
        self.show_dialog("question", message)

    def on_question_response(self, widget, response):
        if response == Gtk.ResponseType.YES:
            try:
                copy_tree(self.data["origin"], self.data["destination"])
            except(Exception) as e:
                self.show_dialog("error", str(e))

builder = Gtk.Builder()
builder.add_from_file(ui_file)

win = builder.get_object("main")
win.set_icon_from_file(icon_image)

builder.connect_signals(Handlers())
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
