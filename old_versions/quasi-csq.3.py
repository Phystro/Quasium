#!/bin/env python3
import gi, os, sys
import mechanize, platform, socket
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gio, WebKit2, GLib, GObject, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from threading import Thread


__version__ = "1.1.0"
__head__ = "QUASI-CSQ"
__thead__= "Quasi-CSQ"
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
				line = str(line).strip("b").split("'")[1]
				page_title = line
				print(page_title)
				return page_title
			elif not "<title>" in source:
				print("[-] No Title")

####################################################################################
# Dialogs Class
class About(Gtk.AboutDialog):
	def __init__(self):
		Gtk.AboutDialog.__init__(self)
		### Fix the PixBuf Issue on the logo

		self.set_border_width(6)
		self.set_program_name(__head__+"\nQuasi-Counter Strike Quantum")
		self.set_version("version 1.1.1")
		self.set_copyright("Eccentric Tensor Labs")
		self.set_comments("Smooth Private Secure Web Browser")
		self.set_license("GNU/GPL License")
		self.set_wrap_license(True)
		self.set_website("https://thehackerrealm.blogspot.com")
		self.set_website_label("ETLabs")
		self.set_authors(['Anthony "Phystro" Karoki'])
		self.set_artists(['Quasar', 'Linux', 'Anthony "Phystro" Karoki'])
		self.set_documenters(['Quaser', 'Omicron', 'Betelguese'])
		self.set_logo()
		self.set_logo_icon_name("Globe")
class Splash(Thread):
	def __init__(self):
		Thread.__init__(self)

		#create pop window
		self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("destroy", Gtk.main_quit)
		self.window.set_default_size(540, 440)

		#Add contents
		box = Gtk.Box()
		lbl = Gtk.Label()
		lbl.set_label("App is Loading...")
		status = Gtk.Statusbar()
		img = Gtk.Image()
		img.set_from_file("/root/Pictures/csgo.jpg")
		box.pack_start(img, False, False, 0)
		status.add(lbl)
		box.pack_start(status, True, True, 1)

		self.window.add(box)
	def run(self):
		self.window.set_auto_startup_notification(False)
		self.window.show_all()
		self.window.set_auto_startup_notification(True)
		Gtk.main()

	def destroy(self):
		self.window.destroy()

####################################################################################
# Browser Tabs Class
class BlankPage(Gtk.VBox):
	def __init__(self):
		Gtk.VBox.__init__(self)
		self.set_border_width(20)

		self.tabpagegrid = Gtk.Grid()
		self.tabpagegrid.set_column_spacing(70)
		self.tabpagegrid.set_row_spacing(60)
		self.add(self.tabpagegrid)

		self.nextimage = Gtk.Image()
		self.nextimage.set_from_file("lib/thumbs/next_image.png")

		self.previmage = Gtk.Image()
		self.previmage.set_from_file("lib/thumbs/prev_image.png")

		# Search Bar
		self.toolitem_searchbar = Gtk.ToolItem()
		self.search_bar = Gtk.Entry()
		#self.search_bar.connect("activate", self.search)
		self.search_bar.set_has_frame(True)
		self.toolitem_searchbar.set_expand(True)
		self.search_bar.set_progress_pulse_step(0.1)
		self.search_bar.set_progress_fraction(0.5)
		#self.timeout_id = GLib.timeout_add(100, self.do_pulse, None)
		icon_name = "system-search-symbolic"
		self.search_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_name)
		self.search_bar.set_placeholder_text("Search with DuckDuckGo or Enter Address")
		self.toolitem_searchbar.add(self.search_bar)
		#self.tabtoolbar.insert(self.toolitem_searchbar, 4)

		self.tabpagegrid.attach(self.nextimage, 1, 2, 1, 1)
		self.tabpagegrid.attach(self.toolitem_searchbar, 2, 2, 12, 1)
		self.tabpagegrid.attach_next_to(self.previmage, self.toolitem_searchbar, Gtk.PositionType.RIGHT, 1, 1)

		self.show_all()

