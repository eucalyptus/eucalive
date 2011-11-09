#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2008 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import gtk
import os, string, sys, time
import os.path
import re
import netaddr

from firstboot.config import *
from firstboot.constants import *
from firstboot.functions import *
from firstboot.module import *

import gettext
_ = lambda x: gettext.ldgettext("firstboot", x)
N_ = lambda x: x

class moduleClass(Module):
    def __init__(self):
        Module.__init__(self)
        self.priority = 110
        self.sidebarTitle = N_("Allocate Eucalyptus Subnet")
        self.title = N_("Allocate Eucalyptus Subnet")
        self.icon = "euca.png"

        self._count = 0

    def apply(self, interface, testing=False):
        if testing:
            return RESULT_SUCCESS

        network = self.networkEntry.get_text()
        netmask = self.netmaskEntry.get_text()

        # Determine whether the specified data was valid
        try:
            net = netaddr.IPNetwork('/'.join([ network, netmask ]))
        except Exception, e:
            self._showErrorMessage(_("You must enter a valid network and netmask in dotted decimal form."))
            return RESULT_FAILURE
        
        if not net.is_private():
            # Maybe this is just a warning, but it's usually bad
            self._showErrorMessage(_("You must use a valid RFC 1918 subnet."))

        # Check validity somehow
        if False:
            self._showErrorMessage(_("Network collision detected!"))
            return RESULT_FAILURE

        # TODO:  Ask the user more questions, and use the answers to configure
        # eucalyptus properly.  i.e., this is where the FastStart code comes in.

        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)

        label = gtk.Label(_("You must assign an unused subnet from which eucalyptus can "
                            "allocate IP addresses. Please provide the information "
                            "requested below."))

        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)

        self.networkEntry = gtk.Entry()
        self.netmaskEntry = gtk.Entry()

        self.networkEntry.connect("changed", self.networkEntry_changed)
        self.netmaskEntry.connect("changed", self.netmaskEntry_changed)

        self.vbox.pack_start(label, False, True)

        table = gtk.Table(3, 4)
        table.set_row_spacings(6)
        table.set_col_spacings(6)

        label = gtk.Label(_("_Network:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.networkEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.networkEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5)

        label = gtk.Label(_("Net_mask:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.netmaskEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.netmaskEntry, 1, 2, 1, 2, gtk.SHRINK, gtk.FILL, 5)

        self.vbox.pack_start(table, False)

    def focus(self):
        self.networkEntry.grab_focus()

    def initializeUI(self):
        self.networkEntry.set_text("")
        self.netmaskEntry.set_text("")

    def _waitWindow(self, text):
        # Shamelessly copied from gui.py in anaconda.
        win = gtk.Window()
        win.set_title(_("Please wait"))
        win.set_position(gtk.WIN_POS_CENTER)

        label = gtk.Label(text)

        box = gtk.Frame()
        box.set_border_width(10)
        box.add(label)
        box.set_shadow_type(gtk.SHADOW_NONE)

        win.add(box)
        win.set_default_size(-1, -1)
        return win

    def _showErrorMessage(self, text):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(True)
        rc = dlg.run()
        dlg.destroy()
        return None

    def networkEntry_changed(self, nw_entry):
        network = nw_entry.get_text()

    def netmaskEntry_changed(self, nm_entry):
        netmask = nm_entry.get_text()

