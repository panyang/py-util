"""
      A simple command line to-do list. 

      The data is stored in a SQLite3 database in the same
      directory. 

"""
#=============================================================
# Send a text email
#=============================================================
import smtplib
from email.mime.text import MIMEText
import sys

COMMASPACE = ", "
def send_text_mail(to, subject, content):
    """ 
      Send a mail to the user using my gmail
    """
    assert type(to) == list
    
    from_string = "Zhi Han <zhi.han@gmail.com>"
    msg = MIMEText(content)
    msg['Subject']  = subject
    msg['To'] = COMMASPACE.join(to)
    msg['From'] = from_string

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('zhi.han@gmail.com', '2003cmu')
    mailServer.sendmail(from_string, to, msg.as_string() )
    mailServer.close()
    

#=============================================================
# ToDoItem is an item on the to do list
#=============================================================
import sqlite3
import sys

class ToDoItem: 
    """ An object for todo item """
    def __init__(self, income_tuple):
        if len(income_tuple)==2:
            self.title = income_tuple[0]
            self.description = income_tuple[1]
            self.t_id = -1
        else:
            self.t_id = income_tuple[0]
            self.title = income_tuple[1]
            self.description = income_tuple[2]
        

    def get_insert_string(self):
        command_string = "(?, ?)"
        value_string = (self.title, self.description)
        return (command_string, value_string)

    def display(self):
        print (str(self.t_id).ljust(4) + self.title.ljust(75) )

    def get_update_string(self):
        return ("title = ?, description = ?", (self.title, self.description))
                
    
    @staticmethod
    def get_columns():
        return "t_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
               "title TEXT, description TEXT"
    @staticmethod
    def get_value_columns():
        return "(title, description)"
    @staticmethod
    def get_id_column():
        return "t_id"
     
#=============================================================
# ToDoDB is the database for todo list
#=============================================================
class ToDoDB:
    """ A SQLite3 database to manage a simple todo list"""
    def __init__(self, dbSrc):
        # Connect to the database
        self.dbSrc = dbSrc
        self.connection = sqlite3.connect(dbSrc)
        self.cursor = self.connection.cursor()
   
        #

    def display_all(self, tableName):
        # List all the content of the table
        sqlString = "SELECT * FROM " + tableName
        self.cursor.execute(sqlString)
        
        # Create a list of objects
        records = self.cursor.fetchall()
        todos = []        
        for item in records:
            todos.append(ToDoItem(item))
        print('='*79)
        for t in todos:
            t.display()
        print('='*79)
        
     
    def create_table(self, tableName):
        sqlString = "CREATE TABLE " + tableName +\
                    "(" + ToDoItem.get_columns() + ")"
        self.cursor.execute(sqlString)

    def insert(self, tableName, item):
        sqlString = "INSERT INTO " + tableName
        formatAndValue = item.get_insert_string()
        sqlString = sqlString + item.get_value_columns() +\
                    " VALUES " + formatAndValue[0]
        self.cursor.execute(sqlString, formatAndValue[1])

    def delete(self, tableName, t_id):
        sqlString = "DELETE FROM " + tableName + \
                    " WHERE " + ToDoItem.get_id_column() + "=?"
        self.cursor.execute(sqlString, (t_id,))


    def get_for_id(self, tableName, t_id):
        sqlString = "SELECT * FROM " + tableName + \
                    " WHERE " + ToDoItem.get_id_column() + "=?"
        self.cursor.execute(sqlString, (t_id,))
        record = self.cursor.fetchone()
        item = ToDoItem(record) # Keep an eye
        return item

    def update(self, tableName, t_id, item):
        formatValues = item.get_update_string()
        format = formatValues[0]
        values = formatValues[1]
        sqlString = "UPDATE " + tableName + \
                    " SET " +  format + \
                    " WHERE " + ToDoItem.get_id_column() + "=?"
        self.cursor.execute(sqlString, (values[0], \
                                        values[1], t_id))

    def commit(self):
        self.connection.commit()

#==========================================================
# Utility functions
#==========================================================
def getline(s):
    str2 = s.splitlines()
    return str2[0]

def print_header():
    print("My To-do list: ")    

