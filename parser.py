
from dataclasses import field
from bs4 import BeautifulSoup
import re 
from datetime import datetime
import pytz

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
    date = re.search(r"Date: (.*)\r", msg_content).groups()[0][5:-12]
    date = datetime.strptime(date, "%d %b %Y %H:%M:%S")
    timezone = pytz.timezone("UTC")
    date = timezone.localize(date).astimezone(pytz.timezone("America/Sao_Paulo"))

    soup = BeautifulSoup(msg_content, 'html.parser')

    # print(soup.prettify())
    fields = [a.string for a in soup.find_all(attrs={"width": "3D\"200\""})]
    values = [a.contents[0] for a in soup.find_all(attrs={"width": "3D\"410\""})]

    fields.append('callmaildate')
    values.append(date)

    return fields, values


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
        keys = ['callcode', 'registerdate', 'description', 'organization', 'callmaildate']

    for i in range(len(values)):
        if keys[i] == 'answered':
            call[keys[i]] = True if values[i] == 'Yes' else False  
        else:
            call[keys[i]] = '\'{0}\''.format(values[i])

        # print(keys[i], ':', values[i])

    return call