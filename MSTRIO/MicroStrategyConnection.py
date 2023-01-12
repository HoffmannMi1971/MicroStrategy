from Constants import *
from mstrio.connection import Connection

def GetMicroStrategyConnection():
    mstr_conn = Connection(base_url=mstr_base_url, username=mstr_username, password=mstr_password, project_id=mstr_project_id)
    return mstr_conn  
