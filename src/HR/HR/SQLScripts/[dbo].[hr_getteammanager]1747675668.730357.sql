CREATE PROCEDURE [dbo].[HR_GetTeamManager] 

	@RoleId int=117,
	@TeamCode Char(3) ='ALL'
	---ALL
	---اگر کلی بخوایم

AS
BEGIN
			--;With CTE_TeamManager As (
			--Select  HM.UserName,U.FirstName,U.LastName,
			--TR.TeamCode_id,T.TeamName
			--From HR_organizationchartteamrole TR
			--Inner JOIN HR_organizationchartrole R
			--On R.Id=TR.OrganizationChartRole_id
			--Inner JOin Role Ro
			--On Ro.RoleId=R.RoleId_id
			--Inner Join UserTeamRole HM
			--On TR.ManagerUserName_id=HM.UserName
			--Inner JOin Users U
			--On HM.UserName=U.UserName
			--INner JOIn Team T
			--On T.TeamCode=TR.TeamCode_id
			--Where R.RoleId_id=@RoleId
			--And (TR.TeamCode_id=@TeamCode Or @TeamCode='ALL')
			--Union 
			--Select  HM.UserName,U.FirstName,U.LastName,
			--H.TeamCode,T.TeamName
			--From UserTeamRole H
			--INner JOIn Team T
			--On T.TeamCode=H.TeamCode
			--Inner Join UserTeamRole HM
			--On H.ManagerUserName_id=HM.UserName
			--Inner JOin Users U
			--On HM.UserName=U.UserName
			--Where H.RoleId=@RoleId
			--And (H.TeamCode=@TeamCode Or @TeamCode='ALL')
			--)
			--Select * From CTE_TeamManager


			
			-- اگر تستر باشد
			IF @RoleId in (72 ,55)
			begin 
				
				select UserName, FirstName, LastName, TeamCode TeamCode_id, TeamName
				from Team T
				inner join Users U on T.TestManager_id = U.UserName
				where (T.TeamCode = @TeamCode Or @TeamCode = 'ALL') And T.IsActive = 1

				
			end
			-- اگر پشتیان باشد

			ELSE IF @RoleId = 69  
			begin 
				select UserName, FirstName, LastName, TeamCode TeamCode_id, TeamName
				from Team T
				inner join Users U on T.SupportManager_id = U.UserName
				where (T.TeamCode = @TeamCode Or @TeamCode = 'ALL') And T.IsActive = 1


				
			end

			-- اگر برنامه نویس یا هر سمت دیگری باشد
			
			ELSE 
			begin 
				select UserName, FirstName, LastName, TeamCode TeamCode_id, TeamName
				from Team T
				inner join Users U on T.GeneralManager_id = U.UserName
				where (T.TeamCode = @TeamCode Or @TeamCode = 'ALL') And T.IsActive = 1


				
			end
		

End

