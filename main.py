import csv
from collections import namedtuple
import requests
from bs4 import BeautifulSoup

InnerBlock = namedtuple(
	'ParseResult',
	(
		'title',
		'price',
		'place',
		'pub_date',
		'url'
	),
)

class Olx:
	def __init__(self):
		self.url = 'https://www.olx.ua/zhivotnye/ptitsy/'
		self.result=[]
	def get_page(self,page: int = None):
		if page == None:
			page = 1
		url = f'{self.url}?page={page}'
		return requests.get(url).text
	def get_max_page(self,text):
		soup = BeautifulSoup(text,'lxml')
		a = soup.select('a.block.br3.brc8.large.tdnone.lheight24 span')[-1].text
		return int(a)
	def parse_data(self, page=None):
		print(page)
		text = self.get_page(page=page)
		soup = BeautifulSoup(text,'lxml')
		trs = soup.select('tr.wrap')
		for tr in trs:
			self.parse_tr(tr)
	def parse_tr(self,tr):
		a = tr.select_one('a.marginright5.link.linkWithHash.detailsLink')
		title = a.select_one('strong').text
		url = a.get('href')
		small = tr.select('p.lheight16 small span')
		place = small[0].text
		pub_date = small[1].text
		price = tr.select_one('p.price strong').text
		data = {
			'title':title,
			'price':price,
			'place':place,
			'pub_date':pub_date,
			'url':url
		}
		self.result.append(InnerBlock(
			title=title,
			price=price,
			place=place,
			pub_date=pub_date,
			url=url
		))
	def write_csv(self):
		with open('olx.csv','a') as f:
			writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
			writer.writerow(('Название','Цена','Местоположение','Дата публикации', 'Ccылка'))
			for i in self.result:
				writer.writerow(i)

	def run(self):
		max_page = self.get_max_page(self.get_page())
		for i in range(2,max_page+1):
			self.parse_data(i)
			self.write_csv()
def main():
	parser = Olx()
	parser.run()
main()
