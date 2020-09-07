#!/usr/bin/env python3

import os
import gi
import sys
import socket
import platform
import threading
import mechanize
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gio, WebKit2, GLib, GObject, Gdk, Pango, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf
from include.query_handler import QueryService
from time import time, sleep

__version__ = "0.0.8"
__head__ = "Quasium"
__alias__ = "Quasi-CSQ"
__subtitle__ = "Quasium - Eccentric Tensor Labs"

icon_path = os.getcwd() + "/lib/icons/"
proc_path = os.getcwd() + "/proc/"
back_path = os.getcwd() + "/lib/background/def.html"

KALI_URL = "file:///usr/share/kali-defaults/web/homepage.html"

###################################################################################
# Determine Platform
oper_sys = platform.system()
if oper_sys == "Windows":
	print("nt")
elif oper_sys == "Linux":
	print("ln")
elif oper_sys == "MacOS":
	print("mc")
elif oper_sys == "Java":
	print("jv")
else:
	print("fr")

###################################################################################
# Check Python Requirements
if sys.version_info < (3, 0, 0):
	print("Error: {} requires python 3".format(__head__))
	sys.exit(1)

####################################################################################
# About and Credits Class
class About(Gtk.AboutDialog):
	def __init__(self):
		Gtk.AboutDialog.__init__(self)
		self.set_border_width(6)
		self.set_program_name("\n{}\n{}".format(__head__, __subtitle__))
		self.set_version("Version: " + __version__ + "\nQuasi-Counter Strike Quantum")
		self.set_copyright("Eccentric Tensor Labs")
		self.set_comments("Web Browser aimed at anonymity")
		self.set_license("GNU/GPL License")
		self.set_wrap_license(True)
		self.set_website("https://thehackerrealm.blogspot.com")
		self.set_website_label("EccentricTensorLabs")
		self.set_authors(['Anthony "Phystro" Karoki'])
		self.set_artists(['Anthony "PhyTensor" Karoki', 'Thismaker'])
		self.set_documenters(['Simple To Use', 'KISS', 'Betelgeuse'])

		logoimage = Gtk.Image()
		logoimage.set_from_file(icon_path + "PhyIcon.svg")
		logop = logoimage.get_pixbuf()
		logop = logop.scale_simple(96, 96, GdkPixbuf.InterpType.BILINEAR)

		self.set_logo(logop)

#######################################################################################
# Settings Class

#######################################################################################
# Manual Class

