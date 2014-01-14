import getopt,sys
from Account import Account
from Meridian import Meridian
from Cibc import Cibc

def analyze(accounts):
    #calc for each month
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
