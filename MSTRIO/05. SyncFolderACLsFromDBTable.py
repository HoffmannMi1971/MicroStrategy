from MicroStrategyConnection import *
import pyodbc
from mstrio.users_and_groups import UserGroup
from mstrio.object_management import Folder
from mstrio.utils.entity import Rights

#MSTR Connection
mstr_conn = GetMicroStrategyConnection()

#DB Connections
db_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MSTR_DEMO;UID=sa;PWD=QRIDLA6t')
MSTR_Folder_ACLs_Cursor = db_conn.cursor()

MSTR_Folder_ACLs_Cursor.execute("select * from tbl_mstr_acls_folder_groups")

for row in MSTR_Folder_ACLs_Cursor:
    SelectedUserGroup = UserGroup(connection=mstr_conn, name=row.UserGroup)
    SelectedFolder = Folder(connection=mstr_conn, id=row.FolderID)
    SelectedAccessType = row.AccessType

    if(SelectedAccessType=='Consumer'):
        SelectedFolder.acl_add(rights=Rights.BROWSE | Rights.READ | Rights.USE | Rights.EXECUTE, trustees=SelectedUserGroup)
        SelectedFolder.acl_add(rights=Rights.BROWSE | Rights.READ | Rights.USE | Rights.EXECUTE, trustees=SelectedUserGroup, inheritable=True, propagate_to_children=True)
    else:
        SelectedFolder.acl_add(rights=Rights.BROWSE | Rights.READ | Rights.USE | Rights.EXECUTE | Rights.WRITE | Rights.DELETE | Rights.CONTROL, trustees=SelectedUserGroup)
        SelectedFolder.acl_add(rights=Rights.BROWSE | Rights.READ | Rights.USE | Rights.EXECUTE | Rights.WRITE | Rights.DELETE | Rights.CONTROL, trustees=SelectedUserGroup, inheritable=True, propagate_to_children=True)

MSTR_Folder_ACLs_Cursor.close()
db_conn.close()
mstr_conn.close()