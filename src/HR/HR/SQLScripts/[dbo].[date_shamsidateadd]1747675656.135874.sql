Create FUNCTION [dbo].[Date_ShamsiDateAdd] 
(
	-- Add the parameters for the function here
	@ShamsiDate varchar(10),
	@DayCount smallint
)
RETURNS varchar(10)
AS
BEGIN
	If ISNULL(@DayCount,0) = 0
		Return @ShamsiDate


	--ابتدا تاریخ معادل میلادی را به دست می آوریم
	Declare @MiladiDate Date 
	Set @MiladiDate = dbo.Date_ShamsiToMiladi(@ShamsiDate)

	--حالا اختلاف روز را حساب می کنیم
	Set @MiladiDate = DATEADD(day, @DayCount, @MiladiDate)

	-- Return the result of the function
	Set @ShamsiDate = dbo.Date_MiladiToShamsi(@MiladiDate)

	Return @ShamsiDate

END
