###################################################################################
# Data
FILE = "file:///"
HTTP = "http://"
HTTPS = "https://"
search_tags = {
	"google":"https://www.google.com/search?q=",
	"duckduckgo":"https://duckduckgo.com/?q=",
	"yandex":"https://yandex.com/search/?text="
}
###################################################################################
# Data and Query Handling Class
class QueryService:
	def __init__(self, query):
		self.query = str(query)

	def check_domain(self, dom):
		domain_list = ["org", "edu", "com", "phy", "gov", "int", "mil", "net"]
		if dom in domain_list[:]:
			return True
		else:
			return False

	def url_decoder(self):
		code = {
			"%20":" ", "%21":"!", "%2C":",", "%28":"(", "%29":")", "%5B":"[", "%5D":"]", "%25":"%", "%26":"&",
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

	def fix_query(self):
		index = self.query.split(".")
		dom = self.query.split(".")[-1]
		# File
		if self.query.startswith("file:///"):
			ll = self.query[8:]
			return FILE + ll
		elif self.query.startswith("/"):
			ll = self.query[1:]
			return FILE + ll
		# HTTP
		elif self.query.startswith("http:") or self.query.startswith("http://"):
			ll = self.query[6:]
			return HTTP + ll
		# HTTPS
		elif self.query.startswith("https:") or self.query.startswith("https://"):
			ll = self.query[7:]
			return HTTPS + ll
		elif self.query.startswith("www."):
			return HTTPS + str(self.query)
		# Sites
		elif "." in self.query and len(dom) == 3:
			if self.check_domain(dom) == True:
				ll = str(self.query)
				return HTTPS + "www." + ll
			elif self.check_domain(dom) == False:
				ll = str(search_tags["google"]) + str(self.query)
				return ll
		# IPs
		elif len(index) == 4:
			if index[0] == "192" or index[0] == "127" or index[0] == "10":
				return HTTP + str(self.query)
			elif index[0] != "192" or index[0] != "127" or index[0] != "10":
				return HTTPS + str(self.query)
		else:
			ll = str(search_tags["google"]) + str(self.query)
			return ll