########################################################################################
# Browser Tabs Class
class BrowserTab(Gtk.VBox):
	def __init__(self, addr=None):
		Gtk.VBox.__init__(self)

		#########Toolbar############################
		self.tabtoolbar = Gtk.Toolbar()
		self.tabtoolbar.set_icon_size(Gtk.IconSize.MENU)
		self.tabtoolbar.set_show_arrow(True)
		#########Tab Web View#######################
		self.webview = WebKit2.WebView()
		self.webview.set_opacity(1.0)
		
		#########Toolbar Items######################
		# Previous Page
		self.previmage = Gtk.Image.new_from_icon_name("go-previous", Gtk.IconSize.MENU)
		#self.previmage.set_from_file(icon_path + "prev_image.png")
		self.goprev = Gtk.ToolButton()
		self.goprev.set_icon_widget(self.previmage)
		self.goprev.set_tooltip_text("Previous Page")
		self.tabtoolbar.insert(self.goprev, 0)
		# Next Page
		self.nextimage = Gtk.Image.new_from_icon_name("go-next", Gtk.IconSize.MENU)
		#self.nextimage.set_from_file(icon_path + "next_image.png")
		self.gonext = Gtk.ToolButton()
		self.gonext.set_icon_widget(self.nextimage)
		self.gonext.set_tooltip_text("Next Page")
		self.tabtoolbar.insert(self.gonext, 1)
		# Refresh
		self.refimage = Gtk.Image.new_from_icon_name("view-refresh", Gtk.IconSize.MENU)
		# self.refimage.set_from_file(icon_path + "refresh_image.png")
		self.goref = Gtk.ToolButton()
		self.goref.set_icon_widget(self.refimage)
		self.goref.set_tooltip_text("Refresh/Reload Page")
		self.tabtoolbar.insert(self.goref, 2)
		# Stop Loading
		self.stopimage = Gtk.Image.new_from_icon_name("process-stop", Gtk.IconSize.MENU)
		# self.stopimage.set_from_file(icon_path + "stop_image.png")
		self.gostop = Gtk.ToolButton()
		self.gostop.set_icon_widget(self.stopimage)
		self.gostop.set_tooltip_text("Stop Loading Present Page")
		self.gostop.set_opacity(0.3)
		self.tabtoolbar.insert(self.gostop, 3)
		# Home Page
		self.homeimage = Gtk.Image.new_from_icon_name("go-home", Gtk.IconSize.MENU)
		#self.homeimage.set_from_file(icon_path + "home_image.png")
		self.gohome = Gtk.ToolButton()
		self.gohome.set_icon_widget(self.homeimage)
		self.tabtoolbar.insert(self.gohome, 4)
		# Spinner
		self.spinner = Gtk.Spinner()
		self.spinner.set_tooltip_text("Page Loading...")
		self.spinner_container = Gtk.ToolItem()
		self.spinner_container.add(self.spinner)
		self.tabtoolbar.insert(self.spinner_container, 5)
		# Search Bar
		self.toolitem_searchbar = Gtk.ToolItem()
		self.url_bar = Gtk.Entry()
		self.url_bar.set_has_frame(True)
		self.url_bar.set_icon_activatable(Gtk.EntryIconPosition.PRIMARY, True)
		self.toolitem_searchbar.set_expand(True)
		icon_name = "system-search-symbolic"
		self.url_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_name)
		self.url_bar.set_placeholder_text("Search with DuckDuckGo or Enter Address")
		self.toolitem_searchbar.add(self.url_bar)
		# self.click_search()
		self.tabtoolbar.insert(self.toolitem_searchbar, 6)
		# Downloads
		self.downimage = Gtk.Image()
		self.downimage.set_from_file(icon_path + "download_image.png")
		self.godown = Gtk.ToolButton()
		self.godown.set_icon_widget(self.downimage)
		self.tabtoolbar.insert(self.godown, 7)
		# Settings
		self.setimage = Gtk.Image()
		self.setimage.set_from_file(icon_path + "icon-fix.png")
		self.goset = Gtk.ToolButton()
		self.goset.set_icon_widget(self.setimage)
		self.tabtoolbar.insert(self.goset, 8)
		#########Packing#############################
		self.pack_start(self.tabtoolbar, 0, 0, 0)
		self.pack_start(self.webview, 1, 1, 0)

		self.show_all()
