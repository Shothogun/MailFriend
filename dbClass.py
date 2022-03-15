from pickle import NONE
import psycopg2
from psycopg2 import sql
from config import config


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
            params = config()

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
        if self.callExists(call['callcode']):
            self.updateCall(call)
        else:
            self.insertCall(call)

    def insertCall(self, call):
        if len(call) < 5:
            call['calltype'] = 'NULL'
            call['status'] = 'NULL'
            call['category'] = 'NULL'
            call['subcategory'] = 'NULL'
            call['slaaimdate'] = '\'(empty)\''
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

        self.cur.execute('''
            INSERT INTO 
                calls
                (callcode, organization, calltype, status,
                 category, subcategory, slaaimdate, answeraimdate,
                 answered, answerdate, conectivityfailtime, conectivitynormalizationtime,
                 registerdate, description, slapausebeginningdate, 
                 slapausefinishdate)
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
                 slapausefinishdate, callid)
            VALUES
                ({0}, {1}, {2}, {3},
                 {4}, {5}, {6}, {7},
                 {8}, {9}, {10}, {11},
                 {12}, {13}, {14}, {15}, {16});
        '''.format(call['callcode'], call['organization'], call['calltype'],
                   call['status'], call['category'], call['subcategory'],
                   call['slaaimdate'], call['answeraimdate'], call['answered'],
                   call['answerdate'], call['conectivityfailtime'],
                   call['conectivitynormalizationtime'], call['registerdate'],
                   call['description'], call['slapausebeginningdate'],
                   call['slapausefinishdate'], callID))

        self.conn.commit()

    def updateCall(self, call):
        callID = self.getCallIDByCode(call['callcode'].replace('\'', ''))

        time_types = [
            'slaaimdate', 'answeraimdate', 'answerdate', 'conectivityfailtime',
            'conectivitynormalizationtime', 'registerdate',
            'slapausebeginningdate', 'slapausefinishdate'
        ]

        if len(call) < 5:
            call['calltype'] = 'NULL'
            call['status'] = 'NULL'
            call['category'] = 'NULL'
            call['subcategory'] = 'NULL'
            call['slaaimdate'] = '\'(empty)\''
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

        self.cur.execute('''
            INSERT INTO 
                calllogs
                (callcode, organization, calltype, status,
                 category, subcategory, slaaimdate, answeraimdate,
                 answered, answerdate, conectivityfailtime, conectivitynormalizationtime,
                 registerdate, description, slapausebeginningdate, 
                 slapausefinishdate, callid)
            VALUES
                ({0}, {1}, {2}, {3},
                 {4}, {5}, {6}, {7},
                 {8}, {9}, {10}, {11},
                 {12}, {13}, {14}, {15}, {16});
        '''.format(call['callcode'], call['organization'], call['calltype'],
                   call['status'], call['category'], call['subcategory'],
                   call['slaaimdate'], call['answeraimdate'], call['answered'],
                   call['answerdate'], call['conectivityfailtime'],
                   call['conectivitynormalizationtime'], call['registerdate'],
                   call['description'], call['slapausebeginningdate'],
                   call['slapausefinishdate'], callID))

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
                   call['category'], call['subcategory'], call['slaaimdate'],
                   call['answeraimdate'], call['answered'], call['answerdate'],
                   call['conectivityfailtime'],
                   call['conectivitynormalizationtime'], call['registerdate'],
                   call['description'], call['slapausebeginningdate'],
                   call['slapausefinishdate'], call['callcode']))

        self.conn.commit()

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

    def pullCalls(self, n: int):
        self.cur.execute('''SELECT * FROM calls''')

        calls = []
        for _ in range(n):
            value = self.cur.fetchone()
            calls.append({
                "callcode": value[1],
                "organization": value[2],
                "calltype": value[3],
                'status': value[4],
                'category': value[5],
                'subcategory': value[6],
                'slaaimdate': value[7],
                'answeraimdate': value[8],
                'answered': value[9],
                'answerdate': value[10],
                'conectivityfailtime': value[11],
                'conectivitynormalizationtime': value[12],
                'registerdate': value[13],
                'description': value[14],
                'slapausebeginningdate': value[15],
                'slapausefinishdate': value[16]
            })

        return calls
