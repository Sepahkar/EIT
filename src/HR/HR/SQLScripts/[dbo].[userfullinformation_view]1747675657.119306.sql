CREATE View [dbo].[UserFullInformation_View] As
Select Username, FirstName, LastName, FatherName,ContractDate,
ContractEndDate, CT.Caption ContractType,
CASE Gender WHEN 1 THEN N'مرد' WHEN 0 THEN N'زن' ELSE N'نامشخص' END Gender, NationalCode, 
NumberOfChildren, CD.Caption DegreeType,  CM.Caption MilitaryStatus, CR.Caption Religion,
BirthDate, C.CityTitle BirthCity, IdentityNumber, U.IsActive,
CS.Caption UserStatus,CMA.Caption MarriageStatus, dbo.GetAllUserTeamRole(Username) UserTeamRoles
From Users U
Left Join HR_constvalue CT
On U.ContractType_id = CT.Id
Left Join HR_constvalue CD
On U.DegreeType_id = CD.id
Left Join HR_constvalue CM
On U.MilitaryStatus_id = CM.id
Left Join HR_constvalue CR
On U.Religion_id = CR.id
Left Join HR_city C
On U.BirthCity_id = C.id
Left Join HR_constvalue CMA
On U.MarriageStatus_id = CMA.id
Left Join HR_constvalue CS
On U.UserStatus_id = CS.id
