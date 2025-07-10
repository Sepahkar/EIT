CREATE FUNCTION [dbo].[HR_ConvertTimeToMinutes] 
(
	-- Add the parameters for the function here
	@TimeText varchar(10)
)
RETURNS int
AS
BEGIN
	Declare @TotalTimeMin int = 0

	--مکان کارکتر : را به دست می آوریم
	Declare @CharPosition tinyint = 0
	Set @CharPosition = CHARINDEX(':',@TimeText) 

	Declare @SplitTime varchar(5)

	--اگر دو نقطه وجود داشته باشد
	If @CharPosition > 1
	Begin
		Set @SplitTime = LEFT(@TimeText,@CharPosition-1)
		--کارکترهای سمت چپ، ساعت را نشان می دهند، آن را در 60 ضرب می کنیم
		If ISNUMERIC(@SplitTime)=1
			Set @TotalTimeMin = @SplitTime * 60
	End
	--اگر سمت راست : عددی وجود داشته باشد
	If LEN(@TimeText)-@CharPosition > 0
	Begin
		Set @SplitTime = RIGHT(@TimeText,LEN(@TimeText)-@CharPosition)

		--به دست آوردن دقیقه
		If ISNUMERIC(@SplitTime)=1
			Set @TotalTimeMin += @SplitTime
	End

	Return @TotalTimeMin
END
