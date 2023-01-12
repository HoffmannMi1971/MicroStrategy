from MicroStrategyConnection import *
from mstrio.users_and_groups import list_users, User, UserGroup, list_user_groups
from mstrio.project_objects import SuperCube
from mstrio.object_management import quick_search
from mstrio.types import ObjectSubTypes
import pandas as pd

#MSTR Connection
mstr_conn = GetMicroStrategyConnection()

mstr_user_and_groups_cube_name = '_MSTR_USERS_AND_GROUPS_ICUBE_'
mstr_user_table_name_in_cube = 'MSTR User'
mstr_usergroup_table_name_in_cube = 'MSTR User Groups'
mstr_usergroupmembership_table_name_in_cube = 'MSTR User Groups Memberships'

#Get User Infos
#--------------
mstr_users = list_users(mstr_conn)
list_userid=[]
list_username=[]
list_fulname=[]
list_email=[]
list_datecreated=[]

print("\nRead User Info:\n")

for selUser in mstr_users:
    print('Read User:', selUser.username)
    list_userid.append(selUser.id)
    list_username.append(selUser.username)
    list_fulname.append(selUser.full_name)
    try:
        UserDefaultAddress=selUser.addresses[0]
    except:
        list_email.append('no E-Mail')
    else:
        list_email.append(UserDefaultAddress['value'])
    list_datecreated.append(str((selUser._date_created))[0:10])

#Get UserGroup Infos
#-------------------
mstr_usergroups = list_user_groups(mstr_conn)
list_usergroupid=[]
list_usergroup=[]
list_usergroup_datecreated = []

print("\nRead UserGroup Info:\n")

for selUserGroup in mstr_usergroups:
    print('Read UserGroup:', selUserGroup.name)
    list_usergroupid.append(selUserGroup.id)
    list_usergroup.append(selUserGroup.name)
    list_usergroup_datecreated.append(str((selUserGroup._date_created))[0:10])

#Get Group Membership Infos
#--------------------------
list_MembershipUserName=[]
list_MembershipUserGroupName=[]

print("\nRead UserGroup Membership Info:\n")

for selUserGroup in mstr_usergroups:
    selUserListFromGroup = selUserGroup.list_members()
    for selUser in selUserListFromGroup:
        try:{
            list_MembershipUserName.append(selUser['username'])}
        except:{
            list_MembershipUserName.append(selUser['abbreviation'])}

        list_MembershipUserGroupName.append(selUserGroup.name)
        print(list_MembershipUserGroupName[-1],'-', list_MembershipUserName[-1])

#Create User Dataframe
Users_DF = pd.DataFrame(list(zip(list_username, list_fulname, list_userid, list_email, list_datecreated)),
                        columns=['Username', 'Full Name', 'User ID', 'User E-Mail', 'User Date Created'])
Users_DF['User Date Created'] = pd.to_datetime(Users_DF['User Date Created'])

#Create User Group Dataframe
UserGroups_DF = pd.DataFrame(list(zip(list_usergroup, list_usergroupid, list_usergroup_datecreated)),
                        columns=['User Group Name', 'User Group ID', 'User Group Date Created'])
UserGroups_DF['User Group Date Created'] = pd.to_datetime(UserGroups_DF['User Group Date Created'])

#Create User Group Membership Dataframe
UserGroupsMemberships_DF = pd.DataFrame(list(zip(list_MembershipUserGroupName, list_MembershipUserName)), columns=['User Group Name', 'Username'])

#Check if SuperCube is already available
FoundObjectSuperCube = quick_search(mstr_conn, mstr_project_id, name=mstr_user_and_groups_cube_name, object_types=ObjectSubTypes.SUPER_CUBE)

try:
    #Update iCube
    Users_And_Groups_iCube = SuperCube(connection=mstr_conn, id=FoundObjectSuperCube[0]['id'])
    Users_And_Groups_iCube.add_table(name=mstr_user_table_name_in_cube, data_frame=Users_DF, update_policy="replace")
    Users_And_Groups_iCube.add_table(name=mstr_usergroup_table_name_in_cube, data_frame=UserGroups_DF, update_policy="replace")
    Users_And_Groups_iCube.add_table(name=mstr_usergroupmembership_table_name_in_cube, data_frame=UserGroupsMemberships_DF, update_policy="replace")
    Users_And_Groups_iCube.update()
except:
    #Create new iCube
    Users_And_Groups_iCube = SuperCube(connection=mstr_conn, name=mstr_user_and_groups_cube_name)
    Users_And_Groups_iCube.add_table(name=mstr_user_table_name_in_cube, data_frame=Users_DF, update_policy="replace")
    Users_And_Groups_iCube.add_table(name=mstr_usergroup_table_name_in_cube, data_frame=UserGroups_DF, update_policy="replace")
    Users_And_Groups_iCube.add_table(name=mstr_usergroupmembership_table_name_in_cube, data_frame=UserGroupsMemberships_DF, update_policy="replace")
    Users_And_Groups_iCube.create()

mstr_conn.close()