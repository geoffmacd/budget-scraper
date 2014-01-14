import getopt,sys
from Account import Account
from Meridian import Meridian
from Cibc import Cibc
from datetime import datetime

# iterate over years
def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield y, m+1

def analyze(accounts):
    print "Analyzing"

    #add transactions from every account and sort
    t = []
    for a in accounts:
        t.extend(a)
    t.sort()

    #calc for each month, start at first trans
    sy = t[0]['date'].year
    sm = t[0]['date'].month
    ey = t[-1]['date'].year
    em = t[-1]['date'].month
    m = []
    i = 0
    for y,m in month_year_iter(sm,sy,em,ey):
        #cycle through transaction
        spending , income = 0,0
        while t[i]['date'].month == m and t[i]['date'].year == y:
            #process
            if not specialCondition(l['name']):
                spending += t[i]['credit']
                income += t[i]['debit']
            i++
        month = {'date':datetime.datetime(y,m,1),'spending':spending,'income':income}
        print "%d %d : Spent $ %.2f , Made $ %.2f" % (y,m,spending,income)
        m.append(month)

    print
    #print highest spending, income months
    highestS = max(m,key=lambda k: k['credit'])
    lowestS = min(m,key=lambda k: k['credit'])
    highestI = max(m,key=lambda k: k['debit'])
    AvInc = sum(map(lambda x: x['debit'],m))/len(m)
    print "Highest spending on %d %d with $ %.f2" % (highestS['date'].year, highestS['date'].month,  highestS['credit'])
    print "Lowest spending on %d %d with $ %.f2" % (lowestS['date'].year, lowestS['date'].month,  lowestS['credit'])
    print "Highest income on %d %d with $ %.2f" % (highestI['date'].year, highestI['date'].month,  highestI['debit'])
    print "Average income: $ %.2f" % AvInc
    print

    spending = 0
    income = 0
    for a in accounts:

        for l in a.d:
            print l
            if not specialCondition(l['name']):
                spending += l['credit']
                income += l['debit']

    print 'Total Spending: ' + str(spending)
    print 'Total Income: ' + str(income)
    print '-----------------------------'
    print 'Total Savings: ' + str(income - spending)

def specialCondition(n):
    # do not include itrade transfers, CIBC is included
    if n.find("ITrade") > -1:
        return True

def main(argv):
    try:
        opts,args = getopt.getopt(argv, "m:c:v:", ["meridian=", "cibc=", 'visa='])
    except getopt.GetoptError:
        sys.exit(2)
    accounts = []
    #process files
    print opts
    for opt, arg in opts:
        if opt in ("-m", "--meridian"):
            #open file
            m = Meridian(arg)
            accounts.append(m)
        elif opt in ("-c", "--cibc"):
            #open file
            c = Cibc(arg)
            accounts.append(c)
        elif opt in ("-v", "--visa"):
            #open file
            v = Cibc(arg)
            accounts.append(v)
    analyze(accounts)

if __name__ == '__main__':
    main(sys.argv[1:])
