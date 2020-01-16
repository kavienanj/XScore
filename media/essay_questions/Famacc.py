import datetime

current_date = datetime.date.today()
Family_account_holders = 0


class New:

    def __init__(self, name, bank, bank_acc_no, info):
        self.name = name
        self.bank = bank
        self.bank_acc_no = bank_acc_no
        self.info = info
        self.ac_info = [self.name,self.bank,self.bank_acc_no,self.info]

    def maturity_end(self, day, month, year, current_date ):
        self.end_date = str(day) + '-' + str(month) + '-' + str(year)
        date = datetime.date(year, month, day)
        self.date_difference = (date - current_date).days

    def __repr__(self):
        key_doc = {}
        key_doc[self.bank_acc_no] = self.ac_info
        return str(key_doc)


Appa = New('K.Jegatheesan', 'Commercial Bank', '9210832330', 'This is an account')
Amma = New('J.Saththiya', 'NSB', '1234567','Another account')
Amamma = New('R.Kamaladevi','Commercial Bank','234567','Another one too')
Appa.maturity_end(3, 12, 2018, current_date)
Amma.maturity_end(18,5,2019,current_date)
Amamma.maturity_end(14,5,2019,current_date)
print(Appa)