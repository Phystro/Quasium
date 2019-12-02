#!/bin/env python3
import gi, os, sys
import mechanize, platform, socket
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gio, WebKit2, GLib, GObject, Gdk

__version__ = "1.0.0"
__head__ = "QUASI-CSQ"
__title__= "QUASI-CSQ - Eccentric Tensor Labs"

###################################################################################
# Data
KALI_URL = "file:///usr/share/kali-defaults/web/homepage.html"

###################################################################################
# Check Requirements
if sys.version_info < (3, 0, 0):
	print("Error: {} requires python 3".format(__head__))
	sys.exit(1)

####################################################################################
# Networking Class
####################################################################################
# Data Handling Class
class PageUtility():
	def __init__(self, query):
		self.query = query
		print(self.query)
		self.browser = mechanize.Browser()

	def get_title(self):
		try:
			page = self.browser.open(self.query)
			print("[+] URL Works")
		except mechanize.URLError:
			print("[-] URL Unable to Connect")
		else:
			#getting tab title
			source = page.read()
			#print(source)
			if bytes("<title>", "utf-8") in source:
				if bytes("rel=icon", "utf-8") and bytes("favicon", "utf-8") in source:
					print("[+] We have a favicon")
				else:
					print("[-] No Favicon")
				st = source.index(bytes("<title>", "utf-8"))
				en = source.index(bytes("</title>", "utf-8"))
				line = source[st + 7:en]
				print("[+] Title: =>", line)
				line = str(line).split("b")[1].split("'")[1]
				page_title = line
				print(page_title)
				return page_title
			elif not "<title>" in source:
				print("[-] No Title")

####################################################################################
# Dialogs Class

####################################################################################
# Browser Tabs Class
class TabWindow(Gtk.VBox):
	def __init__(self):
		Gtk.VBox.__init__(self)
		#Gtk.Window.__init__(self)
		#GObject.threads_init()
		#Gdk.threads_init()
		# self.label = Gtk.Label(label="Karoki")
		# self.add(self.label)
		self.tabpagebox = Gtk.VBox()
		self.add(self.tabpagebox)

		self.tabnotebook = Gtk.Notebook()
		self.tabscrolledwindow = Gtk.ScrolledWindow()
		self.tabwebview = WebKit2.WebView()
		self.tabwebview.load_uri(KALI_URL)
		self.tabscrolledwindow.add(self.tabwebview)

		self.tabtoolbar = Gtk.Toolbar()
		self.tabtoolbar.set_icon_size(Gtk.IconSize.MENU)
		# Previous Page
		self.previmage = Gtk.Image()
		self.previmage.set_from_file("lib/thumbs/prev_image.png")
		self.goprev = Gtk.ToolButton()
		self.goprev.set_icon_widget(self.previmage)
		self.tabtoolbar.insert(self.goprev, 0)

		self.tabpagebox.pack_start(self.tabtoolbar, False, False, 0)
		self.tabpagebox.pack_start(self.tabscrolledwindow, True, True, 0)
		self.show_all()


####################################################################################
# Browser Main Window Class
class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title=__title__)
		self.set_default_size(1100, 660)
		self.set_border_width(0)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_icon_from_file("lib/thumbs/eglobe.svg")

		# Main Widgets used
		self.pagebox = Gtk.VBox(spacing=0)
		self.headerbar = Gtk.HeaderBar()
		self.headerbar.set_title(__head__)
		#self.headerbar.props.title = "Karoki HeaderBar Example"
		self.headerbar.set_subtitle(__title__)
		self.headerbar.set_show_close_button(True)
		self.set_titlebar(self.headerbar)
		self.notebook = Gtk.Notebook()
		self.notebook.set_scrollable(True)
		self.notebook.set_show_tabs(True)
		self.notebook.set_show_border(True)
		self.add(self.notebook)
		self.toolbar = Gtk.Toolbar()
		self.toolbar.set_icon_size(Gtk.IconSize.MENU)
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_propagate_natural_height(True)

		# Header Objects
		self.headbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(self.headbox.get_style_context(), "Linked")

		self.close_tab_image = Gtk.Image()
		self.close_tab_image.set_from_file("lib/thumbs/close_tab.png")
		self.close_tab_button = Gtk.ToolButton()
		self.close_tab_button.set_icon_widget(self.close_tab_image)
		#self.close_tab_button.connect("clicked", self._close_current_tab2)
		self.headerbar.add(self.close_tab_button)
		#
		self.add_tab_image = Gtk.Image()
		self.add_tab_image.set_from_file("lib/thumbs/add_tab.png")
		self.add_tab_button = Gtk.ToolButton()
		self.add_tab_button.set_icon_widget(self.add_tab_image)
		self.add_tab_button.connect("clicked", self.open_new_tab)
		self.headerbar.add(self.add_tab_button)

		self.headerbar.pack_start(self.headbox)
		
		# Objects in Top Toolbar
		# Previous Page
		self.previmage = Gtk.Image()
		self.previmage.set_from_file("lib/thumbs/prev_image.png")
		self.goprev = Gtk.ToolButton()
		self.goprev.set_icon_widget(self.previmage)
		self.toolbar.insert(self.goprev, 0)
		# Next Page
		self.nextimage = Gtk.Image()
		self.nextimage.set_from_file("lib/thumbs/next_image.png")
		self.gonext = Gtk.ToolButton()
		self.gonext.set_icon_widget(self.nextimage)
		self.toolbar.insert(self.gonext, 1)

		self.webview = WebKit2.WebView()
		#self.webview.connect("notify::title", self.title_update)
		#print(self.get_title())
		self.webview.load_uri(KALI_URL)
		self.webview.set_border_width(0)
		self.page_title = PageUtility(KALI_URL).get_title()
		#print("[+ Title]", PageUtility(KALI_URL).get_title())
		self.headerbar.set_title(self.page_title + " - " + __head__)

		# self.notebook.set_tab_label_text(self.webview, "Karoki")

		self.scrolledwindow.add(self.webview)

		self.pagebox.pack_start(self.toolbar, False, False, 0)
		self.pagebox.pack_start(self.scrolledwindow, True, True, 0)

		self.notebook.append_page(self.pagebox, Gtk.Label(label=self.page_title))
		self.tabs = []
		self.tabs.append((self.create_tab(), Gtk.Label(label=self.page_title)))
		self.notebook.append_page(*self.tabs[0])

		#TabWindow()

	def title_update(self, widget, frame):
		self.set_title((__head__))
	def create_tab(self):
		tab = TabWindow()
		return tab
	def open_new_tab(self, widget):
		current_page = self.notebook.get_current_page()
		page_tuple = (self.create_tab, Gtk.Label(label=self.page_title))
		self.tabs.insert(current_page + 1, page_tuple)
		#self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page + 1)
		self.notebook.set_current_page(current_page + 1)


if __name__=="__main__":
	win = MainWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()
