#!/bin/env python3
import os
import gi
import sys
import socket
import platform
import threading
import mechanize
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gio, WebKit2, GLib, GObject, Gdk, Pango
from gi.repository.GdkPixbuf import Pixbuf
from include.query_handler import QueryService
from time import time, sleep

__version__ = "1.2.1"
__head__ = "QUASI-CSQ"
__title__= "Quasi-CSQ"
__subtitle__= "QUASI-CSQ - Eccentric Tensor Labs"
icon_path = os.getcwd() + "/lib/icons/"
proc_path = os.getcwd() + "/proc/"

###################################################################################
# Data
FILE = "file:///"
HTTP = "http://"
HTTPS = "https://"
KALI_URL = "file:///usr/share/kali-defaults/web/homepage.html"
search_tags = {
	"google":"https://www.google.com/search?q=",
	"duckduckgo":"https://duckduckgo.com/?q=",
	"yandex":"https://yandex.com/search/?text="
}

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
# Check Requirements
if sys.version_info < (3, 0, 0):
	print("Error: {} requires python 3".format(__head__))
	sys.exit(1)

####################################################################################
# Dialogs & Other Windows Class
class About(Gtk.AboutDialog):
	def __init__(self):
		Gtk.AboutDialog.__init__(self)
		### Fix the PixBuf Issue on the logo
		self.set_border_width(6)
		self.set_program_name(__title__+"\nQuasi-Counter Strike Quantum")
		self.set_version("Version: " + __version__)
		self.set_copyright("Eccentric Tensor Labs")
		self.set_comments("Smooth Private Secure Web Browser")
		self.set_license("GNU/GPL License")
		self.set_wrap_license(True)
		self.set_website("https://thehackerrealm.blogspot.com")
		self.set_website_label("ETLabs")
		self.set_authors(['Anthony "Phystro" Karoki'])
		self.set_artists(['Quasar', 'Linux', 'Anthony "Phystro" Karoki'])
		self.set_documenters(['Quaser', 'Omicron', 'Betelguese'])

		logoimage = Gtk.Image()
		logoimage.set_from_file(icon_path + "eglobe.svg")
		logop = logoimage.get_pixbuf()
		self.set_logo(logop)
####################################################################################
# Settings Class and Page
class SettingsTab(Gtk.StackSidebar):
	def __init__(self):
		Gtk.StackSidebar.__init__(self)
		self.set_border_width(0)

		self.show_all()

# Toolbar and ScrolledWindow Class
class BrowserTab(Gtk.VBox):
	def __init__(self):
		Gtk.VBox.__init__(self)
		self.set_border_width(0)
		# Init Toolbar
		self.tabtoolbar = Gtk.Toolbar()
		self.tabtoolbar.set_icon_size(Gtk.IconSize.MENU)
		self.tabtoolbar.set_show_arrow(True)
		self.tabtoolbar.set_hexpand(True)
		#TabWebView Window
		self.webview = WebKit2.WebView()
		self.webview.set_opacity(1.0)
		#Contents
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
		self.click_search()
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

		self.pack_start(self.tabtoolbar, False, False, 0)
		self.pack_start(self.webview, True, True, 0)

		self.show_all()

	def click_search(self):
		self.enter = Gtk.Image()
		self.enter.set_from_file(icon_path + "icong2.png")
		ind = self.enter.get_pixbuf()
		self.url_bar.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, ind)
