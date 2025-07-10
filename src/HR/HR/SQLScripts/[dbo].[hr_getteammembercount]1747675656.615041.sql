CREATE FUNCTION [dbo].[HR_GetTeamMemberCount] 
(
	-- Add the parameters for the function here
	@TeamCode char(3)
)
RETURNS tinyint
AS
BEGIN
	
	Return (Select Count(*) From Team Where TeamCode = @TeamCode)

END
