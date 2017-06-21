from db.accounts import Account, AccountAudit, AccountBill
from db import get_session, row2dict, row2dict_many
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import nose.tools


COLUMNS = frozenset(['uuid', 'name', 'email', 'address', 'city', 'state',
                     'zip'])


def is_dict_equal(old_info, new_info, keys=COLUMNS):
    old_info = dict((k, old_info[k]) for k in keys)
    try:
        nose.tools.assert_dict_equal(old_info, new_info)
        return True
    except AssertionError:
        return False


def set_account(account_orm, **new_values):
    for k, v in new_values.iteritems():
        setattr(account_orm, k, v)


def upsert_account(account_info, source):
    assert set(account_info.keys()) == COLUMNS
    uuid = account_info['uuid']
    session = get_session()
    try:
        account = (session.query(Account).filter_by(uuid=uuid).one())
        # check for changes
        if is_dict_equal(row2dict(account), account_info):
            return  # nothing to do
        for k, v in account_info.iteritems():
            setattr(account, k, v)
        session.add(account)
        # (session.query(Account).filter(Account.uuid == uuid)
        #         .update(account_info))
    except NoResultFound:
        # create a new account:
        account = Account(**account_info)
        session.add(account)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise
    # add a row to the audited table
    account_info['source'] = source
    account_info.pop('uuid')
    account_info['account_id'] = account.id
    session.add(AccountAudit(**account_info))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise


def _get_accounts(filters):
    session = get_session()
    return session.query(Account).filter_by(**filters).all()


def get_accounts(filters=None):
    """
    :param filters: optional dict with keys from COLUMNS ('uuid', 'name', ...)
    :return: List of dict repr of accounts
    """
    filters = filters or {}
    return map(row2dict, _get_accounts(filters))


from sqlalchemy.orm import aliased


def _get_accounts_billable(filters):
    """
    select * from accounts where not exists
    (select * from account_bills where account_bills.month = '06' and account_bills.year = '2017'
     and accounts.id = account_bills.account_id)
    :param filters:
    :return:
    """
    session = get_session()
    subquery = (session.query(AccountBill)
                .filter(AccountBill.month == filters.pop('month'))
                .filter(AccountBill.year == filters.pop('year'))
                .filter(Account.id == AccountBill.account_id))
    query = session.query(Account).filter(~subquery.exists())
    accounts = query.all()
    return accounts


def get_accounts_billable(filters):
    """
        Like get_accounts, but joins with accounts billable looking for ones
        without a generated bill.
    :param filters: optional dict with keys from COLUMNS ('uuid', 'name', ...)
                    requires month+year from the AccountBills table.
    :return: List of dict repr of accounts that have not been billed.
    """
    if not (filters.get('month') and filters.get('year')):
        raise
    return map(row2dict, _get_accounts_billable(filters))


def create_account_bill(account_id, amt, month, year):
    session = get_session()
    ab = AccountBill(account_id=account_id, amount=amt, month=month, year=year)
    session.add(ab)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise


def get_account_bills(month, year, processed):
    session = get_session()
    query = (session.query(Account, AccountBill)
             .join(AccountBill, AccountBill.account_id == Account.id)
             .filter(AccountBill.processed == processed)
             .filter(AccountBill.month == month)
             .filter(AccountBill.year == year))
    return map(lambda x: row2dict_many(*x), query.all())


def process_account_bill(bill_id):
    session = get_session()
    session.query(AccountBill).filter_by(id=bill_id).update({'processed': 1})
    session.commit()
