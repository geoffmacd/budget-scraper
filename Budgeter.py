import getopt,sys
from Account import Account
from Meridian import Meridian
from Cibc import Cibc
from datetime import datetime

# iterate over years
def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end+1 ):
        y, m = divmod( ym, 12 )
        yield y, m+1

def analyze(accounts):
    print "Analyzing"

    #add transactions from every account and sort
    t = []
    for a in accounts:
        t.extend(a.d)
    t.sort(key=lambda k: k['date'])

    #calc for each month, start at first trans
    sy = t[0]['date'].year
    sm = t[0]['date'].month
    ey = t[-1]['date'].year
    em = t[-1]['date'].month
    mos = []
    i = 0
    for y,m in month_year_iter(sm,sy,em,ey):
        #cycle through transaction
        spending , income = 0,0
        print
        while i < len(t) and t[i]['date'].month == m and t[i]['date'].year == y:
            #process
            if not specialCondition(t[i]['name']):
                spending += t[i]['credit']
                income += t[i]['debit']
            i += 1
        month = {'date':datetime(y,m,1),'spending':spending,'income':income}
        print "%d %d : Spent $ %.2f , Made $ %.2f" % (y,m,spending,income)
        mos.append(month)


    print
    #print highest spending, income months
    highestS = max(mos,key=lambda k: k['spending'])
    lowestS = min(mos,key=lambda k: k['spending'])
    highestI = max(mos,key=lambda k: k['income'])
    AvInc = sum(map(lambda x: x['income'],mos))/len(mos)
    print "Highest spending on %d %d with $ %.2f" % (highestS['date'].year, highestS['date'].month,  highestS['spending'])
    print "Lowest spending on %d %d with $ %.2f" % (lowestS['date'].year, lowestS['date'].month,  lowestS['spending'])
    print "Highest income on %d %d with $ %.2f" % (highestI['date'].year, highestI['date'].month,  highestI['income'])
    print "Average income: $ %.2f" % AvInc
    print

    spending = 0
    income = 0
    for l in t:
        if not specialCondition(l['name']):
            spending += l['credit']
            income += l['debit']

    print 'Total Spending: ' + str(spending)
    print 'Total Income: ' + str(income)
    print '-----------------------------'
    print 'Total Savings: ' + str(income - spending)

def specialCondition(n):
    # do not include itrade transfers, CIBC is included
    codeWords = ["ITrade","In from advntge","Cheque 50","INSTANT TELLER DEPOSIT","PAYMENT THANK YOU","INTERNET TRANSFER"]
    for c in codeWords:
        if n.find(c) > -1:
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
