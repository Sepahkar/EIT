CREATE View [dbo].[UserTeamRoleJSON] As
Select U.NationalCode, U.FirstName, U.LastName, U.Username2 Username, U.Gender,U.IsActive,'C' As Current_Previous, '{"team_code":"'+ UTR.TeamCode  +'", "team_name":"'+ T.TeamName  +'",
"role_id":"'+ CAST(UTR.RoleId as varchar(5))  +'","role_name":"'+ R.RoleName  +'",
"level_id":"'+ CAST(ISNULL(UTR.LevelId_id,'') As varchar(1))  +'","level_name":"'+ 
ISNULL(RL.LevelName,'')  +'",
"superior":"'+ CAST( UTR.Superior As varchar(1)) 
+'","start_date":"'+ UTR.StartDate  +'", 
"active_in_evaluation":'+ 
CASE T.ActiveInEvaluation  WHEN 1 THEN 'true' ELSE 'false' END +',
"active_in_service":'+ 
CASE T.ActiveInService  WHEN 1 THEN 'true' ELSE 'false' END+',
"manager_nationalcode":"'+ ISNULL(Manager.NationalCode,'')  +'",
"manager_username":"'+ ISNULL(Manager.Username2,'')  +'",
"manager_fullname":"'+ ISNULL(Manager.FirstName + ' ' + Manager.LastName, '')  +'"}' 
UserTeamRole 
From Users U Inner Join
UserTeamRole UTR
On U.NationalCode = UTR.NationalCode
Inner Join Role R
On UTR.RoleId = R.RoleId
Inner Join Team T
On UTR.TeamCode = T.TeamCode
LEFT Join RoleLevel RL
On UTR.LevelId_id = RL.id
Inner Join Users Manager
On UTR.ManagerNationalCode = Manager.NationalCode
UNION
Select U.NationalCode, U.FirstName, U.LastName, U.Username2 Username, U.Gender,U.IsActive,'P' As Current_Previous, '{"team_code":"'+ UTR.TeamCode  +'", "team_name":"'+ T.TeamName  +'",
"role_id":"'+ CAST(UTR.RoleId as varchar(5))  +'","role_name":"'+ R.RoleName  +'",
"level_id":"'+ CAST(ISNULL(UTR.LevelId_id,'') As varchar(1))  +'","team_code":"'+ ISNULL(RL.LevelName,'')  +'",
"superior":"'+ CAST( UTR.Superior As varchar(1)) +'",
"start_date":"'+ UTR.StartDate  +'","end_date":"'+ UTR.EndDate  +'",
"active_in_evaluation":'+ 
CASE T.ActiveInEvaluation  WHEN 1 THEN 'true' ELSE 'false' END +',
"active_in_service":'+ 
CASE T.ActiveInService  WHEN 1 THEN 'true' ELSE 'false' END +',
"manager_nationalcode":"'+ ISNULL(Manager.NationalCode,'')  +'","manager_fullname":"'+ ISNULL(Manager.FirstName + ' ' + Manager.LastName, '')  +'"}' 
UserTeamRole 
From Users U Inner Join
PreviousUserTeamRole UTR
On U.NationalCode = UTR.NationalCode
Inner Join Role R
On UTR.RoleId = R.RoleId
Inner Join Team T
On UTR.TeamCode = T.TeamCode
LEFT Join RoleLevel RL
On UTR.LevelId_id = RL.id
Inner Join Users Manager
On UTR.ManagerNationalCode = Manager.NationalCode