class TabWindow(Gtk.VBox):
	def __init__(self):
		Gtk.VBox.__init__(self)

		self.tabpagebox = Gtk.VBox()
		self.add(self.tabpagebox)

		self.tabscrolledwindow = Gtk.ScrolledWindow()
		self.tabwebview = WebKit2.WebView()
		#self.tabwebview.load_uri(KALI_URL)
		self.tabscrolledwindow.add(self.tabwebview)

		self.tabtoolbar = Gtk.Toolbar()
		self.tabtoolbar.set_icon_size(Gtk.IconSize.MENU)
		# Previous Page
		self.previmage = Gtk.Image()
		self.previmage.set_from_file("lib/thumbs/prev_image.png")
		self.goprev = Gtk.ToolButton()
		self.goprev.set_icon_widget(self.previmage)
		self.goprev.connect("clicked", self.go_prev)
		self.tabtoolbar.insert(self.goprev, 0)
		# Next Page
		self.nextimage = Gtk.Image()
		self.nextimage.set_from_file("lib/thumbs/next_image.png")
		self.gonext = Gtk.ToolButton()
		self.gonext.set_icon_widget(self.nextimage)
		self.gonext.connect("clicked", self.go_next)
		self.tabtoolbar.insert(self.gonext, 1)
		# Refresh
		self.refimage = Gtk.Image()
		self.refimage.set_from_file("lib/thumbs/refresh_image.png")
		self.goref = Gtk.ToolButton()
		self.goref.set_icon_widget(self.refimage)
		self.goref.connect("clicked", self.go_refresh)
		self.tabtoolbar.insert(self.goref, 2)
		# Home Page
		self.homeimage = Gtk.Image()
		self.homeimage.set_from_file("lib/thumbs/home_image.png")
		self.gohome = Gtk.ToolButton()
		self.gohome.set_icon_widget(self.homeimage)
		self.gohome.connect("clicked", self.go_home)
		self.tabtoolbar.insert(self.gohome, 3)
		# Search Bar
		self.toolitem_searchbar = Gtk.ToolItem()
		self.search_bar = Gtk.Entry()
		self.search_bar.connect("activate", self.search)
		self.search_bar.set_has_frame(True)
		self.toolitem_searchbar.set_expand(True)
		#self.search_bar.set_progress_pulse_step(0.1)
		#self.search_bar.set_progress_fraction(0.5)
		#self.timeout_id = GLib.timeout_add(100, self.do_pulse, None)
		icon_name = "system-search-symbolic"
		self.search_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_name)
		self.search_bar.set_placeholder_text("Search with DuckDuckGo or Enter Address")
		self.toolitem_searchbar.add(self.search_bar)
		self.tabtoolbar.insert(self.toolitem_searchbar, 4)
		# Downloads
		self.downimage = Gtk.Image()
		self.downimage.set_from_file("lib/thumbs/download_image.png")
		self.godown = Gtk.ToolButton()
		self.godown.set_icon_widget(self.downimage)
		self.tabtoolbar.insert(self.godown, 5)
		# Settings
		self.setimage = Gtk.Image()
		self.setimage.set_from_file("lib/thumbs/icon-fix.png")
		self.goset = Gtk.ToolButton()
		self.goset.set_icon_widget(self.setimage)
		self.tabtoolbar.insert(self.goset, 6)

		self.tabpagebox.pack_start(self.tabtoolbar, False, False, 0)
		self.tabpagebox.pack_start(self.tabscrolledwindow, True, True, 0)
		self.show_all()

		#self.tabwebview.connect("notify::title", self.update_title)

	#def update_title(self, widget, frame):
		#MainWindow.self.headerbar.set_title(self.page_title + " - " + __head__)
	def search(self, widget):
		address = self.search_bar.get_text()
		#self.tabwebview.load_uri(address)
		# print ("Hello ftom Tab WIndow")
		# MainWindow.tab_url_changed(address)
	def do_pulse(self, user_data):
		self.search_bar.progress_pulse()
		return True
	def go_prev(self, widget):
		self.tabwebview.go_back()
	def go_next(self, widget):
		self.tabwebview.go_forward()
	def go_home(self, widget):
		self.tabwebview.load_uri(KALI_URL)
	def go_refresh(self, widget):
		self.tabwebview.reload()
	def stop_loading(self, widget):
		self.tabwebview.stop_loading()

