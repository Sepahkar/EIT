CREATE PROCEDURE [dbo].[CorectInputData] 
AS
BEGIN

	SET NOCOUNT ON;

	--جدول پرسنلي
	--جايگزيني حرف ي
	Update Users
	Set FirstName =  REPLACE (FirstName,N'ي',N'ی')
	, LastName =  REPLACE (LastName,N'ي',N'ی')
	, FatherName =  REPLACE (FatherName,N'ي',N'ی')


	--جدول سمت
	--جايگزيني حرف ي
	Update Role 
	Set RoleName =  REPLACE (RoleName,N'ي',N'ی')


	--جدول تيم
	--جايگزيني حرف ي	Update Team
	Update Team
	Set TeamName= REPLACE (TeamName,N'ي',N'ی')


END
