from Account import Account
from bs4 import BeautifulSoup
from datetime import datetime
from re import sub

money = '$6,150,593.22'

class Meridian(Account):
	"""Meridian scraper"""

	def __init__(self,f):
		super(Meridian,self).__init__()
		self.scrape(f)

	def scrape(self,f):
		htmlFile = open(f,'rb')
		htmlText = htmlFile.read()
		soup = BeautifulSoup(htmlText)
		htmlFile.close()
		blah = soup.find_all('tr')
		for row in blah:
			cells = row.find_all('td')
			try:
				debit,credit = 0,0
				if cells[2].contents[0][0] == '-':
					#negative
					credit = float(sub(r'[^\d.]', '', cells[2].contents[0][2:].strip()))
				else:
					debit = float(sub(r'[^\d.]', '', cells[2].contents[0][1:].strip()))
				balance = float(sub(r'[^\d.]', '', cells[3].contents[0][1:].strip()))
			except Exception, e:
				continue
			entry = { 'date': cells[0].contents[0].strip(), 'name':cells[1].contents[0].strip(),'debit':debit,'credit':credit}
			self.d.append(entry)
		self.convertDates()

	def convertDates(self):
            for i in range(len(self.d)):
                self.d[i]['date'] = datetime.strptime(self.d[i]['date'], "%b %d, %Y")