class MainWindow(Gtk.Window, TabWindow):
	def __init__(self):
		Gtk.Window.__init__(self, title=__title__)

		# splash = Splash()
		# splash.start()
		# from time import sleep
		# sleep(2)
		# splash.destroy()

		self.set_default_size(1100, 660)
		self.set_border_width(0)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_icon_from_file("lib/thumbs/eglobe.svg")
		self.set_default_icon(Gtk.IconTheme.get_default().load_icon("edit-copy", 64, 0))
		self.set_default_icon_from_file("lib/thumbs/eglobe.svg")

		# Main Window
		self.headerbar = Gtk.HeaderBar()
		self.headerbar.set_title(__head__)
		self.headerbar.set_subtitle(__title__)
		self.headerbar.set_show_close_button(True)
		self.set_titlebar(self.headerbar)
		# Widgets on Header Bar
		# About/ Help
		self.about_tab_image = Gtk.Image()
		self.about_tab_image.set_from_file("lib/thumbs/icon-cloud.png")
		self.about_tab_button = Gtk.ToolButton()
		self.about_tab_button.set_icon_widget(self.about_tab_image)
		self.about_tab_button.connect("clicked", self.about)
		self.headerbar.add(self.about_tab_button)
		# Close Tab
		self.close_tab_image = Gtk.Image()
		self.close_tab_image.set_from_file("lib/thumbs/close_tab.png")
		self.close_tab_button = Gtk.ToolButton()
		self.close_tab_button.set_icon_widget(self.close_tab_image)
		self.close_tab_button.connect("clicked", self.close_current_tab)
		self.headerbar.add(self.close_tab_button)
		# Open New Tab
		self.add_tab_image = Gtk.Image()
		self.add_tab_image.set_from_file("lib/thumbs/add_tab.png")
		self.add_tab_button = Gtk.ToolButton()
		self.add_tab_button.set_icon_widget(self.add_tab_image)
		self.add_tab_button.connect("clicked", self.open_new_tab)
		self.headerbar.add(self.add_tab_button)
		#
		# Home Page/ Start Page
		self.notebook = Gtk.Notebook()
		self.notebook.set_scrollable(True)
		self.notebook.set_show_tabs(True)
		self.notebook.set_show_border(True)
		self.add(self.notebook)

		#self.page_title = PageUtility("http://127.0.0.1").get_title()
		self.page_title = "New Tab"

		self.tabs = []
		self.tabs.append((self.create_tab(), Gtk.Label(label=self.page_title)))
		self.headerbar.set_title(str(self.page_title) + " - " + __thead__)
		self.notebook.append_page(*self.tabs[0])

		# # WebPages and Web Addresses
		# self.currentwebview = self.tabs[self.notebook.get_current_page()][0].tabwebview
		# self.urlbar = self.tabs[self.notebook.get_current_page()][0].search_bar

		# self.currentwebview.connect("notify::title", self.url_changed)

		# Shortcut Keys / Key Events
		# self.connect("key-press-event", self.key_pressed)

	# def tab_url_changed(self, address):
	# 	query = address
	# 	query = self.currentwebview.get_uri()
	# 	title = self.currentwebview.get_title()
	# 	#current_page = self.notebook.get_current_page()
	# 	print(query)
	# 	#self.headerbar.set_title(self.page_title + " - " + __head__)

	# def url_changed(self, widget, webview):
	# 	query = self.currentwebview.get_uri()
	# 	title = self.currentwebview.get_title()

	# 	current_page = self.notebook.get_current_page()

	# 	page_tuple = (self.create_tab(), Gtk.Label(label=title))
	# 	self.tabs.insert(current_page + 1, page_tuple)
	# 	self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page + 1)
	# 	self.notebook.set_current_page(current_page + 1)

	# 	self.currentwebview = self.tabs[current_page + 1][0].tabwebview
	# 	self.urlbar = self.tabs[self.notebook.get_current_page()][0].search_bar
	# 	self.currentwebview.load_uri(query)
	# 	self.urlbar.set_text(query)
	# 	self.headerbar.set_title(title + " - " + __thead__)
	# 	self.notebook.remove(self.tabs.pop(int(current_page))[0])

	# Tab Elements & Widgets
	def tabrealm(self):
		self.tabpagebox = Gtk.VBox()
		self.add(self.tabpagebox)

		self.show_all()

	def create_tab(self):
		tab = self.tabrealm()
		#tab = TabWindow()
		#tab = BlankPage()
		return tab
	def close_current_tab(self, widget):
		if self.notebook.get_n_pages() == 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.WARNING,
				buttons=Gtk.ButtonsType.OK_CANCEL, text="Confirm Exit")
			dialog.format_secondary_text("Do You Really Wish to Close {}".format(__head__))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				dialog.destroy()
				page = self.notebook.get_current_page()
				current_tab = self.tabs.pop(page)
				self.notebook.remove(current_tab[0])
				sys.exit(0)
				#Gtk.main_quit
			elif response == Gtk.ResponseType.CANCEL:
				dialog.destroy()
				return
		else:
			page = self.notebook.get_current_page()
			current_tab = self.tabs.pop(page)
			self.notebook.remove(current_tab[0])
	def open_new_tab(self, widget):
		current_page = self.notebook.get_current_page()
		page_tuple = (self.create_tab(), Gtk.Label(label=self.page_title))
		self.headerbar.set_title(str(self.page_title) + " - " + "Quasi-CSQ")
		self.tabs.insert(current_page + 1, page_tuple)
		self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page + 1)
		self.notebook.set_current_page(current_page + 1)
		#self.currentwebview.connect("notify::title", self.url_changed)
		#if self.url_changed():
		#	pass
		#else:
		#	print("nope")
	def about(self, widget):
		win_about = About()
		win_about.show_all()

	# Shortcut Key Methods/Functions
	def _reload_tab(self):
		self.tabs[self.notebook.get_current_page()][0].tabwebview.reload()
	def _open_new_tab(self):
		current_page = self.notebook.get_current_page()
		page_tuple = (self.create_tab(), Gtk.Label(label=self.page_title))
		self.headerbar.set_title(self.page_title + " - " + "Quasi-CSQ")
		self.tabs.insert(current_page + 1, page_tuple)
		self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page + 1)
		self.notebook.set_current_page(current_page + 1)
	def _focus_url_bar(self):
		current_page = self.notebook.get_current_page()
		self.tabs[current_page][0].search_bar.grab_focus()
	def _zoom_bar(self):
		current_page = self.notebook.get_current_page()
		self.tabs[current_page][0].tabtoolbar.show_all()
	def _close_current_tab(self):
		if self.notebook.get_n_pages() == 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.WARNING,
				buttons=Gtk.ButtonsType.OK_CANCEL, text="Confirm Exit")
			dialog.format_secondary_text("Do You Really Wish to Close {}".format(__head__))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				dialog.destroy()
				page = self.notebook.get_current_page()
				current_tab = self.tabs.pop(page)
				self.notebook.remove(current_tab[0])
				sys.exit(0)
			elif response == Gtk.ResponseType.CANCEL:
				dialog.destroy()
				return
		else:
			page = self.notebook.get_current_page()
			current_tab = self.tabs.pop(page)
			self.notebook.remove(current_tab[0])
	def _exit(self):
		if self.notebook.get_n_pages() > 1:
			dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION,
				buttons=Gtk.ButtonsType.YES_NO, text="Confirm Exit")
			dialog.format_secondary_text("\tClosing Down {} Tabs!\nDo You Really Wish to Close {}".format(self.notebook.get_n_pages(), __head__))
			response = dialog.run()
			if response == Gtk.ResponseType.YES:
				dialog.destroy()
				page = self.notebook.get_current_page()
				current_tab = self.tabs.pop(page)
				self.notebook.remove(current_tab[0])
				self.connect("destroy", Gtk.main_quit)
				sys.exit(0)
			elif response == Gtk.ResponseType.NO:
				dialog.destroy()
				return
		else:
			page = self.notebook.get_current_page()
			current_tab = self.tabs.pop(page)
			self.notebook.remove(current_tab[0])
			self.connect("destroy", Gtk.main_quit)
			sys.exit(0)
	def key_pressed(self, widget, event):
		modifiers = Gtk.accelerator_get_default_mod_mask()
		mapping = {
			Gdk.KEY_r: self._reload_tab,
			Gdk.KEY_t: self._open_new_tab,
			Gdk.KEY_w: self._close_current_tab,
			Gdk.KEY_l: self._focus_url_bar,
			Gdk.KEY_b: self._zoom_bar,
			Gdk.KEY_q: self._exit
		}
		if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK and event.keyval in mapping:
			mapping[event.keyval]()
win = MainWindow()
win.show_all()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
