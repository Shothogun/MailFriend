# import python poplib module
import poplib
from datetime import datetime
from bs4 import BeautifulSoup
import html
import os
import dbClass


def parseEmailCall(lines):

    # lines stores each line of the original text of the message
    # so that you can get the original text of the entire message use the join function and lines variable.
    msg_content = b'\r\n'.join(lines).decode('utf-8')

    msg_content = msg_content.replace('=09', '')
    msg_content = msg_content.replace('=E7', 'ç')

    msg_content = msg_content.replace('=C0', 'À')
    msg_content = msg_content.replace('=C1', 'Á')
    msg_content = msg_content.replace('=C2', 'Â')
    msg_content = msg_content.replace('=C3', 'Ã')
    msg_content = msg_content.replace('=E0', 'à')
    msg_content = msg_content.replace('=E1', 'á')
    msg_content = msg_content.replace('=E2', 'â')
    msg_content = msg_content.replace('=E3', 'ã')

    msg_content = msg_content.replace('=C9', 'É')
    msg_content = msg_content.replace('=CA', 'Ê')
    msg_content = msg_content.replace('=E9', 'é')
    msg_content = msg_content.replace('=EA', 'ê')

    msg_content = msg_content.replace('=CD', 'Í')
    msg_content = msg_content.replace('=CE', 'Î')
    msg_content = msg_content.replace('=ED', 'í')
    msg_content = msg_content.replace('=EE', 'î')

    msg_content = msg_content.replace('=D3', 'Ó')
    msg_content = msg_content.replace('=D4', 'Ô')
    msg_content = msg_content.replace('=F3', 'ó')
    msg_content = msg_content.replace('=F4', 'ô')

    msg_content = msg_content.replace('=DA', 'Ú')
    msg_content = msg_content.replace('=DB', 'Û')
    msg_content = msg_content.replace('=FA', 'ú')
    msg_content = msg_content.replace('=FB', 'û')

    msg_content = msg_content.replace('=\r\n', '')

    soup = BeautifulSoup(msg_content, 'html.parser')

    print(soup.prettify())
    fields = [a.string for a in soup.find_all(attrs={"width": "3D\"200\""})]
    values = [a.contents[0] for a in soup.find_all(attrs={"width": "3D\"410\""})]

    return fields, values


def createCall(keys, values):
    call = {}
    keys = [
        'callcode', 'organization', 'calltype', 'status', 'category',
        'subcategory', 'slaaimdate', 'answeraimdate', 'answered', 'answerdate',
        'conectivityfailtime', 'conectivitynormalizationtime', 'registerdate',
        'description', 'slapausebeginningdate', 'slapausefinishdate'
    ]

    if len(values) < 5:
        keys = ['callcode', 'registerdate', 'description', 'organization']

    for i in range(len(values)):
        print(keys[i], ':', values[i])
        call[keys[i]] = '\'{0}\''.format(values[i])

    return call


# input email address, password and pop3 server domain or ip address
# email = input('Email: ')
# password = input('Password: ')
# pop3_server = input('POP3 server: ')

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

amount = int(input("How many last recently received emails? "))

calls = []

for i in range(index - amount + 1, index+1):
    print("==== Email:", i, "=====")
    resp, lines, octets = server.retr(i)
    fields, values = parseEmailCall(lines)
    calls.append(createCall(fields, values))

server.quit()

db = dbClass.dbClass()

db.connect()

for c in calls:
    db.pushCall(c)

db.close()