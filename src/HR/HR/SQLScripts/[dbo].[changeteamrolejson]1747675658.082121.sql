CREATE View [dbo].[ChangeTeamRoleJSON] As
Select '{"team_code":"'+ UTR.TeamCode  +'", "team_name":"'+ T.TeamName  +'",
"role_id":"'+ CAST(UTR.RoleId as varchar(5))  +'","role_name":"'+ R.RoleName  +'",
"level_id":"'+ CAST(ISNULL(UTR.LevelId_id,'') As varchar(1))  +'","level_name":"'+ ISNULL(RL.LevelName,'')  +'",
"superior":"'+ CAST( UTR.Superior As varchar(1)) +'","start_date":"'+ UTR.StartDate  +'",
"manager_nationalcode":"'+ ISNULL(Manager.NationalCode,'')  +'","manager_fullname":"'+ ISNULL(Manager.FirstName + ' ' + Manager.LastName, '')  +'",
}' ChangeTeamRoleJSON From UserTeamRole UTR
Inner Join Role R
On UTR.RoleId = R.RoleId
Inner Join Team T
On UTR.TeamCode = T.TeamCode
LEFT Join RoleLevel RL
On UTR.LevelId_id = RL.id
Inner Join Users Manager
On UTR.ManagerNationalCode = Manager.NationalCode
Where UTR.NationalCode = '1280419180'
