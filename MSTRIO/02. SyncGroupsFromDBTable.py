from MicroStrategyConnection import *
import pyodbc
from mstrio.users_and_groups import User, UserGroup

#MSTR Connection
mstr_conn = GetMicroStrategyConnection()

#DB Connections
db_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
db_temp_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
MSTR_UserGroup_Tbl_Cursor = db_conn.cursor()
MSTR_UserGroup_Tbl_Update_Cursor = db_temp_conn.cursor()

MSTR_UserGroup_Tbl_Cursor.execute("select * from tbl_mstr_usergroup")

for row in MSTR_UserGroup_Tbl_Cursor:
    #Create New UserGroup if ID Column in DB is empty
    if(row.ID==None):
        #Create MSTR UserGroup and read generated MicroStrategy ID
        NewUserGroup=UserGroup.create(connection=mstr_conn, name=row.UserGroup)
  
        #Update ID in Database for created UserGroup
        SQLStatement="update tbl_mstr_usergroup set ID='" + NewUserGroup.id + "' where UserGroup='" + row.UserGroup + "'"
        MSTR_UserGroup_Tbl_Update_Cursor.execute(SQLStatement)
        db_temp_conn.commit()
    #Update UserGroup because UserGroup ID is already there
    else:
        UserGroupToChange = UserGroup(connection=mstr_conn, id=row.ID)
        #Change UserGroup Properties
        UserGroupToChange.alter(name=row.UserGroup)

MSTR_UserGroup_Tbl_Cursor.close()
MSTR_UserGroup_Tbl_Update_Cursor.close()
db_conn.close()
db_temp_conn.close()
mstr_conn.close()        
