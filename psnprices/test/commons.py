from _pytest.monkeypatch import MonkeyPatch
import pytest
import sys

monkeypatch = MonkeyPatch()

def mailalert(alerts_line, mailfunc):

    import smtplib

    filename = "alerts.csv"

    f = open(filename,"w")
    f.write(alerts_line)
    f.close()

    f = open("mailconfig.json","w")
    f.write("""
    {
        "from":"from@example.com",
        "to":"to@example.com",
        "username":"from_user",
        "password":"from_password",
        "server":"smtp.gmail.com"
    }
    """)
    f.close()

    def mocklogin(cl, user, password):
        return True

    def mockreturn(cl, frm, to, msg):
        assert "from@example.com" == frm
        assert "to@example.com" == to
        assert "Price Drop" in msg
        #TODO Does this really work?

    monkeypatch.setattr(smtplib.SMTP, 'login', mocklogin)
    monkeypatch.setattr(smtplib.SMTP, 'sendmail', mockreturn)

    sys.argv = [
        "psnmailalert",
        ]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        # Call parameter
        mailfunc()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0 

    data = "" 
    with open(filename, 'r') as myfile:
        data = data + myfile.read()

    assert "" == data