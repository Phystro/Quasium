#!/bin/env python3
import gi, os, sys
import mechanize, platform, socket
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gio, WebKit2, GLib, GObject, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import threading
from time import time, sleep

__version__ = "1.2.0"
__head__ = "QUASI-CSQ"
__thead__= "Quasi-CSQ"
__title__= "QUASI-CSQ - Eccentric Tensor Labs"
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
# Check Requirements
if sys.version_info < (3, 0, 0):
	print("Error: {} requires python 3".format(__head__))
	sys.exit(1)

####################################################################################
# Data Handling Class
class CreateProcFiles:
	def __init__(self, temp, perm):
		self.templist = temp
		self.permlist = perm
		templen = len(self.templist)
		permlen = len(self.permlist)
		#temporary files
		for i in range(0, templen):
			tfile = proc_path + self.templist[i]
			if os.path.isfile(tfile):
				pass
			elif not os.path.isfile(tfile):
				with open(tfile, "w") as f:
					f.write("0") #by default means no/negative
					f.close()
		#permanent files
		for i in range(0, permlen):
			pfile = proc_path + self.permlist[i]
			if os.path.isfile(pfile):
				pass
			elif not os.path.isfile(pfile):
				with open(pfile, "a") as f:
					f.write("")
					f.close()
class PageUtility:
	def __init__(self, query):
		self.query = str(query)
		self.browser = mechanize.Browser()
	def check_domain(self, dom):
		domain_list = ["org", "edu", "com", "phy", "gov", "int", "mil", "net"]
		if dom in domain_list[:]:
			print("in")
			return True
		else:
			print("not")
			return False
	def check_service(self):
		ind = self.query.split(".")
		if self.query.startswith("file:"):
			return "file"
		elif self.query.startswith("/") or self.query.startswith("//") or self.query.startswith("///"):
			return "file"
		elif self.query.startswith("http://"):
			return "http"
		elif self.query.startswith("https://"):
			return "https"
		elif self.query.startswith("www."):
			return "https"
		elif "." in self.query	and len(self.query[-3:]) == 3:
			if self.check_domain(self.query[-3:]) == True:
				return "site"
			elif self.check_domain(self.query[-3:]) == False:
				return None
		elif "." in self.query and len(self.query[-2:]) == 2:
			return "site"
		elif len(ind) == 4:
			if ind[0] == "192" or ind[0] == "127":
				return "http"
			elif ind[0] != "192" or ind[0] != "127":
				return "https"
		else:
			return None
	def fix_fileurl(self):
		if self.query.startswith("file:"):
			ll = self.query[7:]
			return FILE + ll
		if self.query.startswith("/"):
			ll = self.query[1:]
			return FILE + ll
	def fix_httpurl(self):
		if self.query.startswith("http:"):
			ll = self.query[6:]
			return HTTP + ll
		elif len(self.query.split(".")) == 4:
			#ind = self.query.split(".")
			#if ind[0] == "192" or ind[0] == "127":
			return HTTP + self.query
	def fix_httpsurl(self):
		if self.query.startswith("https:"):
			ll = self.query[7:]
			return HTTPS + ll
		elif self.query.startswith("www."):
			return HTTPS + self.query
		elif len(self.query.split(".")) == 4:
			#ind = self.query.split(".")
			#if ind[0] != "192" or ind[0] != "127":
			return HTTPS + self.query
	def fix_siteurl(self):
		ll = self.query
		return HTTPS + "www." + ll
	def get_title(self):
		try:
			page = self.browser.open(self.query)
			#print("[+] URL Works")
		except mechanize.URLError:
			print("[-] URL Unable to Connect")
			#return str(self.query)
			# Find way to send signal here
			pass
		else:
			#getting tab title
			source = page.read()
			#print(source)
			if bytes("<title>", "utf-8") in source:
				if bytes("rel=icon", "utf-8") and bytes("favicon", "utf-8") in source:
					#print("[+] We have a favicon")
					pass
				else:
					#print("[-] No Favicon")
					# Do soething about no favicons
					pass
				st = source.index(bytes("<title>", "utf-8"))
				en = source.index(bytes("</title>", "utf-8"))
				line = source[st + 7:en]
				#print("[+] Title: =>", line)
				line = str(line).strip("b").split("'")[1]
				page_title = line
				#print(page_title)
				return page_title
			elif bytes("<title>", "utf-8") not in source:
				# Remember a favicon for the titleless
				print("Here: ",self.query)
				return str(self.query)
	def url_decoder(self):
		code = {
			"%20":" ", "%21":"!", "%2C":",", "%28":"(", "%29":")", "%5B":"[", "%5D":"]", "%25":"%", #"%26":"&",
			"%F0":"ð", "%27":"'", "%C3":"Ã", "%BC":"¼",	"%BD":"½", "%BE":"¾", "%B5":"µ",
			"%9F%8E%AC":"¬",
		}

		for key in code.keys():
			if key in self.query:
				print(key)
				self.query = self.query.split(key)
				self.query = (code[key]).join(self.query)
				print(self.query)
		return self.query

