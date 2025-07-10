CREATE FUNCTION [dbo].[GetAllUserTeamRole] 
(
	-- Add the parameters for the function here
	@Username varchar(100)
)
RETURNS nvarchar(1000)
AS
BEGIN
	-- Declare the return variable here
	DECLARE @AllUserTeamRole nvarchar(1000) = ''
	Declare @UserTeamRole nvarchar(100)

	Declare CurAllTeamRole Cursor LOCAL FORWARD_ONLY FAST_FORWARD READ_ONLY
	For Select RoleName + N' تیم ' + TeamName + N' از ' + StartDate + N' تا ' + 
	CASE  WHEN EndDate IS NULL THEN N'کنون' ELSE EndDate END As UserTeamRole 
	From UserTeamRoleAll 
	Where Username = @Username
	Order By StartDate

	Open CurAllTeamRole

	FETCH Next From CurAllTeamRole into @UserTeamRole
	--به ازای هر سمت این کار را می کنیم
	WHILE @@FETCH_STATUS = 0
	BEGIN
		--در صورتی که اولین سمت نباشد کاما اضافه می کنیم
		if @AllUserTeamRole = '' 
			Set @AllUserTeamRole = @AllUserTeamRole + ', '
		--سمت را به لیست سمت های فرد اضافه می کنیم
		Set @AllUserTeamRole = @AllUserTeamRole + @UserTeamRole
		--رکورد بعدی را واکشی می کنیم
		FETCH Next From CurAllTeamRole into @UserTeamRole
	END
	--کرسر را بسته و حافظه را آزاد می کنیم
	Close CurAllTeamRole
	Deallocate CurAllTeamRole
	-- Return the result of the function
	RETURN @AllUserTeamRole

END
