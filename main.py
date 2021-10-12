import requests
from bs4 import BeautifulSoup
import concurrent.futures
import lxml
import pandas as pd
import json
proxies_url = "https://www.google-proxy.net/"

def scrape_proxies(proxies_url):
	html = requests.get(proxies_url)
	content = BeautifulSoup(html.text, 'lxml')
	table = content.find('table')
	rows = table.findAll('tr')
	headers = [header.text for header in rows[0]]
	results = []
	for row in rows:
		results.append([data.text for data in row.findAll('td')])
	data = pd.DataFrame(results[1::], columns=headers)
	return data

def rotate(proxy, port):
	parsed_proxy = "http://" + proxy + ":" + port
	try:
		r = requests.get("https://httpbin.org/ip", proxies={"http": parsed_proxy, "https": parsed_proxy}, timeout=2)
		print(r.json(), " - worked!")
	except:
		pass


def rotate_list(proxy_list):
	for proxy, port in zip(proxy_list['IP Address'], proxy_list["Port"]):
		rotate(proxy, port)

proxies = scrape_proxies(proxies_url)
proxies_ip = proxies['IP Address'].tolist()
proxies_port = proxies["Port"].tolist()
with concurrent.futures.ThreadPoolExecutor() as executor:
	executor.map(rotate, proxies_ip, proxies_port)

