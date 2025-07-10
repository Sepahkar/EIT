CREATE FUNCTION [dbo].[Date_WorkHistory]
(
 @StartDate varchar(10),
 @EndDate varchar(10)
)
RETURNS nvarchar(100)
AS
BEGIN
	Declare @MonthCount int, @YearCount int
	Declare @ReturnString nvarchar(100) = ''
	Set @MonthCount = DATEDIFF(MONTH,dbo.Date_ShamsiToMiladi(@StartDate), 
	ISNULL(dbo.Date_ShamsiToMiladi(@EndDate),GETDATE()))

	if @MonthCount = 0 
		Set @ReturnString = N'کمتر از یک ماه'
	else
	begin
		Set @YearCount = @MonthCount / 12
		Set @MonthCount = @MonthCount % 12
		if @YearCount > 0
			Set @ReturnString = CAST(@YearCount As varchar(2)) + N' سال '
	
		if @MonthCount > 0 and @YearCount > 0
			Set @ReturnString = @ReturnString + N' و '

		if @MonthCount > 0 
			Set @ReturnString = @ReturnString + CAST(@MonthCount As varchar(2)) + N' ماه'
	end

	return @ReturnString

END
