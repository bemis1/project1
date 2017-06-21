"""
    Process account bills consists of: Generating, persisting and delivering
    customer billing statements.
    Searches for unprocessed billing statements for the current month/year.
"""
import datetime
import logic.accounts
import logic.users


TEMPLATE = u'''
<p>Dear {name},</p>
<p>Thank you for using Acme Water\u2122 for your address at {address} {city}, {state} {zip}. Your amount due
for the month of {bill_month} is ${amount_due:.2f}.</p>
<p>Warm Regards, Acme Water\u2122</p>
'''


def process_monthly_bills(run_dt):
    month, year = run_dt.strftime('%m-%Y').split('-')
    account_bills = logic.accounts.get_account_bills(month, year, processed=0)
    for ab in account_bills:
        ab['bill_month'] = (datetime.datetime.strptime(ab['month'], "%m")
                            .strftime('%B'))
        ab['amount_due'] = ab['amount']
        logic.users.send_alert(ab['uuid'], ab['email'], TEMPLATE.format(**ab))
        logic.accounts.process_account_bill(ab['id'])


if __name__ == '__main__':
    run_date = datetime.date.today()
    process_monthly_bills(run_date)

