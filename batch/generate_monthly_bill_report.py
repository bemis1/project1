"""
    Process account bills consists of: Generating, persisting and delivering
    customer billing statements.
    Searches for unprocessed billing statements for the current month/year.

    Would be cool to generate a web based dash...
    for now just prints to stdout :)
"""
import datetime
import logic.accounts
import logic.users


def report_monthly_bills(run_dt):
    month, year = run_dt.strftime('%m-%Y').split('-')
    account_bills = logic.accounts.get_account_bills(month, year, processed=1)
    total = sum([x['amount'] for x in account_bills])
    count = len(account_bills)
    print ('Total Amount Billed: %s' % total)
    print ('Number of Invoices: %s' % count)


if __name__ == '__main__':
    run_date = datetime.date.today()
    report_monthly_bills(run_date)
