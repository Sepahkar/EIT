CREATE FUNCTION [dbo].[HR_Name_GetTeamManager]
(
	@RoleId int,
	@TeamCode Char(3)
	,@ReturnType Char(1)
	---U UserNme
	---N Name
)
RETURNS Varchar(150)
AS
BEGIN
	DECLARE @TeamManager varchar(150)
	--If @Type = 'U'
	--	Begin
	--		;With CTE_TeamManager As (
	--		Select  HM.UserName UserName
	--		From HR_organizationchartteamrole TR
	--		Inner JOIN HR_OrganizationChartRole R
	--		On R.Id=TR.OrganizationChartRole_id
	--		Inner JOin Role Ro
	--		On Ro.RoleId=R.RoleId_id
	--		Inner Join UserTeamRole HM
	--		On TR.ManagerUserName_id=HM.UserName
	--		Inner JOin Users U
	--		On HM.UserName=U.UserName
	--		INner JOIn Team T
	--		On T.TeamCode=TR.TeamCode_id
	--		Where R.RoleId_id=@RoleId
	--		And (TR.TeamCode_id=@TeamCode)
	--		Union 
	--		Select  HM.UserName UserName
	--		From UserTeamRole H
	--		INner JOIn Team T
	--		On T.TeamCode=H.TeamCode
	--		Inner Join UserTeamRole HM
	--		On H.ManagerUserName_id=HM.UserName
	--		Inner JOin Users U
	--		On HM.UserName=U.UserName
	--		Where H.RoleId=@RoleId
	--		And (H.TeamCode=@TeamCode )
	--		)
	--		Select @TeamManager= UserName From CTE_TeamManager
	--	End
	--	If @Type= 'N'
	--		Begin
	--			;With CTE_TeamManager As (
	--			Select  U.FirstName +' ' + U.LastName FullName
	--			From HR_organizationchartteamrole TR
	--			Inner JOIN HR_OrganizationChartRole R
	--			On R.Id=TR.OrganizationChartRole_id
	--			Inner JOin Role Ro
	--			On Ro.RoleId=R.RoleId_id
	--			Inner Join UserTeamRole HM
	--			On TR.ManagerUserName_id=HM.UserName
	--			Inner JOin Users U
	--			On HM.UserName=U.UserName
	--			INner JOIn Team T
	--			On T.TeamCode=TR.TeamCode_id
	--			Where R.RoleId_id=@RoleId
	--			And (TR.TeamCode_id=@TeamCode)
	--			Union 
	--			Select U.FirstName +' ' + U.LastName FullName
	--			From UserTeamRole H
	--			INner JOIn Team T
	--			On T.TeamCode=H.TeamCode
	--			Inner Join UserTeamRole HM
	--			On H.ManagerUserName_id=HM.UserName
	--			Inner JOin Users U
	--			On HM.UserName=U.UserName
	--			Where H.RoleId=@RoleId
	--			And (H.TeamCode=@TeamCode )
	--			)
	--			Select @TeamManager= FullName From CTE_TeamManager
	--	End

	If @ReturnType = 'U'
	Begin
		Select TOP(1) @TeamManager = ManagerUserName_id From UserTeamRole
		Where RoleId = @RoleId And TeamCode = @TeamCode

		--اگر سمت مورد نظر در تیم وجود نداشته باشد، مدیر تیم را بازگشت می دهد
		If @TeamManager Is null
			Select TOP(1) @TeamManager = GeneralManager_id From Team
			Where  TeamCode = @TeamCode
	End
	Else
	Begin
		Select TOP(1) @TeamManager = FirstName + ' ' + LastName
		From UserTeamRole UTR
		Inner Join Users U
		On ManagerUserName_id = U.UserName
		Where RoleId = @RoleId And TeamCode = @TeamCode		

		--اگر سمت مورد نظر در تیم وجود نداشته باشد، مدیر تیم را بازگشت می دهد
		If @TeamManager Is null
			Select TOP(1) @TeamManager = FirstName + ' ' + LastName From Team
			Inner Join Users U
			On GeneralManager_id = U.UserName
			Where  TeamCode = @TeamCode

	End

		RETURN @TeamManager
END