def print_instruction():
    print(" a - Add | u - Update | m - More |" + \
          " n - Notify | r - Archive | q - Quit " )

def print_table(db, table):
    print_header()
    db.display_all(table)
    print_instruction()

def create_db(filename):
    dbSrc = filename
    table = "todo"
    # Create some test data
    db = ToDoDB(dbSrc)
    db.create_table('todo')
    a = ToDoItem(('title1', 'desc'))
    b = ToDoItem(('title2', 'desc2'))
    db.insert(table, a)
    db.insert(table, b)
    return (db, table)

def create_test_db():
    return create_db(":memory:")

#==========================================================
# Functionalities
#==========================================================
def add_item(db, table):
    """ Add an item to the database"""
    print('Enter the title')
    line = sys.stdin.readline()
    title = getline(line)
    print("Enter the description")
    line = sys.stdin.readline()
    desc = getline(line)
    item = ToDoItem((title,desc))
    db.insert(table, item)


def delete_item(db, table):
    """ Delete a seleted item"""
    print('Select the item:')
    line = sys.stdin.readline()
    selected_id = int(getline(line))
    db.delete(table, selected_id)

def archive_item(db, table, archive_tbl):
    """ Archive a seleted item"""
    print('Select the item:')
    line = sys.stdin.readline()
    selected_id = int(getline(line))
    item = db.get_for_id(table, selected_id)
    db.delete(table, selected_id)
    db.insert(archive_tbl, item)
    

def update_item(db, table):
    """ Update a seleted item"""
    print('Select the item:')
    line = sys.stdin.readline()
    selected_id = int(getline(line))
    item = db.get_for_id(table, selected_id)
    
    # User interaction
    print("Old Title: " + item.title)
    print("New title:")
    line = sys.stdin.readline()
    item.title = getline(line)
    print("Old Description: " + item.description)
    print("New Description:")
    line = sys.stdin.readline()
    item.description = getline(line)
    
    # Update the record
    db.update(table, selected_id, item)
    
def display_more(db, table):
    """ Display more information on a selected item """
    print('Select the item:')
    line = sys.stdin.readline()
    selected_id = int(getline(line))
    item = db.get_for_id(table, selected_id)

    print("="*79)
    print("Title: " + item.title)
    print("\nDescription\n")
    print(item.description)
    print("="*79)
    print("Press [Enter] to return")
    line = sys.stdin.readline()
    
def send_notification(db, table):
    """ Send a notification email for a selected item """
    print('Select the item:')
    line = sys.stdin.readline()
    selected_id = int(getline(line))
    item = db.get_for_id(table, selected_id)

    print("Send an Email To:")
    dsts= sys.stdin.readline()
    dsts = getline(dsts)
    to = dsts.split(',')
    
    
    print('A one-line short message:')
    line = sys.stdin.readline()
    status_string = getline(line)
    # Synthesize the content of the email.
    content = "Item: " + item.title + "\n\n" + \
              status_string + "\n\n" \
              "--------------------------------- \n" + \
              "This is an automatically generated message."
              
    subject = "[TODO]" + item.title + " STATUS UPDATE"

    print(" Sending email message...")
    send_text_mail(to, subject, content)
    print(" Message sent")

# main
if (__name__ == "__main__"):
    
    # tp = create_test_db()
    # db = tp[0]
    # table = tp[1]
    if len(sys.argv) < 2:
        todo_table  = "todo"
    else:
        todo_table = sys.argv[1]

    db = ToDoDB("todo.db")
    
    # New tables
    someday_table = "someday"
    archive_table = "archive"
    
    # Prompt to select a table to work on 
    table = todo_table

    stop = False
    while (~stop):
        #main loop
        print_table(db, table)
        line = sys.stdin.readline()
        cmd = getline(line)
        if (cmd =='q'):
            stop = True
            break
        elif (cmd == 'a'):
            add_item(db, table)
        elif (cmd == 'd'):
            delete_item(db, table)
        elif (cmd == 'u'):
            update_item(db, table)
        elif (cmd == 'm'):
            display_more(db, table)
        elif (cmd == 'n'):
            send_notification(db, table)
        elif (cmd == 'r'):
            archive_item(db, table, archive_table)
    # At the end, commit to save the changes
    db.commit()

