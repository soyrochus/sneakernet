#!/usr/bin/env python3
# Simple utility with GUI to copy directory trees, typically between PC and USB
# Copyright (c) 2021, Iwan van der Kleijn (iwanvanderkleijn@gmail.com)
# This is Free Software (BSD). See the file LICENSE.txt

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys, os, os.path
from distutils.dir_util import copy_tree

copy_from_pc_image = os.path.join(os.path.dirname(__file__), "pc2usb.png")
copy_to_pc_image = os.path.join(os.path.dirname(__file__), "usb2pc.png")
icon_image = os.path.join(os.path.dirname(__file__), "icon.png")

if len(sys.argv) == 3:
    pc_dir = sys.argv[1]
    remote_dir = sys.argv[2]
else:
    print("Usage: sneakernet.py «pc» «remote/device»")
    sys.exit(0)

class Sneakernet(Gtk.Window):
    def __init__(self):
        super().__init__(title="Copy data from and to PC")
        self.set_icon_from_file(icon_image)

        #self.set_default_size(150, 100)
        self.set_border_width(10)
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.copy_from_pc = Gtk.Button(label="Copy from PC")
        self.copy_from_pc.set_image(Gtk.Image.new_from_file(copy_from_pc_image))
        self.copy_from_pc.set_always_show_image(True)
        self.copy_from_pc.set_image_position(Gtk.PositionType.TOP)

        self.copy_from_pc.connect("clicked", self.on_copy_from_pc_clicked)
        self.box.pack_start(self.copy_from_pc, True, True, 0)

        self.copy_to_pc = Gtk.Button(label="Copy to PC")
        self.copy_to_pc.set_image(Gtk.Image.new_from_file(copy_to_pc_image))
        self.copy_to_pc.set_always_show_image(True)
        self.copy_to_pc.set_image_position(Gtk.PositionType.TOP)

        self.copy_to_pc.connect("clicked", self.on_copy_to_pc_clicked)
        self.box.pack_start(self.copy_to_pc, True, True, 0)

    def on_copy_from_pc_clicked(self, widget):
        self.copy_folder(f"You want to copy from\n\n{pc_dir}\n\nto\n\n{remote_dir}", pc_dir, remote_dir)

    def on_copy_to_pc_clicked(self, widget):
        self.copy_folder(f"You want to copy from\n\n{remote_dir}\n\nto\n\n{pc_dir}", remote_dir, pc_dir)

    def copy_folder(self, message, origin, destination):
        if self.yes_no_dialog(message) == Gtk.ResponseType.YES:
            try:
                copy_tree(origin, destination)
            except(Exception) as e:
                self.error_dialog(e)

    def yes_no_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=message
        )
        response = dialog.run()
        dialog.destroy()
        return response

    def error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            text=message
        )
        response = dialog.run()
        dialog.destroy()
        return response

win = Sneakernet()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
