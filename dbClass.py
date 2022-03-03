from pickle import NONE
import psycopg2
from config import config


class dbClass:
    def __init__(self):
        self.conn = None
        self.cur = None

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

    def insertCall(self, call):
        if self.callExists(call['callcode']):
            return 

        timeTypes = [
            'slaaimdate', 'answeraimdate', 'answerdate', 'conectivityfailtime',
            'conectivitynormalizationtime', 'registerdate',
            'slapausebeginningdate', 'slapausefinishdate'
        ]

        for tt in timeTypes:
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

        self.conn.commit()

    def callExists(self,code):
        self.cur.execute('''
            SELECT * FROM calls where callcode = {0};
        '''.format(code))

        if self.cur.fetchone() == None:
            return False
        else:
            return True
        