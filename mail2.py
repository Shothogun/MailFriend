# import python poplib module
import poplib
from datetime import datetime
from bs4 import BeautifulSoup
import os
import dbClass
import parser


def mail_fetch():
    # input email address, password and pop3 server domain or ip address
    email = os.environ['MAIL_USERNAME']
    password = os.environ['MAIL_PASSWORD']
    pop3_server = os.environ['POP3_SERVER']

    # connect to pop3 server:
    server = poplib.POP3(pop3_server)

    # open debug switch to print debug information between client and pop3 server.
    server.set_debuglevel(1)

    # get pop3 server welcome message.
    pop3_server_welcome_msg = server.getwelcome().decode('utf-8')

    # print out the pop3 server welcome message.
    print(server.getwelcome().decode('utf-8'))

    # Stablish Stls protocol
    server.stls()

    # user account authentication
    server.user(email)
    server.pass_(password)

    # stat() function return email count and occupied disk size
    print('Messages: %s. Size: %s' % server.stat())

    # list() function return all email list
    resp, mails, octets = server.list()

    # retrieve the newest email index number
    index = len(mails)

    # server.retr function can get the contents of the email with index variable value index number.
    amount = 30

    calls = []

    # Pull emails and parsing
    for i in range(index - amount + 1, index + 1):
        print("==== Email:", i, "=====")
        resp, lines, octets = server.retr(i)
        fields, values, email_from = parser.parseEmailCall(lines)

        if (email_from == "noreply-atendimento@rnp.br"
                or email_from == "atendimento@rnp.br"
                or email_from == "sla@gigacandanga.net.br>"
                or email_from == "matheus.bawden@gigacandanga.net.br"):
            calls.append(parser.createCall(fields, values))

    server.quit()

    # DB connection and
    db = dbClass.dbClass()

    db.connect()

    for c in calls:
        db.pushCall(c)

    db.close()


def main():
    mail_fetch()
    print(datetime.now())


if __name__ == "__main__":
    main()
