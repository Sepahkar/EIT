CREATE PROCEDURE [dbo].[HR_ImportData] 
	@YearNumber int = 0
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	Declare @CurrentDate varchar(10)
	--اگر شماره سال ارسال نشده باشد، سال جاری را به دست می آوریم
	if @YearNumber = 0
	Begin
		Set @CurrentDate = dbo.Date_MiladiToShamsi(GETDATE())
		--اکنون شماره سال را به دست می آوریم
		if LEN(@CurrentDate) = 10
			Set @YearNumber = CAST(LEFT(@CurrentDate, 4)  as int)
	End



	Declare @WorkTime Table ([PersonnelCode] [varchar](10) NOT NULL,
	[YearNo] [smallint] NOT NULL,
	[MonthNo] [tinyint] NOT NULL,
	[WorkHours] [varchar](10) NULL,
	[RemoteHours] [varchar](10) NULL,
	[RemoteDays] [tinyint] NULL,
	[OverTime] [varchar](10) NULL,
	[DeductionTime] [varchar](10) NULL,
	[OffTimeHourly] [varchar](10) NULL,
	[OffTimeDaily] [int] NULL,
	[UserName] [varchar](100) NULL)

	Insert into @WorkTime
	([PersonnelCode],[YearNo],[MonthNo],[WorkHours]
	,[RemoteHours],[RemoteDays],[OverTime]
	,[DeductionTime],[OffTimeHourly],[OffTimeDaily])
	SELECT [PersonnelCode]
		,[YearNo]
		,[MonthNo]
		,[WorkHours]
		,[RemoteHours]
		,[RemoteDays]
		,[OverTime]
		,[DeductionTime]
		,[OffTimeHourly]
		,[OffTimeDaily]
	FROM [Evaluation].[dbo].[EVA_WorkTime] 
	Where [YearNo] = @YearNumber

	Update @WorkTime
	Set username = U.Username2
	From @WorkTime W
	Inner Join Users U
	On NationalCode = W.PersonnelCode
	
	--اکنون داده های مربوط به آن سال را پاک می کنیم
	Delete WorkTime
	Where YearNo = @YearNumber
	
	Insert into WorkTime ([PersonnelCode],[YearNo],[MonthNo],[WorkHours]
	,[RemoteHours],[RemoteDays],[OverTime]
	,[DeductionTime],[OffTimeHourly],[OffTimeDaily],UserName)
	Select [PersonnelCode],[YearNo],[MonthNo],[WorkHours]
	,[RemoteHours],[RemoteDays],[OverTime]
	,[DeductionTime],[OffTimeHourly],[OffTimeDaily],UserName
	From @WorkTime



END
