from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import sys
from pprint import pprint

import time

class TwitterCrawler:

	def __init__(self):
		self.driver = webdriver.Chrome()
		self.wait = WebDriverWait(self.driver, 60)
		
	def getFinalUrl(url, method="get", data=None):
		"""
        check whether a specific URL is reachable
        :param url: URL for checking
        :param method: the method used to access the URL, get or post, default is get
        :param data: data used to attach to the request
        :return: {'finalurl':<final URL>, 'redirect':<list of redirection>, 'dom':<DOM of the page>}-if reachable,
        None-unreachable
        """
        # disable warning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        #format url
        if not url.startswith("http"):
            url = "http://" + url

        res = {}
        r = self.sendRequest(url, method, data)
        #print(r)

        if r is not None and r.status_code == 200:
            res['finalUrl'] = r.url
            res['dom'] = r.text
            if len(r.history) != 0:
                # for saving the raw data
                res['redirect'] = []
                # add all the url
                for redirectResponse in r.history:
                    res['redirect'].append(redirectResponse.url)
                # add for final url to fill up completed path
                res['redirect'].append(r.url)
            else:
                res['redirect'] = None
        else:
            res = None

        return res
		
	def call(self, id, savefolder, url="https://twitter.com/i/web/status/"):
		
		# check if result exists
		fname = os.path.join(savefolder, id_str)
		if os.path.isfile(fname):
			print("file exists: %s" % (fname))	
			return
		
		# otherwise call
		url = ''.join([url,id])
		expanded_url = self.vt_more(url)
		
		if expanded_url:
			# get final url
			res = getFinalUrl(expanded_url)
			
			# write to file
			with open(fname, 'w', encoding="utf-8") as fout:
				pprint(res, fout)

	def vt_more(self, url):
		print(url)

		driver = self.driver
		wait = self.wait

		driver.get(url)

		# waiting for presence of an element
		time.sleep(1)
		
		# get elements
		try: element = driver.find_element_by_xpath("//div[@class='js-tweet-text-container']/p/a").get_attribute("data-expanded-url")
		except Exception as e: pass #print(e)
		else: return element

if __name__ == '__main__':

	url = "https://twitter.com/i/web/status/1166752700324859904"
	ct = TwitterCrawler()
	res = ct.vt_more(url)
	print(res)