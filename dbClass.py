from time import time
import os
import psycopg2
from psycopg2 import sql
from config import config
from datetime import date, datetime
from classifier import classifyTicket, updateRemainingTime


class dbClass:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.time_types = [
            'slaaimdate', 'answeraimdate', 'answerdate', 'conectivityfailtime',
            'conectivitynormalizationtime', 'registerdate',
            'slapausebeginningdate', 'slapausefinishdate'
        ]

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config(filename=os.environ['CONFIG_PATH'])

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            # create a cursor
            self.cur = self.conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            self.cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cur.fetchone()
            print(db_version)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        self.cur.close()
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def pushCall(self, call):
        if not self.callExists(call['callcode']):
            self.insertCall(call)
        elif not self.callLogExists(call['callcode'], call['callmaildate']):
            self.updateCall(call)

    def insertCall(self, call):
        if len(call) < 6:
            call['calltype'] = 'NULL'
            call['status'] = 'NULL'
            call['category'] = 'NULL'
            call['subcategory'] = 'NULL'
            call['slaaimdate'] = '\'(empty)\''
            call['registerdate'] = '\'(empty)\''
            call['answeraimdate'] = '\'(empty)\''
            call['answered'] = 'NULL'
            call['answerdate'] = '\'(empty)\''
            call['conectivityfailtime'] = '\'(empty)\''
            call['conectivitynormalizationtime'] = '\'(empty)\''
            call['slapausebeginningdate'] = '\'(empty)\''
            call['slapausefinishdate'] = '\'(empty)\''

        for tt in self.time_types:
            if (call[tt] == '\'(empty)\''):
                call[tt] = 'NULL'
            else:
                call[tt] = 'timestamp ' + call[tt]

        try:

            self.cur.execute('''
                INSERT INTO 
                    calls
                    (callcode, organization, calltype, status,
                    category, subcategory, slaaimdate, answeraimdate,
                    answered, answerdate, conectivityfailtime, conectivitynormalizationtime,
                    registerdate, description, slapausebeginningdate, slapausefinishdate)
                VALUES
                    ({0}, {1}, {2}, {3},
                    {4}, {5}, {6}, {7},
                    {8}, {9}, {10}, {11},
                    {12}, {13}, {14}, {15});
            '''.format(call['callcode'], call['organization'], call['calltype'],
                    call['status'], call['category'], call['subcategory'],
                    call['slaaimdate'], call['answeraimdate'], call['answered'],
                    call['answerdate'], call['conectivityfailtime'],
                    call['conectivitynormalizationtime'], call['registerdate'],
                    call['description'], call['slapausebeginningdate'],
                    call['slapausefinishdate']))

            callID = self.getCallIDByCode(call['callcode'].replace('\'', ''))

            self.cur.execute('''
                INSERT INTO 
                    calllogs
                    (callcode, organization, calltype, status,
                    category, subcategory, slaaimdate, answeraimdate,
                    answered, answerdate, conectivityfailtime, conectivitynormalizationtime,
                    registerdate, description, slapausebeginningdate, 
                    slapausefinishdate, callid, callmaildate)
                VALUES
                    ({0}, {1}, {2}, {3},
                    {4}, {5}, {6}, {7},
                    {8}, {9}, {10}, {11},
                    {12}, {13}, {14}, {15}, {16}, {17});
            '''.format(call['callcode'], call['organization'], call['calltype'],
                    call['status'], call['category'], call['subcategory'],
                    call['slaaimdate'], call['answeraimdate'], call['answered'],
                    call['answerdate'], call['conectivityfailtime'],
                    call['conectivitynormalizationtime'], call['registerdate'],
                    call['description'], call['slapausebeginningdate'],
                    call['slapausefinishdate'], callID, call['callmaildate']))

            self.conn.commit()

        except Exception:
            pass

    def updateCall(self, call):
        callID = self.getCallIDByCode(call['callcode'].replace('\'', ''))

        time_types = [
            'slaaimdate', 'answeraimdate', 'answerdate', 'conectivityfailtime',
            'conectivitynormalizationtime', 'registerdate',
            'slapausebeginningdate', 'slapausefinishdate'
        ]

        if len(call) < 6:
            call['calltype'] = 'NULL'
            call['status'] = 'NULL'
            call['category'] = 'NULL'
            call['subcategory'] = 'NULL'
            call['slaaimdate'] = '\'(empty)\''
            call['registerdate'] = '\'(empty)\''
            call['answeraimdate'] = '\'(empty)\''
            call['answered'] = 'NULL'
            call['answerdate'] = '\'(empty)\''
            call['conectivityfailtime'] = '\'(empty)\''
            call['conectivitynormalizationtime'] = '\'(empty)\''
            call['slapausebeginningdate'] = '\'(empty)\''
            call['slapausefinishdate'] = '\'(empty)\''

        for tt in time_types:
            if (call[tt] == '\'(empty)\''):
                call[tt] = 'NULL'
            else:
                call[tt] = 'timestamp ' + call[tt]

        try:

            self.cur.execute('''
                INSERT INTO 
                    calllogs
                    (callcode, organization, calltype, status,
                    category, subcategory, slaaimdate, answeraimdate,
                    answered, answerdate, conectivityfailtime, conectivitynormalizationtime,
                    registerdate, description, slapausebeginningdate, 
                    slapausefinishdate, callid, callmaildate)
                VALUES
                    ({0}, {1}, {2}, {3},
                    {4}, {5}, {6}, {7},
                    {8}, {9}, {10}, {11},
                    {12}, {13}, {14}, {15}, {16}, {17});
            '''.format(
                call['callcode'], call['organization'], call['calltype'],
                call['status'], call['category'], call['subcategory'],
                call['slaaimdate'], call['answeraimdate'], call['answered'],
                call['answerdate'], call['conectivityfailtime'],
                call['conectivitynormalizationtime'], call['registerdate'],
                call['description'], call['slapausebeginningdate'],
                call['slapausefinishdate'], callID, call['callmaildate']))

            self.cur.execute('''
                UPDATE calls
                SET organization = {0}, calltype = {1}, status = {2}, category = {3}, 
                    subcategory = {4}, slaaimdate = {5}, answeraimdate = {6},
                    answered = {7}, answerdate = {8}, conectivityfailtime = {9}, 
                    conectivitynormalizationtime = {10}, registerdate = {11}, 
                    description = {12}, slapausebeginningdate = {13}, 
                    slapausefinishdate =  {14}
                WHERE callcode = {15}
            '''.format(call['organization'], call['calltype'], call['status'],
                       call['category'], call['subcategory'],
                       call['slaaimdate'], call['answeraimdate'],
                       call['answered'], call['answerdate'],
                       call['conectivityfailtime'],
                       call['conectivitynormalizationtime'],
                       call['registerdate'], call['description'],
                       call['slapausebeginningdate'],
                       call['slapausefinishdate'], call['callcode']))

            self.conn.commit()

        except Exception:
            pass

    def getCallIDByCode(self, code):
        self.cur.execute(
            '''
                SELECT * FROM calls WHERE callcode = %s
                ''', (code, ))
        call = self.cur.fetchone()

        # 2nd field from CallLogs: CallID
        return call[0]

    def callExists(self, code):
        self.cur.execute('''
            SELECT * FROM calls where callcode = {0};
        '''.format(code))

        if self.cur.fetchone() == None:
            return False
        else:
            return True

    def closedCallExists(self, code):
        code.replace('\'', '')
        self.cur.execute('''
            SELECT * FROM calls where callcode = '{0}'
            AND status != 'Fechado'  AND
            status != 'Encaminhado';
        '''.format(code))

        if self.cur.fetchone() == None:
            return False
        else:
            return True

    def callLogExists(self, code, date):
        self.cur.execute('''
            SELECT * FROM calllogs where callcode = {0} AND
            callmaildate = {1};
        '''.format(code, date))

        if self.cur.fetchone() == None:
            return False
        else:
            return True

    def ticketPriorityClassify(self, ticket):
        if ticket['subcategory'] == "Indisponibilidade":
            return "Alta"

        db = dbClass()

        db.connect()

        exists = db.closedCallExists(ticket['ID'])

        db.close()

        if exists:
            return "Medio"

        else:
            return "Baixo"

    def pullCalls(self, n: int):
        self.cur.execute('''SELECT * FROM calls 
                            WHERE status != 'Fechado' AND
                            status != 'Encaminhado' ''')

        calls = []

        for i in range(n):
            ticket = self.cur.fetchone()
            if ticket == None:
                continue

            ticket_parsed = {
                'N':
                i,
                'ID':
                ticket[1],
                'Organização':
                ticket[2],
                'Tipo':
                ticket[3],
                'Status':
                ticket[4],
                'Categoria':
                ticket[5],
                'subcategory':
                ticket[6],
                'Data_Alvo_SLA':
                None if ticket[7] == None else
                ticket[7].strftime("%-d/%-m/%Y %H:%M:%S"),
                'Data_Alvo_Resp':
                None if ticket[8] == None else
                ticket[8].strftime("%-d/%-m/%Y %H:%M:%S"),
                'Respondido':
                "Sim" if ticket[9] else "Não",
                'Data_Resp':
                ticket[10].strftime("%-d/%-m/%Y %H:%M:%S"),
                'Hora_Falha':
                None if ticket[11] == None else
                ticket[11].strftime("%H:%M:%S %-d/%-m/%Y"),
                'Hora_Normalizacao':
                None if ticket[12] == None else
                ticket[12].strftime("%H:%M:%S %-d/%-m/%Y"),
                'Data_do_Registro':
                None if ticket[13] == None else
                ticket[13].strftime("%-d/%-m/%Y %H:%M:%S"),
                'Breve_Descricao':
                ticket[14],
                'Pausa_SLA_inicio':
                ticket[15],
                'Pausa_SLA_FIM':
                ticket[16],
                'Tempo_Restante':
                0
            }

            priority = self.ticketPriorityClassify(ticket_parsed)

            call = {
                'N': i,
                'ID': ticket_parsed['ID'],
                'Organização': ticket_parsed['Organização'],
                'Tipo': ticket_parsed['Tipo'],
                'Status': ticket_parsed['Status'],
                'Respondido': ticket_parsed['Respondido'],
                'Data_do_Registro': ticket_parsed['Data_do_Registro'],
                'Breve_Descricao': ticket_parsed['Breve_Descricao'],
                'Tempo_Restante': 0,
                'Prioridade': priority
            }

            calls.append(call)

        return calls

    def pullTicketData(self, n: int):
        calls = self.pullCalls(n)

        current_month = datetime.now().month
        current_year = datetime.now().year

        self.cur.execute(
            '''SELECT COUNT(*) FROM calls 
                            WHERE registerdate >= '1/%s/%s' 
        ''', (current_month, current_year))
        n_tickets_last_month = self.cur.fetchone()

        calls = [(classifyTicket(call)) for call in calls]

        calls = [(updateRemainingTime(call)) for call in calls]

        calls_abertos = [call[0] for call in calls if call[1] == 'A']
        calls_breves = [call[0] for call in calls if call[1] == 'B']
        calls_vencidos = [call[0] for call in calls if call[1] == 'V']

        aberto_size = len(calls_abertos)
        breve_size = len(calls_breves)
        vencido_size = len(calls_vencidos)
        total_size = aberto_size + breve_size + vencido_size

        ticketData = {
            'Info_Geral': {
                'N_Tickets_Recentes': aberto_size,
                'N_Tickets_Perto_Vencer': breve_size,
                'N_Tickets_Vencidos': vencido_size,
                'N_Tickets_Ultimo_Mes': n_tickets_last_month[0],
                'N_Tickets_Total': total_size,
                'Ultimo_Fetch': datetime.now().strftime('%H:%M:%S %d/%m')
            },
            'Lista_Abertos': calls_abertos,
            'Lista_Breve': calls_breves,
            'Lista_Vencidos': calls_vencidos
        }

        return ticketData
