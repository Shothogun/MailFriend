from pprint import pprint
import psycopg2
from config import config


def initDatabase():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        cur.execute('CREATE TABLE Calls (\
                        CallID SERIAL, \
                        CallCode VARCHAR(30),\
                        Organization VARCHAR(50), \
                        CallType VARCHAR(30), \
                        Status VARCHAR(30), \
                        Category VARCHAR(30), \
                        SubCategory VARCHAR(30), \
                        SlaAimDate TIMESTAMP, \
                        AnswerAimDate TIMESTAMP, \
                        ANSWERED BOOLEAN, \
                        AnswerDate TIMESTAMP, \
                        ConectivityFailTime TIMESTAMP, \
                        ConectivityNormalizationTime TIMESTAMP, \
                        RegisterDate TIMESTAMP, \
                        Description VARCHAR(100), \
                        SlaPauseBeginningDate TIMESTAMP, \
                        SlaPauseFinishDate TIMESTAMP );')
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    initDatabase()