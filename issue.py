import sqlite3
import datetime
import time

def dict2string(fields):
    # create a comma-deliminated list of dictionary strings
    fieldlists = []
    for akey in fields:
        fieldlists.append(akey + " " + fields[akey])
    return ','.join(fieldlists)

def record2string(fields, values):
    fieldlists = []
    for akey in fields:
        if fields[akey]== 'TEXT':
                fieldlists.append('"' + values[akey] + '"')
        elif fields[akey]=='REAL':
                fieldlists.append('%f' % values[akey])
        elif fields[akey]=='INTEGER':
                fieldlists.append('%d' % values[akey])
    return ','.join(fieldlists)

class myDB:
    """ Creating my own table in SQLite database """
    def __init__(self, dbSrc):
        # connect to the database at initialization
        # the connection will be automatically closed when
        # the object is deleted
        self.dbSrc = dbSrc
        self.conn = sqlite3.connect(dbSrc)
        self.cur = self.conn.cursor()
        # load the field structures
        self.LoadIssueFields()
        # load the members
        self.LoadMembers()
        
    def LoadIssueFields(self):
        # table columns
        self.issueFields = {'owner': 'TEXT', \
                            'priority': 'INTEGER', \
                            'description': 'TEXT', \
                            'nextStep': 'TEXT', \
                            'log': 'TEXT', \
                            'due': 'REAL' }

    def LoadMembers(self):
        self.member = [{'name': 'Zhi', \
                        'email': 'zhi.han@gmail.com'}, \
                       {'name': 'Bo', \
                        'email': 'kellybosong@gmail.com'}]
        
    def CreateIssueTable(self, name):
        sqlstring = "CREATE TABLE " + name
        sqlstring = sqlstring + \
                    '(' + dict2string(self.issueFields) + ')'

        self.cur.execute(sqlstring)
        self.issueTableName = name
        
    def NewRecord(self):
        return {'owner': '', 'priority': 0, \
                'description': '', 'nextStep': '', \
                'log': '', 'due': time.time()}
    
    def InsertRecord(self, record):
        sqlstring = "INSERT INTO " +  self.issueTableName + " VALUES "
        sqlstring = sqlstring + \
                    "(" + record2string(self.issueFields, record) + \
                    ")"
        self.cur.execute(sqlstring)
        print "One record is added to the database."


class ToDoItem:
    """ To do item is a special kind of row in the table"""
    def __init__(self):
        self.description = ""
    @staticmethod
    def getColumns():
        return ("", )

