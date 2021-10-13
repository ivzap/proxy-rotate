import requests
from bs4 import BeautifulSoup
import concurrent.futures
import lxml
import pandas as pd
import json
proxies_url = "https://www.google-proxy.net/"

def scrape_proxies(proxies_url):
	print("------------------------------------------")
	print("|           [Scraping Proxies]           |")
	print("------------------------------------------")
	html = requests.get(proxies_url)
	content = BeautifulSoup(html.text, 'lxml')
	table = content.find('table')
	rows = table.findAll('tr')
	proxies = []
	for row in rows:
		all_data = [data.text for data in row.findAll('td', limit=2)]
		if(len(all_data) == 2):
			parser_dict = {"IP": None, "Port": None}
			parser_dict["IP"] = (all_data[0])
			parser_dict["Port"] = (all_data[1])
			proxies.append("http://" + parser_dict["IP"] + ":" + parser_dict["Port"])
	return proxies

def rotate(proxy):
	try:
		r = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=2)
		print(r.json(), " - worked!")
		print("-----------------------------------------")

	except:
		pass

proxies = scrape_proxies(proxies_url)
with concurrent.futures.ThreadPoolExecutor() as executor:
	executor.map(rotate, proxies)

