import pyodbc
from MicroStrategyConnection import *
from mstrio.users_and_groups import User, UserGroup

#MSTR Connection
mstr_conn = GetMicroStrategyConnection()

#DB Connections
db_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
db_temp_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
MSTR_GroupsMemberships_Tbl_Cursor = db_conn.cursor()
MSTR_GroupsMemberships_Tbl_Update_Cursor = db_temp_conn.cursor()

MSTR_GroupsMemberships_Tbl_Cursor.execute("select * from tbl_mstr_group_membership")

for row in MSTR_GroupsMemberships_Tbl_Cursor:
    SelectedUser = User(connection=mstr_conn, username=row.Username)
    SelectedUserGroup = UserGroup(connection=mstr_conn, name=row.UserGroup)
    
    #Memberships created only if not yet in place
    SelectedUserGroup.add_users(users=[SelectedUser.id])

MSTR_GroupsMemberships_Tbl_Cursor.close()
MSTR_GroupsMemberships_Tbl_Update_Cursor.close()
db_conn.close()
db_temp_conn.close()
mstr_conn.close()    