#####################################################################################
# Main Window Browser
class MainWindow(Gtk.ApplicationWindow):
	def __init__(self, app, addr=None):
		Gtk.Window.__init__(self, title=__title__, application=app)
		# Window
		self.set_default_size(1100, 660)
		self.set_border_width(0)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_resizable(True)
		# self.activate_focus() #activates curretn focused widget within the window
		self.set_icon_from_file(icon_path + "eglobe.svg")
		self.set_default_icon_from_file(icon_path + "eglobe.svg")
		# HeaderBar
		self.headerbar = Gtk.HeaderBar(spacing=0)
		self.headerbar.set_border_width(0)
		self.headerbar.set_title(__head__)
		self.headerbar.set_subtitle(__subtitle__)
		self.headerbar.set_show_close_button(True)
		self.headerbar.set_decoration_layout("icon,menu:minimize,maximize,close")
		self.set_titlebar(self.headerbar)
		# Widgets on Header Bar
		# Fullscreen Icon Button
		full_icon = Gtk.Image.new_from_icon_name("view-fullscreen", Gtk.IconSize.MENU)
		self.fullscreen_btn = Gtk.ToolButton.new(full_icon)
		self.fullscreen_btn.set_tooltip_text("Open in Fullscreen Mode")
		self.fullscreen_btn.set_is_important(True)
		self.headerbar.pack_end(self.fullscreen_btn)
		#self.headerbar.add(self.fullscreen_btn)
		self.fullscreen_btn.set_action_name("win.fullscreen")
		# Fullscreen Action
		fullscreen_action = Gio.SimpleAction.new("fullscreen", None)
		fullscreen_action.connect("activate", self.fullscreen_callback)
		self.add_action(fullscreen_action)
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
		self.add_tab_button.connect("clicked", self.open_blank_tab)
		self.headerbar.add(self.add_tab_button)
		# Notebook
		self.notebook = Gtk.Notebook()
		self.notebook.set_group_name("KAR")
		self.notebook.set_border_width(0)
		self.notebook.set_scrollable(True)
		self.notebook.set_show_tabs(True)
		self.notebook.set_show_border(True)
		self.notebook.popup_enable()
		self.add(self.notebook)

		# Main Browser Box, for toolbar and webview
		if addr != None:
			self.open_web_tab(addr)
		elif addr == None:
			self.open_blank_tab()

		# Signals
		self.tabwebview.connect("notify::title", self.title_changed)
		#self.tabwebview.connect("load-failed", self.url_failed)
		self.tabwebview.connect("load-changed", self.url_changed)
		#self.tabwebview.connect("load-changed", self.url_title_from_path)
		# Shortcut Keys / Key Events
		self.connect("key-press-event", self.key_pressed)
	def setlbl(self, text):
		lbl = Gtk.Label(label=text)
		lbl.set_ellipsize(Pango.EllipsizeMode.END)
		lbl.set_tooltip_text(text)
		lbl.set_pattern("_")
		lbl.set_selectable(False)
		lbl.set_track_visited_links(True)
		lbl.set_width_chars(21)
		return lbl
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
		self.view_download.connect("clicked", self.pop_download)
		self.app_settings.connect("clicked", self.go_settings)
	def show_about(self, widget):
		credits = About()
		credits.show_all()
	def go_prev(self, widget):
		self.tabwebview.go_back()
	def go_next(self, widget):
		self.tabwebview.go_forward()
	def go_home(self, widget):
		self.tabwebview.load_uri(KALI_URL)
	def go_refresh(self, widget=None):
		self.tabwebview.reload()	#reload current contents of webpage
		#self.tabwebview.reload_bypass_cache()	#reload current contents of webpage without using any cached data
	def stop_loading(self, widget):
		self.tabwebview.stop_loading()
	def go_search(self, widget):
		self.tabwebview.grab_focus()
		address = self.search_bar.get_text()
		########################################################
		address = QueryService(address).fix_query()	# validation
		########################################################
		self.search_bar.set_text(address)
		self.tabwebview.load_uri(address)
	def pop_download(self, widget):
		self.pop = Gtk.Popover()
		vbox = Gtk.VBox()
		vbox.pack_start(Gtk.ModelButton(label="Download Page"), 0, 1, 10)
		vbox.pack_start(Gtk.Label(label="<<Under Development!>>"), 0, 1, 10)
		self.pop.add(vbox)
		self.pop.set_position(Gtk.PositionType.BOTTOM)

		self.pop.set_relative_to(widget)
		self.pop.show_all()
		self.pop.popup()
	def go_settings(self, widget):
		current_page = self.notebook.get_current_page()
		self.settings_page = SettingsTab()
		self.notebook.insert_page(self.settings_page, Gtk.Label(label="Browser Settings"), current_page + 1)
		self.notebook.set_current_page(current_page + 1)#self.notebook.get_n_pages() - 1)
		#self.tabcalls()
	def istitle(self, addr):
		num = self.notebook.get_current_page()
		self.page_title = str(self.tabwebview.get_title())
		if self.page_title == "None":
			self.page_title = addr
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.setlbl(self.page_title))#Gtk.Label(label=self.page_title))
		elif self.page_title == "" and len(self.page_title) == 0:
			self.page_title = addr
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.setlbl(self.page_title))#Gtk.Label(label=self.page_title))
		else:
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.setlbl(self.page_title))#Gtk.Label(label=self.page_title))
	def focus_url_bar(self, widget=None):
		num = self.notebook.get_current_page()
		self.search_bar.grab_focus()
	def zoom_in(self, widget=None):
		zoom_level = self.tabwebview.get_zoom_level()
		zoom_level = float(zoom_level) + 0.01
		self.tabwebview.set_zoom_level(zoom_level)
	def zoom_out(self, widget=None):
		zoom_level = self.tabwebview.get_zoom_level()
		zoom_level = float(zoom_level) - 0.01
		self.tabwebview.set_zoom_level(zoom_level)
	def title_changed(self, widget=None, event=None):
		new_url = self.tabwebview.get_uri()
		self.istitle(str(new_url))
	def url_changed(self, widget=None, event=None):
		new_url = self.tabwebview.get_uri()
		#print(self.tabwebview.get_window_properties())
		#self.tabwebview.set_zoom_level(0.5)
		#self.tabwebview.download_uri(new_url)
		self.search_bar.set_text(new_url)
		is_loadn = self.tabwebview.is_loading()
		if is_loadn == True:
			self.spin.show()
			self.spin.start()
			self.refresh.hide()
			self.stop.show()
			self.stop.set_opacity(1.0)
		elif is_loadn == False:
			self.spin.stop()
			self.spin.hide()
			self.stop.hide()
			self.stop.set_opacity(0.4)
			self.refresh.show()
			if new_url.startswith("file:"):
				dir_title = str(new_url[7:])
				self.istitle(dir_title)
		# if self.tabwebview.can_go_back() == True:
		# 	self.prev.show()
		# elif self.tabwebview.can_go_back() == False:
		# 	self.prev.hide()
		# if self.tabwebview.can_go_forward() == True:
		# 	self.forward.show()
		# elif self.tabwebview.can_go_forward() == False:
		# 	self.forward.hide()
	def url_title_from_path(self, widget=None, event=None):
		print("o")
		num = self.notebook.get_current_page()
		url = self.tabwebview.get_uri()
		if str(url).startswith("file:"):
			path = url.split("file://")[1]
			if os.path.isdir(path):
				pt = str(path)
				self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.setlbl(pt))
			elif os.path.isfile(path):
				path = path.split("/")[-1]
				pt = str(path)
				self.notebook.set_tab_label(self.notebook.get_nth_page(num), self.setlbl(pt))
		else:
			pass
	def url_failed(self, webview, url2, sdf, widget=None ):#event=None):
		print("Failed")
	def open_blank_tab(self, widget=None):
		current_page = self.notebook.get_current_page()
		self.bpage = BrowserTab()
		self.notebook.insert_page(self.bpage, Gtk.Label(label="New Tab"), current_page + 1)
		self.notebook.set_current_page(current_page + 1)#self.notebook.get_n_pages() - 1)
		self.tabcalls()
		self.tabwebview.connect("notify::title", self.title_changed)
		#self.tabwebview.connect("load-failed", self.url_failed)
		self.tabwebview.connect("load-changed", self.url_changed)
		#self.tabwebview.connect("load-changed", self.url_title_from_path)
		# Setting Tab as Reoderable and Detachable
		self.notebook.set_tab_reorderable(self.notebook.get_nth_page(current_page), True)
		self.notebook.set_tab_detachable(self.notebook.get_nth_page(current_page), True)
	def open_web_tab(self, addr, widget=None):
		current_page = self.notebook.get_current_page()
		self.cpage = BrowserTab()
		#not Complete
		self.tabcalls()
	def close_current_tab(self, widget=None):
		if self.notebook.get_n_pages() == 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.WARNING,
				buttons=Gtk.ButtonsType.OK_CANCEL, text="Confirm Exit")
			dialog.format_secondary_text("Well, this is really sad! Closing down {}? Are you sure?\n\n\t\t\t\tProceed with shutdown...?".format(__title__))
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
			current_page = self.notebook.get_current_page()
			self.notebook.remove_page(current_page)
	def exit(self, widget=None):
		if self.notebook.get_n_pages() > 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION,
				buttons=Gtk.ButtonsType.YES_NO, text="Confirm Exit")
			dialog.format_secondary_text("\t\t\t\t\tWell, this is sad to see you go.\n\nThis will close down {} tabs!. Please confirm decision to close down {}\n\n\t\t\t\t\tProceed with shutdown...?".format(self.notebook.get_n_pages(), __title__))
			response = dialog.run()
			if response == Gtk.ResponseType.YES:
				dialog.destroy()
				self.close()
			elif response == Gtk.ResponseType.NO:
				dialog.destroy()
				return
		else:
			self.close()
	def fullscreen_callback(self, action=None, parameter=None):
		is_full = self.get_window().get_state() & Gdk.WindowState.FULLSCREEN != 0
		if not is_full:
			self.fullscreen_btn.set_icon_name("view-restore")
			self.fullscreen()
		else:
			self.fullscreen_btn.set_icon_name("view-fullscreen")
			self.unfullscreen()
	def many_window_handler(self, link):
		cwd = os.getcwd()
		command = os.system("python3 {}/quasi-csq-1.2.1.py {}".format(cwd, link))
		if command == 0:
			return False	#successful
	def open_new_window(self, widget=None, addr=None):
		handle = threading.Thread(target=self.many_window_handler, args=(addr,))
		handle.start()
	def key_pressed(self, widget, event):
		modifiers = Gtk.accelerator_get_default_mod_mask()
		mapping = {
			Gdk.KEY_l: self.focus_url_bar,
			Gdk.KEY_z: self.zoom_in,
			Gdk.KEY_x: self.zoom_out,
			Gdk.KEY_r: self.go_refresh,
			Gdk.KEY_t: self.open_blank_tab,
			Gdk.KEY_w: self.close_current_tab,
			Gdk.KEY_f: self.fullscreen_callback,
			Gdk.KEY_n: self.open_new_window,
			Gdk.KEY_q: self.exit,
		}
		if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK and event.keyval in mapping:
			mapping[event.keyval]()

class BrowserApp(Gtk.Application):
	def __init__(self, addr):
		Gtk.Application.__init__(self)
		self.addr = addr

	def do_activate(self):
		win = MainWindow(self, self.addr)
		win.show_all()

if __name__=="__main__":
	try:
		addr = sys.argv[1]
	except:
		addr = None
	else:
		pass
	finally:
		try:
			browser = BrowserApp(addr)
			exit_status = browser.run(sys.argv)
			sys.exit(exit_status)
			# browser = MainWindow(addr)
			# browser.show_all()
			# browser.connect("destroy", Gtk.main_quit)
			# Gtk.main()
		except KeyboardInterrupt:
			print("\n[-] Shutdown Ordered!\nClosing...")