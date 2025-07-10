Create FUNCTION [dbo].[Date_SubStrCount](@SubStr varchar(8000), @MainText Text) 
RETURNS int 
AS 
BEGIN 
DECLARE @StrCount int
DECLARE @StrPos int

SET @StrCount = 0
SET @StrPos = 0
SET @StrPos = CHARINDEX( @SubStr, @MainText, @StrPos)

WHILE @StrPos > 0
BEGIN
SET @StrCount = @StrCount + 1
SET @StrPos = CHARINDEX( @SubStr, @MainText, @StrPos+1)
END

RETURN @StrCount 
END