####################################################################################
# Dialogs & Other Windows Class
class About(Gtk.AboutDialog):
	def __init__(self):
		Gtk.AboutDialog.__init__(self)
		### Fix the PixBuf Issue on the logo
		self.set_border_width(6)
		self.set_program_name(__head__+"\nQuasi-Counter Strike Quantum")
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
		self.set_logo_icon_name("Globe")
class Splash(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#create pop window
		self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("destroy", Gtk.main_quit)
		self.window.set_default_size(888, 500)
		#Add contents
		self.box = Gtk.VBox(spacing=6)
		self.img = Gtk.Image()
		self.img.set_from_file(icon_path + "quantum-eye.jpg")
		self.progress = Gtk.ProgressBar()
		self.progress.set_show_text(True)
		self.box.pack_start(self.img, False, False, 0)
		self.box.pack_start(self.progress, False, False, 0)

		self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)

		self.window.add(self.box)
	def on_timeout(self, user_data):
		new_value = self.progress.get_fraction() + 0.01
		self.progress.set_fraction(new_value)
		#sleep(0.1)
		if new_value == 1.02:
			return False
		else:
			return True
	def run(self):
		self.window.set_auto_startup_notification(False)
		self.window.show_all()
		self.window.set_auto_startup_notification(True)
		Gtk.main()
	def destroy(self):
		self.window.close()
class loading_indicator(Gtk.Spinner):
	def __init__(self):
		Gtk.Spinner.__init__(self)
		#Pop window
		self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("destroy", Gtk.main_quit)
		self.window.set_default_size(540, 440)

		self.spinner = Gtk.Spinner()
		self.spinner.start()

		self.window.add(self.spinner)

		self.show_all()
		Gtk.main()

