from db.user_alerts import UserAlert
from db import get_session


def _queue_email(email, body):
    # TODO
    print "alert to %s" % email
    print "%s" % body
    pass


def send_alert(uuid, email, content):
    session = get_session()
    _queue_email(email, content)
    ua = UserAlert(uuid=uuid, content=content)
    session.add(ua)
    session.commit()
