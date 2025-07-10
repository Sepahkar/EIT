CREATE View [dbo].[UserWithoutTeamRole] As
Select UserName, FirstName, LastName, NationalCode, 
ContractDateMiladi as ContractDate,  dbo.Date_MiladiToShamsi(ContractDateMiladi) ContractDateShamsi,
ContractEndDateMiladi as ContractEndDate,  dbo.Date_MiladiToShamsi(ContractEndDateMiladi) ContractEndDateShamsi
From Users
Where UserName Not In
(Select UserName From PreviousUserTeamRole
UNION 
Select UserName From UserTeamRole)
