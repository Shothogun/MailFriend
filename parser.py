from dataclasses import field
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz


def parseEmailCall(lines):

    # lines stores each line of the original text of the message
    # so that you can get the original text of the entire message use the join function and lines variable.
    msg_content = b'\r\n'.join(lines).decode('utf8')

    msg_content = msg_content.replace('=C3=A7', 'ç')

    msg_content = msg_content.replace('=C3=80', 'À')
    msg_content = msg_content.replace('=C3=81', 'Á')
    msg_content = msg_content.replace('=C3=82', 'Â')
    msg_content = msg_content.replace('=C3=83', 'Ã')
    msg_content = msg_content.replace('=C3=A0', 'à')
    msg_content = msg_content.replace('=C3=A1', 'á')
    msg_content = msg_content.replace('=C3=A2', 'â')
    msg_content = msg_content.replace('=C3=A3', 'ã')

    msg_content = msg_content.replace('=C3=88', 'È')
    msg_content = msg_content.replace('=C3=89', 'É')
    msg_content = msg_content.replace('=C3=8A', 'Ê')
    msg_content = msg_content.replace('=C3=8B', 'Ë')
    msg_content = msg_content.replace('=C3=A8', 'è')
    msg_content = msg_content.replace('=C3=A9', 'é')
    msg_content = msg_content.replace('=C3=AA', 'ê')
    msg_content = msg_content.replace('=C3=AB', 'ë')

    msg_content = msg_content.replace('=C3=88', 'Ì')
    msg_content = msg_content.replace('=C3=89', 'Í')
    msg_content = msg_content.replace('=C3=8A', 'Î')
    msg_content = msg_content.replace('=C3=8B', 'Ï')
    msg_content = msg_content.replace('=C3=AC', 'ì')
    msg_content = msg_content.replace('=C3=AD', 'í')
    msg_content = msg_content.replace('=C3=AE', 'î')
    msg_content = msg_content.replace('=C3=BF', 'ï')

    msg_content = msg_content.replace('=C3=92', 'Ò')
    msg_content = msg_content.replace('=C3=93', 'Ó')
    msg_content = msg_content.replace('=C3=94', 'Ô')
    msg_content = msg_content.replace('=C3=95', 'Õ')
    msg_content = msg_content.replace('=C3=96', 'Ö')
    msg_content = msg_content.replace('=C3=B2', 'ò')
    msg_content = msg_content.replace('=C3=B3', 'ó')
    msg_content = msg_content.replace('=C3=B4', 'ô')
    msg_content = msg_content.replace('=C3=B5', 'õ')
    msg_content = msg_content.replace('=C3=B6', 'ö')

    msg_content = msg_content.replace('=C3=99', 'Ù')
    msg_content = msg_content.replace('=C3=9A', 'Ú')
    msg_content = msg_content.replace('=C3=9B', 'Û')
    msg_content = msg_content.replace('=C3=9C', 'Ü')
    msg_content = msg_content.replace('=C3=B9', 'ù')
    msg_content = msg_content.replace('=C3=BA', 'ú')
    msg_content = msg_content.replace('=C3=BB', 'û')
    msg_content = msg_content.replace('=C3=BC', 'ü')

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
    msg_lines = msg_content.split('\n')
    date = re.search(r"Date: (.*)\r", msg_content).groups()[0][5:24]
    date = datetime.strptime(date, "%d %b %Y %H:%M:%S")
    timezone = pytz.timezone("UTC")
    date = timezone.localize(date).astimezone(
        pytz.timezone("America/Sao_Paulo"))

    soup = BeautifulSoup(msg_content, 'html.parser')
    email_from = ""

    if (re.search(r"\(LHLO (.*)\)", msg_lines[1]) != None):
        email_from = re.search(r"\(LHLO (.*)\)", msg_lines[1]).groups()[0]

    fields = [a.string for a in soup.find_all(attrs={"width": "3D\"200\""})]
    values = [
        a.contents[0] for a in soup.find_all(attrs={"width": "3D\"410\""})
    ]

    if len(values) == 0:
        fields = [a.string for a in soup.find_all(attrs={"width": "200"})]
        values = [a.contents[0] for a in soup.find_all(attrs={"width": "410"})]

    # print(soup.prettify())

    fields.append('callmaildate')
    values.append(date)

    return fields, values, email_from


def createCall(keys, values):
    call = {}
    keys = [
        'callcode', 'organization', 'calltype', 'status', 'category',
        'subcategory', 'slaaimdate', 'answeraimdate', 'answered', 'answerdate',
        'conectivityfailtime', 'conectivitynormalizationtime', 'registerdate',
        'description', 'slapausebeginningdate', 'slapausefinishdate',
        'callmaildate'
    ]

    if len(values) < 6:
        keys = [
            'callcode', 'registerdate', 'description', 'organization',
            'callmaildate'
        ]

    for i in range(len(values)):
        print(values[i])
        if keys[i] == 'answered':
            call[keys[i]] = True if values[i] == 'Yes' else False
        else:
            call[keys[i]] = '\'{0}\''.format(values[i])

        # print(keys[i], ':', values[i])

    return call