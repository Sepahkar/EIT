CREATE View [dbo].[HR_RoleManager] As
With CTE_RoleTeam As 
(Select * From Role R, Team T)
,CTE_RoleManager As
(Select RoleId,RoleName, HasLevel, RoleTypeCode, TeamCode, TeamName,
SupportManager_id ManagerId, SupportManagerNationalCode ManagerNationalCode
From CTE_RoleTeam
Where RoleTypeCode = 'S' 
UNION
Select RoleId,RoleName, HasLevel, RoleTypeCode, TeamCode, TeamName, 
TestManager_id ManagerId, TestManagerNationalCode ManagerNationalCode
From CTE_RoleTeam
Where RoleTypeCode = 'T' 
UNION
Select RoleId,RoleName, HasLevel, RoleTypeCode, TeamCode, TeamName, 
GeneralManager_id ManagerId, GeneralManagerNationalCode ManagerNationalCode
From CTE_RoleTeam
Where RoleTypeCode Not In ('T','S','M')
UNION
Select RT.RoleId,RT.RoleName, RT.HasLevel, RT.RoleTypeCode, RT.TeamCode, RT.TeamName, 
UTR.ManagerUserName_id ManagerId, UTR.ManagerNationalCode ManagerNationalCode
From CTE_RoleTeam RT
Inner Join UserTeamRole UTR
On UTR.TeamCode = RT.TeamCode And UTR.RoleId = RT.RoleId
Where RoleTypeCode = 'M' )
Select ROW_NUMBER() Over (Order By RoleId, TeamCode) Id ,* From CTE_RoleManager




