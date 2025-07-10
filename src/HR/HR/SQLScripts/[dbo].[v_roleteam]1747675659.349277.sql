CREATE View [dbo].[V_RoleTeam] As 
With CTE_User As (
Select Distinct RoleId_id RoleId,TeamCode_id TeamCode,OC.ManagerUserName_id ManagerUserName, OC.ManagerNationalCode ManagerNationalCode
From  HR_organizationchartrole o
Inner Join HR_organizationchartteamrole OC
On oC.OrganizationChartRole_id=O.id
union
Select Distinct RoleId,TeamCode,ManagerUserName_id, ManagerNationalCode From UserTeamRole WHERE ManagerNationalCode IS NULL)
Select * 
,ROW_NUMBER() Over(order By teamCode) Id
From CTE_User
