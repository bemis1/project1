"""
    Iterates accounts for the current mm/yyyy (or supplied mm/yyyy)
    calling the REST service for monthly bill.  Creates a bill if successful.
    If REST call fails or returns garbage, will report and log raise exception
    for retry.
"""
import requests
import json
import datetime
from decimal import Decimal
import logic.accounts


SERVER = 'http://api.acme.fake'
API = '/due/{uuid}/{mm}/{yyyy}'


def get_amount_due(uuid, mm, yyyy):
    """
        Exceptions to handle:
        requests.ConnectionError, requests.Timeout, KeyError (invalid response)
        TypeError (invalid response), and requests.RequestException
    :param uuid:
    :param mm:
    :param yyyy:
    :return:
    """
    api = API.format(uuid=uuid, mm=mm, yyyy=yyyy)
    r = requests.get('{}{}'.format(SERVER, api), timeout=10)
    if r.status_code >= requests.codes.bad_request:
        raise requests.RequestException(response=r)
    response = json.loads(r.content, parse_float=Decimal)
    return response['amount_due']


def create_monthly_bills(run_dt, accounts=None, retries=0):
    month, year = run_dt.strftime('%m-%Y').split('-')
    accounts = accounts or logic.accounts.get_accounts_billable({'year': year, 'month': month})
    errors = []
    for account in accounts:
        try:
            amt = get_amount_due(account['uuid'], month, year)
        except (requests.RequestException, KeyError, TypeError):
            errors.append(account)
            continue
        logic.accounts.create_account_bill(account['id'], amt, month, year)
    if errors and retries > 0:
        return create_monthly_bills(run_dt, errors, retries=retries - 1)
    if errors:
        write_to_file(errors)
        raise


def write_to_file(*_):
    pass


if __name__ == '__main__':
    run_date = datetime.date.today()
    create_monthly_bills(run_date)
