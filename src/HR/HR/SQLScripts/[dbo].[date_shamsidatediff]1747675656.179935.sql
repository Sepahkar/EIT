CREATE FUNCTION [dbo].[Date_ShamsiDateDiff] 
(
	-- Add the parameters for the function here
	@StartDate varchar(10),
	@EndDate varchar(10)
)
RETURNS int
AS
BEGIN
	-- Declare the return variable here
	DECLARE @DiffDays int

	
	--در صورت وقوع هر یک از شرایط زیر مقدار صفر بازگشت داده می شود
	If ISNULL(@StartDate,'') = '' Or ISNULL(@EndDate,'') = '' --اگر پارامترهای ورودی خالی باشند
	Or LEN(@StartDate) < 10  Or LEN(@EndDate) < 10
	--Or LEFT(@StartDate,2) <> '13' 
	Or ISNUMERIC(LEFT(@StartDate,4)) = 0 -- در صورتی که شماره سال در تاریخ شروع نامعتبر باشد
	--Or LEFT(@EndDate,2) <> '13' 
	Or ISNUMERIC(LEFT(@EndDate,4)) = 0 -- در صورتی که شماره سال در تاریخ پایان نامعتبر باشد
	Or ISNUMERIC(SUBSTRING(@StartDate,6,2)) = 0 Or SUBSTRING(@StartDate,6,2) > '12'--در صورتی که شماره ماه در تاریخ نامعتبر باشد
	Or ISNUMERIC(SUBSTRING(@EndDate,6,2)) = 0 Or SUBSTRING(@EndDate,6,2) > '12'--در صورتی که شماره ماه در تاریخ نامعتبر باشد
	Or ISNUMERIC(RIGHT(@StartDate,2)) = 0 Or RIGHT(@StartDate,2) > '31' --در صورتی که شماره ی روز در تاریخ نامعتبر باشد
	Or ISNUMERIC(RIGHT(@EndDate,2)) = 0 Or RIGHT(@EndDate,2) > '31' --در صورتی که شماره ی روز در تاریخ نامعتبر باشد
		Return 0

	--Declare @StartDay int, @StartMonth int, @StartYear int
	--Declare @EndDay int, @EndMonth int, @EndYear int

	----فیلدهای روز و ماه و سال را به ازای هر تاریخ به دست می آوریم
	--Select @StartDay = RIGHT(@StartDate,2),@StartMonth=SUBSTRING(@StartDate,6,2), @StartYear = LEFT(@StartDate,4),	
	--@EndDay = RIGHT(@EndDate,2),@EndMonth=SUBSTRING(@EndDate,6,2), @EndYear = LEFT(@EndDate,4)


	--Set @DiffDays = (@EndYear - @StartYear) * 365 + (@EndMonth - @StartMonth) * 30 + (@EndDay - @StartDay)
	
	Set @DiffDays =  DATEDIFF(Day, dbo.EVA_Date_ShamsiToMiladi(@StartDate), dbo.EVA_Date_ShamsiToMiladi(@EndDate))
	
	-- Return the result of the function
	RETURN @DiffDays

END