####################################################################################
# Browser Tabs Class
class BrowserTab(Gtk.VBox):
	def __init__(self, addr=None):
		Gtk.VBox.__init__(self)

		self.tabtoolbar = Gtk.Toolbar()
		self.tabwebview = WebKit2.WebView()
		self.spinner = Gtk.Spinner()
		self.progressbar = Gtk.ProgressBar()
		#self.statusbar = Gtk.InfoBar()

		# ToolBar Items
		self.tabtoolbar.set_icon_size(Gtk.IconSize.MENU)
		self.tabtoolbar.set_show_arrow(True)
		# Previous Page
		self.previmage = Gtk.Image()
		self.previmage.set_from_file(icon_path + "prev_image.png")
		self.goprev = Gtk.ToolButton()
		self.goprev.set_icon_widget(self.previmage)
		self.goprev.connect("clicked", self.go_prev)
		self.tabtoolbar.insert(self.goprev, 0)
		# Next Page
		self.nextimage = Gtk.Image()
		self.nextimage.set_from_file(icon_path + "next_image.png")
		self.gonext = Gtk.ToolButton()
		self.gonext.set_icon_widget(self.nextimage)
		self.gonext.connect("clicked", self.go_next)
		self.tabtoolbar.insert(self.gonext, 1)
		# Refresh
		self.refimage = Gtk.Image()
		self.refimage.set_from_file(icon_path + "refresh_image.png")
		self.goref = Gtk.ToolButton()
		self.goref.set_icon_widget(self.refimage)
		self.goref.connect("clicked", self.go_refresh)
		self.tabtoolbar.insert(self.goref, 2)
		# Stop Loading
		self.stopimage = Gtk.Image()
		self.stopimage.set_from_file(icon_path + "stop_image.png")
		self.gostop = Gtk.ToolButton()
		self.gostop.set_icon_widget(self.stopimage)
		self.gostop.set_opacity(0.3)
		self.gostop.connect("clicked", self.stop_loading)
		self.tabtoolbar.insert(self.gostop, 3)
		# Home Page
		self.homeimage = Gtk.Image()
		self.homeimage.set_from_file(icon_path + "home_image.png")
		self.gohome = Gtk.ToolButton()
		self.gohome.set_icon_widget(self.homeimage)
		self.gohome.connect("clicked", self.go_home)
		self.tabtoolbar.insert(self.gohome, 4)
		# Search Bar
		self.toolitem_searchbar = Gtk.ToolItem()
		self.search_bar = Gtk.Entry()
		self.search_bar.connect("activate", self.search)
		self.search_bar.set_has_frame(True)
		self.toolitem_searchbar.set_expand(True)
		icon_name = "system-search-symbolic"
		self.search_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_name)
		self.search_engines()
		self.search_bar.set_placeholder_text("Search with DuckDuckGo or Enter Address")
		self.toolitem_searchbar.add(self.search_bar)
		self.tabtoolbar.insert(self.toolitem_searchbar, 5)
		# Downloads
		self.downimage = Gtk.Image()
		self.downimage.set_from_file(icon_path + "download_image.png")
		self.godown = Gtk.ToolButton()
		self.godown.set_icon_widget(self.downimage)
		self.tabtoolbar.insert(self.godown, 6)
		# Settings
		self.setimage = Gtk.Image()
		self.setimage.set_from_file(icon_path + "icon-fix.png")
		self.goset = Gtk.ToolButton()
		self.goset.set_icon_widget(self.setimage)
		self.tabtoolbar.insert(self.goset, 7)

		# # Spinner
		# self.pack_start(self.spinner, 0, 0, 0)

		# Webview Items
		if addr != None:
			self.tabwebview.load_uri(addr)

		self.tabwebview.connect("load-changed", self.url_changed)

		self.pack_start(self.tabtoolbar, False, False, 0)
		self.pack_start(self.tabwebview, True, True, 0)
		# self.pack_start(self.progressbar, True, True, 1)

		self.show_all()

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
	def do_pulse(self, user_data):
		self.search_bar.progress_pulse()
	def search(self, widget):
		self.tabwebview.grab_focus()
		address = self.search_bar.get_text()
		self.search_bar.set_text(address)
		# Input Validation
		serv = PageUtility(address).check_service()
		if serv == "file":
			nurl = PageUtility(address).fix_fileurl()
		elif serv == "http":
			nurl = PageUtility(address).fix_httpurl()
		elif serv == "https":
			nurl = PageUtility(address).fix_httpsurl()
		elif serv == "site":
			nurl = PageUtility(address).fix_siteurl()
		elif serv == None:
			address = str(search_tags["google"]) + address
			nurl = address

		self.tabwebview.load_uri(nurl)
	def search_engines(self):
		self.sengine = Gtk.Image()
		self.sengine.set_from_file(icon_path + "icon-other.png")
		#self.sengine.set_from_icon_name("Engine", 24)
		ind = self.sengine.get_pixbuf()
		self.search_bar.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, ind)
	def url_changed(self, widget, event):
		self.spinner.new()
		new_url = self.tabwebview.get_uri()
		self.search_bar.set_text(new_url)
		a = self.tabwebview.is_loading()
		if a == True:
			self.spinner.start()
			self.goref.hide()
			self.gostop.show()
			self.gostop.set_opacity(1.0)
		elif a == False:
			self.spinner.stop()
			self.gostop.hide()
			self.gostop.set_opacity(0.4)
			self.goref.show()

