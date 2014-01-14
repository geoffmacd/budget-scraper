from Account import Account
import csv
from datetime import datetime

class Cibc(Account):
        """CIBC information scraper"""
        def __init__(self,f):
            super(Cibc,self).__init__()
            self.scrape(f)

        def scrape(self,f=None):
                csvFile = open(f,'rb')
                a = csv.reader(csvFile)
                for row in a:
                    debit,credit = 0,0
                    try:
                        debit = float(row[3].strip())
                    except Exception:
                        try:
                            credit = float(row[2].strip())
                        except Exception:
                            continue
                    entry = {'date':row[0].strip(),'name':row[1].strip(),'debit':debit,'credit':credit}
                    self.d.append(entry)
                self.convertDates()

        def convertDates(self):
            for i in range(len(self.d)):
                self.d[i]['date'] = datetime.strptime(self.d[i]['date'], "%Y-%m-%d")
