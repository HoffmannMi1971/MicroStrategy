import pyodbc
from MicroStrategyConnection import *
from mstrio.users_and_groups import UserGroup
from mstrio.access_and_security.security_role import SecurityRole
from mstrio.modeling.security_filter import SecurityFilter

#MSTR Connection
mstr_conn = GetMicroStrategyConnection()

#DB Connections
db_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
MSTR_UserGroup_Tbl_Cursor = db_conn.cursor()

MSTR_UserGroup_Tbl_Cursor.execute("select * from tbl_mstr_usergroup")

for row in MSTR_UserGroup_Tbl_Cursor:
    SelectedUserGroup = UserGroup(connection=mstr_conn, name=row.UserGroup)
    SelectedSecurityRole = SecurityRole(connection=mstr_conn, name=row.SecurityRole)
    SelectedSecurityFilter = SecurityFilter(connection=mstr_conn, name=row.SecurityFilter,)
    SelectedSecurityRole.grant_to(members = SelectedUserGroup, project = mstr_project_name)
    SelectedSecurityFilter.apply(SelectedUserGroup)

MSTR_UserGroup_Tbl_Cursor.close()
db_conn.close()
mstr_conn.close()