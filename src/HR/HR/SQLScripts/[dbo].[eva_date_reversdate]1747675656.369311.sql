Create FUNCTION [dbo].[EVA_Date_ReversDate] (@DateStr varchar(10))
RETURNS varchar(10)

AS

BEGIN
DECLARE @TempStr varchar(10)
DECLARE @StartIndex int
DECLARE @SubStrLen int
DECLARE @i int

SET @TempStr = ''
SET @StartIndex = LEN(@DateStr) + 2
SET @i = LEN(@DateStr)
WHILE @i > 0
BEGIN
IF SUBSTRING(@DateStr,@i,1) IN ('/', '-')
BEGIN
SET @SubStrLen = @StartIndex - (@i + 2)
SET @StartIndex = @i + 1
SET @TempStr = @TempStr + SUBSTRING(@DateStr,@StartIndex,@SubStrLen) + SUBSTRING(@DateStr,@i,1)
END
SET @i = @i - 1
END
IF @TempStr <> ''
BEGIN
SET @SubStrLen = @StartIndex - 2
SET @TempStr = @TempStr + SUBSTRING(@DateStr,1,@SubStrLen)
END
ELSE
SET @TempStr = @DateStr
RETURN @TempStr
END





