import pyodbc
from MicroStrategyConnection import *
from mstrio.users_and_groups import User

#MSTR Connection
mstr_conn = GetMicroStrategyConnection()

#DB Connections
db_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
db_temp_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
MSTR_User_Tbl_Cursor = db_conn.cursor()
MSTR_User_Tbl_Update_Cursor = db_temp_conn.cursor()

MSTR_User_Tbl_Cursor.execute("select * from tbl_mstr_user")

for row in MSTR_User_Tbl_Cursor:
    #Create New User if ID Column in DB is empty
    if(row.ID==None):
        #Create MSTR User and read generated MicroStrategy ID
        NewUser=User.create(connection=mstr_conn, username=row.Username, full_name=row.Fullname, password=row.Password)
        #Create default Mail Address for new User
        NewUser.add_address(name='Default E-Mail Address', address=row.EMail, default=True)
        
        #Update ID in Database for created User
        SQLStatement="update tbl_mstr_user set ID='" + NewUser.id + "' where Username='" + row.Username + "'"
        MSTR_User_Tbl_Update_Cursor.execute(SQLStatement)
        db_temp_conn.commit()
    #Update User and default Mail Adress because User ID is already there
    else:
        UserToChange = User(connection=mstr_conn, id=row.ID)
        #Change User Properties
        UserToChange.alter(username=row.Username, full_name=row.Fullname, password=row.Password)
        #Change User Default Address
        AddressToChange=UserToChange.addresses[0]
        UserToChange.update_address(id=AddressToChange['id'], name='Default E-Mail Address', address=row.EMail, default=True)

MSTR_User_Tbl_Cursor.close()
MSTR_User_Tbl_Update_Cursor.close()
db_conn.close()
db_temp_conn.close()
mstr_conn.close()