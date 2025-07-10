CREATE PROCEDURE [dbo].[auth2_CrossDBSynchromization]

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;


	

	-- INSERT NEW ACTIVE USERS THAT NOT IN AUTH2_USERS
    INSERT INTO SalesManagement.dbo.auth2_user (
	   [password]
      ,[last_login]
      ,[is_superuser]
      ,[username]
      ,[first_name]
      ,[last_name]
      ,[email]
      ,[is_staff]
      ,[is_active]
      ,[date_joined]
      ,[national_code]
      ,[team_roles]
      ,[gender])
	 SELECT 0
      ,NULL
      ,0
      ,[username2]
      ,FirstName
      ,LastName
      ,LOWER(CONCAT(Username2, '@iraneit.com'))
      ,0
      ,1
      ,GETDATE()
      ,NationalCode
	  ,NULL
      ,Gender
	  FROM hr.dbo.Users
	WHERE NationalCode NOT IN (SELECT national_code FROM SalesManagement.dbo.auth2_user) 
	AND NationalCode IS NOT NULL 
	AND IsActive = 1


	-- UPDATE INACTIVE USERS
	UPDATE SalesManagement.dbo.auth2_user
	SET is_active = 0 
	WHERE national_code IN (SELECT NATIONALCODE FROM HR.DBO.Users WHERE IsActive = 0)


	-- UPDATE USER TEAM ROLES 
	UPDATE SalesManagement.dbo.auth2_user
	SET team_roles = UTR.UserTeamRoles
	FROM  SalesManagement.dbo.auth2_user  A2U
	INNER JOIN HR.DBO.Auth_UserTeamRole UTR ON UTR.NationalCode = A2U.national_code
	
END