#####################################################################################
# Main Window Browser
class MainWindow(Gtk.Window):
	def __init__(self, addr=None):
		Gtk.Window.__init__(self, title=__title__)
		# Splash Screen
		splash = Splash()
		splash.start()
		###############################################################
		# Set up process files
		proc_files_t = [
			"fscreen",
		]
		proc_files_p = [
			"history",
		]
		CreateProcFiles(proc_files_t, proc_files_p)
		###############################################################
		sleep(5.08)
		splash.destroy()
		# Window
		self.set_default_size(1100, 660)
		self.set_border_width(0)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_resizable(True)
		self.activate_focus()	#activates current focused widget within window
		self.set_icon_from_file(icon_path + "eglobe.svg")
		self.set_default_icon_from_file(icon_path + "eglobe.svg")
		# HeaderBar
		self.headerbar = Gtk.HeaderBar()
		self.headerbar.set_title(__head__)
		self.headerbar.set_subtitle(__title__)
		self.headerbar.set_show_close_button(True)
		self.headerbar.set_decoration_layout("icon,menu:minimize,maximize,close")
		self.set_titlebar(self.headerbar)
		# Widgets on Header Bar
		# About/ Help
		self.about_image = Gtk.Image()
		self.about_image.set_from_file(icon_path + "icon-cloud.png")
		self.about_button = Gtk.ToolButton()
		self.about_button.set_icon_widget(self.about_image)
		self.about_button.connect("clicked", self.about)
		self.headerbar.add(self.about_button)
		# Close Tab
		self.close_tab_image = Gtk.Image()
		self.close_tab_image.set_from_file(icon_path + "close_tab.png")
		self.close_tab_button = Gtk.ToolButton()
		self.close_tab_button.set_icon_widget(self.close_tab_image)
		self.close_tab_button.connect("clicked", self.close_current_tab)
		self.headerbar.add(self.close_tab_button)
		# Open New Tab
		self.add_tab_image = Gtk.Image()
		self.add_tab_image.set_from_file(icon_path + "add_tab.png")
		self.add_tab_button = Gtk.ToolButton()
		self.add_tab_button.set_icon_widget(self.add_tab_image)
		self.add_tab_button.connect("clicked", self.open_blank_tab)
		self.headerbar.add(self.add_tab_button)

		# Notebook
		self.notebook = Gtk.Notebook()
		self.notebook.set_border_width(0)
		self.notebook.set_scrollable(True)
		self.notebook.set_show_tabs(True)
		self.notebook.set_show_border(True)
		self.notebook.popup_enable()
		self.add(self.notebook)

		#start
		if addr != None:
			self.contentpage(addr)
		elif addr == None:
			self.blankpage()

		# Shortcut Keys / Key Events
		self.connect("key-press-event", self.key_pressed)
		# On Browsing
		#self.notebook.get_nth_page(self.notebook.get_current_page()).tabwebview.connect("notify::title", self.url_changed)
		self.notebook.get_nth_page(self.notebook.get_current_page()).tabwebview.connect("load-changed", self.url_changed)

	def new_pages(self, page):
		if page == None:
			self.bpage = BrowserTab()
			self.notebook.append_page(self.bpage, Gtk.Label(label="New Tab"))
		elif page != None:
			self.cpage = BrowserTab(page)
			self.notebook.append_page(self.cpage, Gtk.Label(label="Content Page"))
	# Opening/Login Modes
	def blankpage(self):
		self.new_pages(page=None)
	def contentpage(self, addr):
		self.new_pages(page=addr)
	# About Window
	def about(self, widget):
		"""About The Browser"""
		win_about = About()
		win_about.show_all()
	def istitle(self, addr):
		num = self.notebook.get_current_page()
		self.page_title = self.notebook.get_nth_page(num).tabwebview.get_title()
		if self.page_title == None:
			serv = PageUtility(addr).check_service()
			if serv == "file":
				self.page_title = addr[7:]
				# more validation
				print("Address:", self.page_title)
				self.page_title = PageUtility(self.page_title).url_decoder()
				self.page_title = str(self.page_title)
				fsplt = self.page_title.split("/")
				flast = fsplt[len(fsplt) - 1]
				ffast = fsplt[:len(fsplt)]
				isfl = os.path.isfile(self.page_title)
				if isfl == True:
					self.page_title = flast
					print("True of", self.page_title)

				self.notebook.set_tab_label(self.notebook.get_nth_page(num), Gtk.Label(label=self.page_title))
				self.page_title = str(self.page_title) + " - " + __thead__
				return self.page_title
		else:
			self.notebook.set_tab_label(self.notebook.get_nth_page(num), Gtk.Label(label=self.page_title))
			self.page_title = str(self.page_title) + " - " + __thead__
			return self.page_title
	# Shortcut Functions
	def reload(self, widget=None):
		num = self.notebook.get_current_page()
		self.notebook.get_nth_page(num).tabwebview.reload()
	def focus_url_bar(self, widget=None):
		num = self.notebook.get_current_page()
		self.notebook.get_nth_page(num).search_bar.grab_focus()
	# Main Widget Functions
	def url_changed(self, widget, event):
		#print("URL url_changedGED")
		page_num = self.notebook.get_current_page()
		#print("Page NUM", page_num)
		new_url = self.notebook.get_nth_page(page_num).tabwebview.get_uri()
		# self.open_web_tab(new_url)
		# self.notebook.remove_page(page_num)
		# self.notebook.get_nth_page(page_num).search_bar.set_text(new_url)
		#print("Title:", self.istitle(new_url))
		self.headerbar.set_title(self.istitle(new_url))
		#self.open_web_tab(new_url)
		return 0
	# def url_changed_thread(self, widget, event):
	# 	run = threading.Thread(target=self.url_changed, args=(widget, event))
	# 	run.start()
	def open_blank_tab(self, widget=None):
		current_page = self.notebook.get_current_page()
		self.bpage = BrowserTab()
		#page_tuple = (self.bpage, Gtk.Label(label="New Tab."))
		#print(current_page)
		#self.tabs.insert(current_page + 1, page_tuple)
		self.notebook.insert_page(self.bpage, Gtk.Label(label="New Tab."), -1)
		#self.notebook.append_page(self.bpage, Gtk.Label(label="New Tab."))
		self.notebook.set_current_page(self.notebook.get_n_pages() - 1)
		#self.notebook.get_nth_page(self.notebook.get_current_page()).tabwebview.connect("notify::title", self.url_changed)
		self.notebook.get_nth_page(self.notebook.get_current_page()).tabwebview.connect("load-changed", self.url_changed)
	def open_web_tab(self, addr, widget=None):
		current_page = self.notebook.get_current_page()
		self.bpage = BrowserTab(addr)
		tab_title = self.istitle(addr)
		self.notebook.insert_page(self.bpage, Gtk.Label(label=tab_title), -1)
		self.notebook.set_current_page(current_page + 1)
		print("New WEB TAB No.", current_page)
		#close extra/unwanted tabs
		#page_num = current_page + 1
		#self.notebook.remove_page(page_num)
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
			current_page = self.notebook.get_current_page()
			self.notebook.remove_page(current_page)
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
			self.close()
	def many_window_handler(self, link):
		cwd = os.getcwd()
		command = os.system("python3 {}/quasi-csq-1.2.0.py {}".format(cwd, link))
		if command == 0:
			return False	#Successful
	def open_blank_window(self, widget=None):
		handle = threading.Thread(target=self.many_window_handler, args=("http://127.0.0.1",))
		handle.start()
	def fset(self, i):
		with open(proc_path+"fscreen", "w") as f:
			f.write(str(i))
			f.close()
	def fullview(self, widget=None):
		with open(proc_path+"fscreen", "r") as f:
			conf = f.read()
			f.close()
		if conf == "0":
			self.fullscreen()
			self.fset("1")
		elif conf == "1":
			self.unfullscreen()
			self.fset("0")
	def screenview(self, widget=None):
		run = threading.Thread(target=self.fullview, args=())
		run.start()
	def key_pressed(self, widget, event):
		modifiers = Gtk.accelerator_get_default_mod_mask()
		mapping = {
			Gdk.KEY_r: self.reload,
			Gdk.KEY_l: self.focus_url_bar,
			Gdk.KEY_t: self.open_blank_tab,
			Gdk.KEY_n: self.open_blank_window,
			Gdk.KEY_w: self.close_current_tab,
			Gdk.KEY_f: self.screenview,
			Gdk.KEY_q: self.exit
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
			browser.show_all()
			browser.connect("destroy", Gtk.main_quit)
			Gtk.main()
		except KeyboardInterrupt:
			print("\n[-] Shutdown Ordered!\nClosing...")