########################################################################################
# Main Window Browser
class MainWindow(Gtk.Window):
	def __init__(self, addr=None):
		Gtk.Window.__init__(self)
		# MainWindow Settings - (permanent)
		self.set_default_size(1100, 660)
		self.set_border_width(0)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_resizable(True)
		self.activate_focus()
		self.set_icon_from_file(icon_path + "PhyIcon.svg")
		self.set_default_icon_from_file(icon_path + "PhyIcon.svg")

		#HeaderBar
		self.headerbar = Gtk.HeaderBar(spacing=0)
		self.headerbar.set_border_width(0)
		self.headerbar.set_title(__head__)
		self.headerbar.set_subtitle(__subtitle__)
		self.headerbar.set_show_close_button(True)
		self.headerbar.set_decoration_layout("icon,menu:minimize,maximize,close")
		self.set_titlebar(self.headerbar)

		# About
		self.about_image = Gtk.Image()
		self.about_image.set_from_file(icon_path + "icon-cloud.png")
		self.about_button = Gtk.ToolButton()
		self.about_button.set_icon_widget(self.about_image)
		self.about_button.set_tooltip_text("About Quasi-CSQ")
		self.about_button.connect("clicked", self.show_about)
		self.headerbar.add(self.about_button)
		# Close Tab
		self.close_tab_image = Gtk.Image()
		self.close_tab_image.set_from_file(icon_path + "close_tab.png")
		self.close_tab_button = Gtk.ToolButton()
		self.close_tab_button.set_icon_widget(self.close_tab_image)
		self.close_tab_button.set_tooltip_text("Close Current Tab")
		self.close_tab_button.connect("clicked", self.close_current_tab)
		self.headerbar.add(self.close_tab_button)
		# Open New Tab
		self.add_tab_image = Gtk.Image()
		self.add_tab_image.set_from_file(icon_path + "add_tab.png")
		self.add_tab_button = Gtk.ToolButton()
		self.add_tab_button.set_icon_widget(self.add_tab_image)
		self.add_tab_button.set_tooltip_text("Open New Blank Tab")
		self.add_tab_button.connect("clicked", self.open_new_tab)
		self.headerbar.add(self.add_tab_button)
		# Fullscreen
		self.full_icon = Gtk.Image.new_from_icon_name("view-fullscreen", Gtk.IconSize.MENU)
		self.fullscreen_btn = Gtk.ToolButton.new(self.full_icon)
		self.fullscreen_btn.set_tooltip_text("Activate Fullscreen Mode")
		self.fullscreen_btn.connect("clicked", self.fullscreen_callback)
		self.headerbar.pack_end(self.fullscreen_btn)
		# Notebook
		self.notebook = Gtk.Notebook()
		self.notebook.set_group_name("Quasium")
		self.notebook.set_border_width(0)
		self.notebook.set_scrollable(True)
		self.notebook.set_show_tabs(True)
		self.notebook.set_show_border(True)
		self.notebook.popup_enable()
		self.add(self.notebook)


		#############SMART#########################################

		#############Splash Screen#################################

		#################Start Browser#############################
		"""0 = Blank, 1 = Default, 2 = Previous Session"""
		with open(proc_path + "init_page", "r") as f:
			open_mode = str(f.read())
			f.close()
		if open_mode == ("0\n"):
			if addr == None:
				self.open_new_tab(addr=None)
			elif addr != None:
				self.open_new_tab(addr=addr)
		# elif open_mode == "1\n":
		# 	self.open_new_tab(addr=deff)
		# elif open_mode == "2\n":
		# 	self.open_previous_tabs()

		##################SIGNALS##################################
		self.connect("key-press-event", self.key_pressed)
		# self.connect("destroy", self.exit)

	##########Tab Label Styling##########################
	def tablbl(self, text):
		lbl = Gtk.Label(label=text)
		lbl.set_ellipsize(Pango.EllipsizeMode.END)
		lbl.set_tooltip_text(text)
		lbl.set_pattern("_")
		lbl.set_selectable(False)
		lbl.set_track_visited_links(True)
		lbl.set_width_chars(21)
		return lbl
	##########Tab Widgets and Callbacks##############
	def tabcalls(self):
		# Current Tab Widgets/Features
		self.tabwebview = self.notebook.get_nth_page(self.notebook.get_current_page()).webview
		self.prev = self.notebook.get_nth_page(self.notebook.get_current_page()).goprev
		self.forward = self.notebook.get_nth_page(self.notebook.get_current_page()).gonext
		self.refresh = self.notebook.get_nth_page(self.notebook.get_current_page()).goref
		self.stop = self.notebook.get_nth_page(self.notebook.get_current_page()).gostop
		self.home = self.notebook.get_nth_page(self.notebook.get_current_page()).gohome
		self.spin = self.notebook.get_nth_page(self.notebook.get_current_page()).spinner
		self.search_bar = self.notebook.get_nth_page(self.notebook.get_current_page()).url_bar
		self.view_download = self.notebook.get_nth_page(self.notebook.get_current_page()).godown
		self.app_settings = self.notebook.get_nth_page(self.notebook.get_current_page()).goset
		# Current Tab Widget Callbacks
		self.prev.connect("clicked", self.go_prev)
		self.forward.connect("clicked", self.go_next)
		self.refresh.connect("clicked", self.go_refresh)
		self.stop.connect("clicked", self.stop_loading)
		self.home.connect("clicked", self.go_home)
		self.search_bar.connect("activate", self.go_search)
		# self.view_download.connect("clicked", self.pop_download)
		# self.app_settings.connect("clicked", self.go_settings)

		self.tabwebview.connect("notify::title", self.title_changed)
		self.tabwebview.connect("load-changed", self.url_changed)
	##########Credits and About######################
	def show_about(self, widget):
		credits = About()
		credits.show_all()
	##########Fullscreen Callback####################
	def fullscreen_callback(self, widget=None):
		is_full = self.get_window().get_state() & Gdk.WindowState.FULLSCREEN != 0
		if not is_full:
			self.fullscreen_btn.set_icon_name("view-restore")
			self.fullscreen()
		else:
			self.fullscreen_btn.set_icon_name("view-fullscreen")
			self.unfullscreen()
	############URL Bar Focussing########################
	def focus_url_bar(self, widget=None):
		num = self.notebook.get_current_page()
		self.search_bar.grab_focus()
	###########Zooming In and Out of Web Pages##########
	def zoom_in(self, widget=None):
		zoom_level = self.tabwebview.get_zoom_level()
		zoom_level = float(zoom_level) + 0.01
		self.tabwebview.set_zoom_level(zoom_level)
	def zoom_out(self, widget=None):
		zoom_level = self.tabwebview.get_zoom_level()
		zoom_level = float(zoom_level) - 0.01
		self.tabwebview.set_zoom_level(zoom_level)
	##########Web Navigation############################
	def go_prev(self, widget):
		self.tabwebview.go_back()
		#self.url_changed()
	def go_next(self, widget):
		self.tabwebview.go_forward()
		#self.url_changed()
	def go_home(self, widget):
		self.tabwebview.load_uri(KALI_URL)
		#self.url_changed()
	def go_refresh(self, widget=None):
		# self.tabwebview.reload()	#reload current contents of webpage
		self.tabwebview.reload_bypass_cache()	#reload current contents of webpage without using any cached data
		#self.url_changed()
	def stop_loading(self, widget):
		self.tabwebview.stop_loading()
		#self.url_changed()
	##########Search on Search Bar#####################
	def go_search(self, widget):
		self.tabwebview.grab_focus()
		address = self.search_bar.get_text()
		########################################################
		address = QueryService(address).fix_query()	# validation
		########################################################
		self.search_bar.set_text(address)
		self.tabwebview.load_uri(address)
	##########URL Changes#######################################
	def url_changed(self, widget=None, event=None):
		new_url = self.tabwebview.get_uri()

		if new_url != str("file://" + back_path):
			self.search_bar.set_text(new_url)
		else:
			print ("gotten text: ", self.search_bar.get_text() )
			self.search_bar.set_text("")

		is_loadn = self.tabwebview.is_loading()
		print(new_url)
		#print("url has been called")

		#self.title_changed()


		if is_loadn == True:
			self.spin.start()
			self.refresh.hide()
			self.stop.set_opacity(1.0)
			self.stop.show()
		elif is_loadn == False:
			self.spin.stop()
			self.stop.hide()
			self.stop.set_opacity(0.4)
			self.refresh.show()
			#if new_url.startswith("file:"):
			#	self.title_changed(addr=new_url)
	##########Page Title Changes################################
	def title_changed(self, widget=None, event=None, addr=None):
		current_page = self.notebook.get_current_page()
		page_view = self.notebook.get_nth_page(current_page)
		new_url = self.tabwebview.get_uri()
		num = self.notebook.page_num(page_view)
		print(current_page, num)
		self.page_title = str(self.tabwebview.get_title())

		#self.title_changed()
		
		if addr != None and str(addr).startswith("file:"):
			dir_title = str(addr[8:])
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.tablbl(dir_title))
		if self.page_title == "None":
			self.page_title = new_url
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.tablbl(self.page_title))
		# elif self.page_title == "" and len(self.page_title) == 0:
		# 	self.page_title = new_url
		# 	self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.tablbl(self.page_title))
		else:
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.tablbl(self.page_title))
	##########Moving, Dragging, Re-Ordering Tabs########################
	def movable_tabs(self, widget=None):
		current_page = self.notebook.get_current_page()
		self.notebook.set_tab_reorderable(self.notebook.get_nth_page(current_page), True)
		self.notebook.set_tab_detachable(self.notebook.get_nth_page(current_page), True)
	###########Opening New Tab#######################
	def open_new_tab(self, widget=None, addr=None):
		current_page = self.notebook.get_current_page()
		self.browser_page = BrowserTab()
		self.notebook.insert_page(self.browser_page, self.tablbl("New Tab"), current_page + 1)
		self.notebook.set_current_page(current_page + 1)
		self.tabcalls()
		self.movable_tabs()
		if addr == None:
			naddr = "file://" + back_path 				# "file://" + icon_path + "../background/def.html"
			self.tabwebview.load_uri(naddr)
			self.search_bar.set_text("")
			self.search_bar.grab_focus()
		elif addr != None:
			naddr = str(addr)
			self.tabwebview.load_uri(naddr)
			self.tabwebview.grab_focus()
	###########Closing Current Tab###################
	def close_current_tab(self, widget=None):
		if self.notebook.get_n_pages() == 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.WARNING,
				buttons=Gtk.ButtonsType.OK_CANCEL, text="Confirm Exit")
			dialog.format_secondary_text("Well, this is really sad! Closing down {}? Are you sure?\n\n\t\t\t\tProceed with shutdown...?".format(__head__))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				dialog.destroy()
				current_page = self.notebook.get_current_page()
				self.notebook.remove_page(current_page)
				self.close()
			elif response == Gtk.ResponseType.CANCEL:
				dialog.destroy()
				return
		else:
			self.notebook.remove_page(self.notebook.get_current_page())
	###########EXIT##################################
	def exit(self, widget=None):
		if self.notebook.get_n_pages() > 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION,
				buttons=Gtk.ButtonsType.YES_NO, text="Confirm Exit")
			dialog.format_secondary_text("\t\t\t\t\tWell, this is sad to see you go.\n\nThis will close down {} tabs!. Please confirm decision to close down {}\n\n\t\t\t\t\tProceed with shutdown...?".format(self.notebook.get_n_pages(), __head__))
			response = dialog.run()
			if response == Gtk.ResponseType.YES:
				dialog.destroy()
				self.close()
			elif response == Gtk.ResponseType.NO:
				dialog.destroy()
				return
		else:
			print("Exiting...")
			self.close()
	###########Key Pressed###########################
	def key_pressed(self, widget, event):
		modifiers = Gtk.accelerator_get_default_mod_mask()
		mapping = {
			Gdk.KEY_f: self.fullscreen_callback,
			Gdk.KEY_l: self.focus_url_bar,
			Gdk.KEY_z: self.zoom_in,
			Gdk.KEY_x: self.zoom_out,
		}
		if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK and event.keyval in mapping:
			mapping[event.keyval]()

if __name__=="__main__":
	try:
		addr = sys.argv[1]
	except:
		addr = None
	else:
		pass
	finally:
		try:
			browser = MainWindow(addr)
			browser.connect("destroy", Gtk.main_quit)
			browser.show_all()
			Gtk.main()
		except KeyboardInterrupt:
			print("\n[-] Shutdown Ordered!\nClosing...")
