CREATE PROCEDURE [dbo].[HR_ExportData] 

AS
BEGIN

	-----------------------Cost Price Start------------------------
	----اگر مواردی داریم که کد ملی یکسان است ولی نام کاربری تغییر کرده است باید اصلاح شود
	--اگر مواردی داریم که کد ملی یکسان است ولی نام کاربری تغییر کرده است باید اصلاح شود
	--چون نام کاربری در بسیاری از جداول ذخیره شده است باید در تمامی آنها به روزرسانی انجام شود
	Declare @ChangeUserName Table(OldUsername varchar(50), NewUsername varchar(50))
	insert into @ChangeUserName (NewUsername,OldUsername)
	select U.Username, CU.Username from Users U
	Inner Join CostPrice.dbo.CostPrice_users CU
	on U.NationalCode = CU.PersonnelCode And U.UserName <> CU.Username
	--این خیلی کار خفنیه!
	--نمی توانیم به روزرسانی را انجام دهیم چون یک عالمه کلید خارجی دارد
	--از طرف دیگه نمی توانیم اول کلید خارجی ها را به روزرسانی کنیم، چون نام کاربری جدید وجود ندارد
	--بنابراین اول یک رکورد با نام کاربری جدید درج می کنیم
	--ولی چون کد ملی باید منحصر به فرد باشد، این درج را با کد ملی تغییر یافته انجام می دهیم
	--برای این کار به آخر کدملی *** اضافه می کنیم
	insert into CostPrice.dbo.CostPrice_users(Username, FirstName, LastName, PersonnelCode, ContractDate)
	select NewUser.NewUsername, FirstName, LastName, PersonnelCode+'***', ContractDate 
	from CostPrice.dbo.CostPrice_users U
	Inner Join @ChangeUserName NewUser
	On U.Username = OldUsername
	Where NewUsername Not In
	(Select Username From CostPrice.dbo.CostPrice_users)

	--حالا نام کاربری جدید را داریم، می توانیم کلیدهای خارجی را به روزرسانی کنیم
	--ابتدا در هر یک از جدولهایی که  نام کاربری کلید خارجی است باید به روزرسانی انجام شود
	--CostPrice_importdata_tasklist
	Update TL 
	Set FromUsername = NewUsername
	From CostPrice.dbo.CostPrice_importdata_tasklist TL
	inner join @ChangeUserName U
	On TL.FromUsername = U.OldUsername

	Update TL 
	Set ToUsername = NewUsername
	From CostPrice.dbo.CostPrice_importdata_tasklist TL
	inner join @ChangeUserName U
	On TL.ToUsername = U.OldUsername

	--CostPrice_importdata_taskworktime
	Update TW 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_importdata_taskworktime TW
	inner join @ChangeUserName U
	On TW.Username = U.OldUsername

	--CostPrice_payment
	Update Pay 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_payment Pay
	inner join @ChangeUserName U
	On Pay.Username = U.OldUsername

	--CostPrice_productservicecostdetail
	Update PSCD 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_productservicecostdetail PSCD
	inner join @ChangeUserName U
	On PSCD.Username = U.OldUsername

	--CostPrice_productservicetaskdeletelog
	Update PSTD 
	Set CreatorUser_id = NewUsername
	From CostPrice.dbo.CostPrice_productservicetaskdeletelog PSTD
	inner join @ChangeUserName U
	On PSTD.CreatorUser_id = U.OldUsername

	--CostPrice_producttask
	Update PT 
	Set CreatorUser_id = NewUsername
	From CostPrice.dbo.CostPrice_producttask PT
	inner join @ChangeUserName U
	On PT.CreatorUser_id = U.OldUsername

	--CostPrice_servicetask
	Update ST 
	Set CreatorUser_id = NewUsername
	From CostPrice.dbo.CostPrice_servicetask ST
	inner join @ChangeUserName U
	On ST.CreatorUser_id = U.OldUsername

	--CostPrice_userteamrole
	Update UTR 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_userteamrole UTR
	inner join @ChangeUserName U
	On UTR.Username = U.OldUsername

	--CostPrice_userteamrolecount_
	Update UTRC 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_userteamrolecount_ UTRC
	inner join @ChangeUserName U
	On UTRC.Username = U.OldUsername

	--CostPrice_userteamrolepermonth
	Update UTRM 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_userteamrolepermonth UTRM
	inner join @ChangeUserName U
	On UTRM.Username = U.OldUsername

	--CostPrice_userwithoutteam
	Update UWT 
	Set Username = NewUsername
	From CostPrice.dbo.CostPrice_userwithoutteam UWT
	inner join @ChangeUserName U
	On UWT.Username = U.OldUsername

	--به روزرسانی کلیدهای خارجی تمام شد
	--حالا رکوردهای قدیمی را حذف می کنیم
	Delete CostPrice.dbo.CostPrice_users
	Where Username In (Select OldUsername From @ChangeUserName)

	--حالا کد ملی را به روز می کنیم
	Update CostPrice.dbo.CostPrice_users
	Set PersonnelCode = REPLACE(PersonnelCode,'***','')
	Where Username In (Select NewUsername From @ChangeUserName)



	--user table
	Insert into CostPrice.dbo.CostPrice_users ( Username, FirstName, LastName,PersonnelCode )
	Select Username, FirstName, LastName,NationalCode From Users
	Where NationalCode Is not null and UserName not In (Select Username From CostPrice.dbo.CostPrice_users)

	Select CAST(@@ROWCOUNT As varchar(10)) + ' new users added'

	--ممکن است فیلدهای موجود نام، نام خانوادگی، کد ملی و ... تغییر کرده باشند
	Update CostPrice.dbo.CostPrice_users
	Set FirstName = U.FirstName, LastName = U.LastName
	From CostPrice.dbo.CostPrice_users CU
	Inner Join Users U
	On CU.Username = U.UserName

	--برای کد ملی دو موضوع وجود دارد که قبل از به روزرسانی باید کنترل شود
	--کد ملی تکراری نباشد
	--کد ملی نال نباشد
	Update CostPrice.dbo.CostPrice_users
	Set FirstName = U.FirstName, LastName = U.LastName, 
	ContractDate = U.ContractDate
	From CostPrice.dbo.CostPrice_users CU
	Inner Join Users U
	On CU.Username = U.UserName
	Where NationalCode is not null and NationalCode not in
	(Select PersonnelCode From CostPrice.dbo.CostPrice_users)

	--role table
	--add new role as 'other' group
	Insert into CostPrice.dbo.CostPrice_roles (RoleId, RoleName, RoleGroupCode)
	Select RoleId, RoleName,'O' From Role
	Where RoleId not In (Select RoleId From CostPrice.dbo.CostPrice_roles)

	Select CAST(@@ROWCOUNT As varchar(10)) + ' new role added'

	--role level table
	Insert into CostPrice.dbo.CostPrice_rolelevel (LevelName)
	Select LevelName From RoleLevel
	Where LevelName not In (Select LevelName From CostPrice.dbo.CostPrice_rolelevel)

	Select CAST(@@ROWCOUNT As varchar(10)) + ' new role level added'


	--team table
	--add new team with operation 0 (means not operational team)
	Insert into CostPrice.dbo.CostPrice_team(TeamCode,TeamName, OperationType)
	Select TeamCode, TeamName,0 From Team
	Where TeamCode not In (Select TeamCode From CostPrice.dbo.CostPrice_team)

	Select CAST(@@ROWCOUNT As varchar(10)) + ' new team added'



	--user team role table

	--ابتدا رکوردهای قبلی را پاک می کنیم
	Delete CostPrice.dbo.CostPrice_UserTeamRole

	;With CTE_UserTeamRole As
	(SELECT StartDate, EndDate, ManagerUserName_id
	,[RoleId],[TeamCode],[UserName]
	FROM [HR].[dbo].[PreviousUserTeamRole]
	Union 
	SELECT [StartDate],[EndDate], ManagerUserName_id
	,[RoleId],[TeamCode],[UserName]
	FROM [HR].[dbo].[UserTeamRole])


	Insert into CostPrice.dbo.CostPrice_UserTeamRole
	(StartDateJalali, EndDateJalali, RoleId, TeamCode, Username, ManagerUsername)
	--برای کسانی که در همان سمت و تیم تغییر سطح داشته اند
	--نیازی نیست دو رکورد منتقل شود
	--تاریخ شروع را به عنوان زودترین تاریخ شروع می گیریم
	--تاریخ خاتمه را یک تاریخ بزرگ می گیریم، بعدا نال می کنیم
	Select MIN([StartDate]) StartDate,MAX(ISNULL([EndDate],'1440/01/01' )) EndDate, 
	[RoleId],[TeamCode],UTR.[UserName], ManagerUserName_id
	From CTE_UserTeamRole UTR
	Inner Join Users U
	On UTR.UserName = U.UserName
	Where U.NationalCode Is Not Null
	Group By [RoleId],[TeamCode],UTR.[UserName], ManagerUserName_id

	Select CAST(@@ROWCOUNT As varchar(10)) + ' user team role added'

	--اکنون تاریخی که به عنوان تاریخ بزرگ آینده گرفته بودیم را نال می کنیم
	Update CostPrice.dbo.CostPrice_UserTeamRole
	Set EndDateJalali = null
	Where EndDateJalali = '1440/01/01'

	--حالا تاریخ میلادی را به روزرسانی می کنیم
	Update CostPrice.dbo.CostPrice_UserTeamRole
	Set StartDate = CostPrice.dbo.CostPrice_Date_ShamsiToMiladi(StartDateJalali),
	EndDate = CostPrice.dbo.CostPrice_Date_ShamsiToMiladi(EndDateJalali)

	--در سیستم بهای تمام شده آخرین وضعیت ارشد بودن و آخرین سطح مهم است
	--بنابراین باید آخرین رکورد معادل هر کاربر را به دست بیاوریم
	;with CTE_LastUserTeamRole As
	(Select UserName,TeamCode,RoleId, LevelId_id, Superior,
	ROW_NUMBER() Over(Partition By Username, TeamCode, RoleId Order By StartDate DESC) RecordNumber 
	From UserTeamRoleAll)

	Update CostPrice.dbo.CostPrice_UserTeamRole
	Set LastLevel_id= LUTR.LevelId_id, IsSuperior=LUTR.Superior
	From CostPrice.dbo.CostPrice_UserTeamRole UTR
	Inner Join CTE_LastUserTeamRole LUTR
	on LUTR.Username = UTR.Username and LUTR.TeamCode = UTR.TeamCode And LUTR.RoleId = UTR.RoleId
	Where RecordNumber = 1

	-----------------------Cost Price End------------------------

	-------------------------Service Book Start--------------------

	--کاربرانی که وجود ندارند را اضافه می کنیم
	Insert into ServiceBook.dbo.Users (UserName, FirstName,LastName)
	Select Username, FirstName, LastName From Users Where UserName Not In
	(Select UserName From ServiceBook.dbo.Users)

	--با توجه به کارهای خارق العاده ای که واحد فناوری اطلاعات انجام می دهد، ممکن است نام کاربری یک نفر 
	--را به یک نفر دیگر داده باشد، بنابراین باید نام و نام خانوادگی ها را هم به روز کنیم
	--هر چند اینطوری کل داده ها به هم می ریزد
	Update ServiceBook.dbo.Users
	Set FirstName = HU.FirstName, LastName = HU.LastName
	From ServiceBook.dbo.Users SU
	Inner Join Users HU
	On SU.UserName = HU.UserName

	--حالا لیست سمت ها را به روز می کنیم
	Insert into ServiceBook.dbo.Role(RoleId, RoleName)
	Select RoleId,RoleName From Role
	Where RoleId Not In
	(Select RoleId From ServiceBook.dbo.Role)

	--جهت اطمینان بیشتر همان عملیات به روزرسانی را اینجا هم انجام می دهیم
	--این ربطی به شیرین کاری های فناوری اطلاعات ندارد. 
	--ربط به تجربه من داره که اینجا چیزهای خیلی غیرمنتظره دیده ام
	Update ServiceBook.dbo.Role
	Set RoleName = HR.RoleName
	From ServiceBook.dbo.Role SR
	Inner Join Role HR
	On SR.RoleId = HR.RoleId

	--حالا برویم سراغ تیم ها
	insert into ServiceBook.dbo.Team(TeamCode, TeamName, ActiveInService, ActiveInEvaluation)
	Select TeamCode, TeamName, ActiveInService, ActiveInEvaluation From Team
	Where TeamCode Not In
	(Select TeamCode From ServiceBook.dbo.Team)

	--باز هم به روزرسانی اطلاعات
	--کار از محکم کاری عیب نمی کنه!
	Update ServiceBook.dbo.Team
	Set TeamName = HT.TeamName, ActiveInService = HT.ActiveInService, ActiveInEvaluation = HT.ActiveInEvaluation
	From ServiceBook.dbo.Team ST
	Inner Join Team HT
	On ST.TeamCode = HT.TeamCode

	--یک نکته جالب داشتم فکر می کردم، اگه یک کاربر یا یک تیم یا یک سمت حذف بشود چی؟
	--راجع به کاربر و سمت کاری نمی توانیم بکنیم
	--نمی توانیم حذف کنیم چون ممکن است در جدول مقصد کلید خارجی باشند و همه چیز منفجر می شود
	--اما راجع به تیم می توانیم یک حرکتی بزنیم
	--یعنی می توانیم در این دیتابیس فعال بودن آن در سرویس را غیرفعال کنیم
	Update ServiceBook.dbo.Team
	Set  ActiveInService = 0
	Where TeamCode Not In
	(Select TeamCode From Team)

	--حالا به سراغ جدول سمت و تیم کاربران می رویم
	--با تشکر از خودم، این جدول کلید خارجی ندارد و راحت می توانیم رکوردها را پاک کنیم
	--فقط یک سئوال مهم مطرح می شود
	--آیا اینجا فقط سمت های فعال باید آورده شود یا همه سمت ها؟
	--الان یادم نیست که منطق برنامه چیه، باید چک کنیم و در صورت لزوم اصلاح نماییم
	Delete ServiceBook.dbo.UserTeamRole

	Insert into ServiceBook.dbo.UserTeamRole
	Select StartDate,EndDate,RoleId,TeamCode,UserName From UserTeamRole

	-----------------------Service Book End----------------------

	-----------------------PersonnelService Start--------------------
	-- In personnel service (pors app) we are using the PersonnelService.dbo.Users for 
	-- generating reports. so as we need to the Personnel NationalCode in reports we have to 
	-- keep update the PersonnelService.dbo.Users as well.
	-- we do not have Role, Team and UserTeamRole tables by this time. so we skip updating them
	--(windowsam taze avaz shode va hal nadashtam ke keyboard ro farsi konam)

	--کاربرانی که وجود ندارند را اضافه می کنیم
	Insert into PersonnelService.dbo.Users (UserName, FirstName,LastName, NationalCode)
	Select Username, FirstName, LastName, NationalCode From Users Where UserName Not In
	(Select UserName From PersonnelService.dbo.Users)

	--با توجه به کارهای خارق العاده ای که واحد فناوری اطلاعات انجام می دهد، ممکن است نام کاربری یک نفر 
	--را به یک نفر دیگر داده باشد، بنابراین باید نام و نام خانوادگی ها را هم به روز کنیم
	--هر چند اینطوری کل داده ها به هم می ریزد
	Update PersonnelService.dbo.Users
	Set FirstName = HU.FirstName, LastName = HU.LastName
	From PersonnelService.dbo.Users SU
	Inner Join Users HU
	On SU.UserName = HU.UserName
	-----------------------PersonnelService End----------------------


	-----------------------CorpIssue Start----------------------
	--ابتدا تیم های جدید را درج می کنیم
	insert into SalesManagement.dbo.CorpIssue_team (team_code,team_name, manager)
	Select TeamCode,TeamName,U.NationalCode From HR.dbo.Team T
	Inner Join Users U
	On T.GeneralManager_id = U.Username
	Where T.IsActive = 1 And
	TeamCode not in 
	(Select team_code From SalesManagement.dbo.CorpIssue_team)

	--حالا اگر مدیر تیم عوض شده باشد آن را اصلاح می کنیم
	update c
	set manager = NationalCode
	From HR.dbo.Team T
	Inner Join Users U
	On T.GeneralManager_id = U.Username
	inner join SalesManagement.dbo.CorpIssue_team c
	on t.TeamCode = c.team_code
	Where NationalCode <> manager
	-----------------------CorpIssue End----------------------


END


