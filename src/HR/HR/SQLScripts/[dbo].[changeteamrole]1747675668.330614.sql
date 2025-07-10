CREATE PROCEDURE [dbo].[ChangeTeamRole] 
	-- Add the parameters for the stored procedure here
	@RequestId int = 61689
AS
BEGIN


	Declare @RequestType tinyint
	Declare @RequestTypeTitle nvarchar(30)
	Declare @Username varchar(50) 
	Declare @EffectiveDate varchar(10)
	Declare @EffectiveDay tinyint--روز تاریخ موثر
	Declare @EffectiveMonth tinyint--ماه تاریخ موثر
	Declare @DayDiff smallint = 0--اختلاف تاریخ موثر با ابتدای ماه
	Declare @EffectiveDate1 varchar(10)--تاریخ خاتمه سمت قبلی
	Declare @ManagerEffectiveDate varchar(10)
	Declare @SourceRoleId int
	Declare @SourceTeamCode char(3)
	Declare @SourceLevelId tinyint
	Declare @SourceSuperior bit
	Declare @TargetRoleId int
	Declare @TargetTeamCode char(3)
	Declare @TargetLevelId tinyint
	Declare @TargetSuperior bit

	Declare @UserTeamRoleId int
	Declare @ManagerUserName varchar(200)
	Declare @ManagerNationalCode varchar(10)
	Declare @UserNationalCode varchar(10)
	Declare @ContractEndDate Date
	--ابتدا اطلاعات درخواست را دریافت می کنیم
	select @RequestTypeTitle=RequestTypeTitle,
	@Username= UserName,@EffectiveDate=FormEffectiveDate, @ManagerEffectiveDate=ManagerEffectiveDate,@RequestType=RequestTypeId,
	@SourceTeamCode=SourceTeamCode, @SourceRoleId=SourceRoleId, @SourceLevelId=SourceLevelId, @SourceSuperior=SourceSuperior,
	@TargetTeamCode=TargetTeamCode, @TargetRoleId=TargetRoleId, @TargetLevelId=TargetLevelId, @TargetSuperior=TargetSuperior
	from ProcessManagement.dbo.ChangeTeamRole_History
	Where Id = @RequestId

	-- کد ملی کاربر را به دست می آوریم
	Select @UserNationalCode = NationalCode From Users
	Where Username = @Username

	--اگر درخواست غیرفعال سازی باشد، تاریخ موثر همان تاریخ تعیین شده توسط مدیریت است
	If @RequestType = 7
		Set @EffectiveDate = @ManagerEffectiveDate


	--اگر درخواست مربوط به روزهای پایانی ماه باشد، آن را برابر با ابتدا ماه جدید قرار می دهیم
	--مثلا اگر 29 ماه باشد، فرض می کنیم سمت جدید از 1 ماه بعد شروع شده است
	-- البته این موضوع برای غیرفعال سازی که سمت جدیدی وجود ندارد، معنی نخواهد داشت
	If @RequestType <> 7
	Begin
		Set @EffectiveDay = CAST( RIGHT(@EffectiveDate, 2) As tinyint)
		Set @EffectiveMonth = CAST(LEFT(RIGHT(@EffectiveDate, 5),2) As tinyint)
		If @EffectiveDay >= 27 
		Begin
			--در این حالت تاریخ شروع می شود تاریخ روز نخست ماه بعد
			Set @DayDiff = 30 - @EffectiveDay + 1
			--اگر ماه 31 روزه باشد اختلاف یک روز بیشتر است
			If @EffectiveMonth Between 1 And 6
				Set @DayDiff = @DayDiff + 1
		End
		--اگر تاریخ شروع هم سه روز اول ماه باشد، همان روز اول ماه در نظر می گیریم
		If @EffectiveDay <= 3
		Begin
			--در این حالت تاریخ شروع می شود تاریخ روز نخست ماه بعد
			Set @DayDiff = 1 - @EffectiveDay 
		End

		--تاریخ موثر را به روز می کنیم
		Set @EffectiveDate = dbo.Date_ShamsiDateAdd(@EffectiveDate, @DayDiff)
	End

	--تاریخ خاتمه سمت قبلی یک روز قبل از تاریخ شروع این سمت است
	Set @EffectiveDate1 = dbo.Date_ShamsiDateAdd(@EffectiveDate, -1)

	--مدیر تیم مقصد را به دست می آوریم
	--اگر پشتیبان باشد
	If @TargetRoleId = 69
		Select @ManagerUserName = SupportManager_id, 
		@ManagerNationalCode = SupportManagerNationalCode From Team
		Where TeamCode = @TargetTeamCode
	--اگر تستر باشد
	Else If @TargetRoleId in( 72,55 )
		Select @ManagerUserName = TestManager_id, 
		@ManagerNationalCode=TestManagerNationalCode From Team
		Where TeamCode = @TargetTeamCode
	--در غیر این صورت یعنی برنامه نویس یا سمت های دیگر است
	Else
		Select @ManagerUserName = GeneralManager_id, 
		@ManagerNationalCode=GeneralManagerNationalCode From Team
		Where TeamCode = @TargetTeamCode

	Select @UserTeamRoleId = Id From UserTeamRole
	Where UserName = @Username And RoleId = @SourceRoleId And TeamCode = @SourceTeamCode 
	And ISNULL(LevelId_id,0) = ISNULL(@SourceLevelId,0) And Superior = @SourceSuperior


	--اگر رکورد سمت قبلی وجود داشته باشد
	--و تغییر تیم و سمت و یا غیر فعال سازی باشد
	If @UserTeamRoleId Is not null And @RequestType In (1,2,3,7,8)
	Begin
		--در صورتی که این سمت قبلا برای این کاربر درج نشده باشد
		If Not Exists (Select 1 From PreviousUserTeamRole 
						Where UserName = @Username And RoleId = @SourceRoleId And TeamCode = @SourceTeamCode 
						And ISNULL(LevelId_id,0) = ISNULL(@SourceLevelId,0) And Superior = @SourceSuperior And EndDate=@EffectiveDate1)

			--سمت قبلی را در جدول سمت های قبلی کاربران درج می کنیم
			Insert into PreviousUserTeamRole (StartDate, EndDate, RoleId, TeamCode, NationalCode, ManagerNationalCode,
											UserName, LevelId_id, Superior, ManagerUserName_id, Comment)
			Select StartDate, @EffectiveDate1, RoleId, TeamCode, NationalCode, ManagerNationalCode,
			UserName, LevelId_id, Superior, ManagerUserName_id ,Comment + ' ' + 
			N'بنا به درخواست ' + @RequestTypeTitle + N' شماره ' + CAST(@RequestId  as varchar(10)) + N' این سمت غیرفعال شد'
			From UserTeamRole
			Where UserName = @Username And RoleId = @SourceRoleId And TeamCode = @SourceTeamCode 
			And ISNULL(LevelId_id,0) = ISNULL(@SourceLevelId,0) And Superior = @SourceSuperior





		--حالا اطلاعات سمت جدید را در سمت قبلی به روز می کنیم
		Update UserTeamRole
		Set RoleId = @TargetRoleId, LevelId_id = @TargetLevelId , TeamCode = @TargetTeamCode, 
		Superior = @TargetSuperior, ManagerUserName_id = @ManagerUserName, StartDate = @EffectiveDate,
		ManagerNationalCode = @ManagerNationalCode,
		Comment = N'بنا به درخواست ' + @RequestTypeTitle + N' شماره ' + CAST(@RequestId  as varchar(10)) + N' به سیستم اضافه شد'
		Where Id = @UserTeamRoleId
	End

	--اگر تعریف تیم یا سمت جدید باشد، بایستی فقط سمت و تیم جدید را اضافه کنیم
	Else If @RequestType In (4,5,6)
	Begin
		--سمت جدید را در جدول سمت های  کاربران درج می کنیم
		If Not Exists (Select 1 From UserTeamRole Where
						UserName = @Username And RoleId = @TargetRoleId And TeamCode = @TargetTeamCode 
						And ISNULL(LevelId_id,0) = ISNULL(@TargetLevelId,0) And Superior = @TargetSuperior)
			Insert into UserTeamRole (StartDate,  RoleId, TeamCode, ManagerNationalCode, NationalCode,
											UserName, LevelId_id, Superior, ManagerUserName_id, Comment)
			Select @EffectiveDate, @TargetRoleId, @TargetTeamCode, @ManagerNationalCode,@UserNationalCode,
			@UserName, @TargetLevelId, @TargetSuperior, @ManagerUserName , 
			N'بنا به درخواست ' + @RequestTypeTitle + N' شماره ' + CAST(@RequestId  as varchar(10)) + N' به سیستم اضافه شد'
	
	End

	--اگر درخواست غیرفعال سازی باشد باید کارهای زیر را انجام دهیم
	If @RequestType = 7
	Begin
		--رکورد سمت فعلی را حذف کنیم
		Delete UserTeamRole Where Id = @UserTeamRoleId

		--اگر این کاربر هیچ سمت فعال دیگری ندارد، باید آن را غیر فعال کنیم
		If Not Exists (Select 1 From UserTeamRole Where UserName = @Username)
		Begin
			--Set @ContractEndDate = @EffectiveDate

			Select @EffectiveDate ContractEndDate
			--کاربر را غیرفعال کرده و تاریخ خاتمه همکاری را بزنیم
			Update Users
			Set IsActive = 0, ContractEndDate = @EffectiveDate
			Where Username = @Username
		End
	End

	Select * From ProcessManagement.dbo.ChangeTeamRole_History
	Where Id = @RequestId

	Select 'CurrentRole->' CurrentRole, FirstName, LastName, UTR.UserName,
	UTR.NationalCode, UTR.ManagerNationalCode ,StartDate, EndDate 
	,UTR.RoleId, RoleName, UTR.TeamCode, TeamName, LevelId_id, LevelName,Superior, UTR.Comment,
	ManagerUserName_id, U.IsActive
	From Users U
	Left Join UserTeamRole UTR
	On UTR.UserName = U.UserName
	Inner Join Role R
	On UTR.RoleId = R.RoleId
	Inner Join Team T
	On UTR.TeamCode = T.TeamCode
	Left Join RoleLevel RL
	On UTR.LevelId_id = RL.id
	Where UTR.Username = @Username


	Select 'PreviousRole->' CurrentRole, FirstName, LastName, UTR.UserName,
	UTR.NationalCode, UTR.ManagerNationalCode , StartDate, EndDate 
	,UTR.RoleId, RoleName, UTR.TeamCode, TeamName, LevelId_id, LevelName,Superior ,UTR.Comment, 
	ManagerUserName_id,  U.IsActive,  ContractEndDate
	From Users U
	Left Join PreviousUserTeamRole UTR
	On UTR.UserName = U.UserName
	Inner Join Role R
	On UTR.RoleId = R.RoleId
	Inner Join Team T
	On UTR.TeamCode = T.TeamCode
	Left Join RoleLevel RL
	On UTR.LevelId_id = RL.id
	Where UTR.Username = @Username

END
