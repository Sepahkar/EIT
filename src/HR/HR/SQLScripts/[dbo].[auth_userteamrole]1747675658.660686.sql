CREATE View [dbo].[Auth_UserTeamRole] As
SELECT 
    NationalCode, 
    Username, 
    FirstName, 
    LastName, 
    Gender, 
    IsActive,
   
    JSON_QUERY(
        '{' +
        '"current": [' + ISNULL(STRING_AGG(CASE WHEN Current_Previous = 'C' THEN CAST(UserTeamRole AS NVARCHAR(MAX)) END, ','), '') + '],' +
        '"previous": [' + ISNULL(STRING_AGG(CASE WHEN Current_Previous = 'P' THEN CAST(UserTeamRole AS NVARCHAR(MAX)) END, ','), '') + ']' +
        '}'
    ) AS UserTeamRoles

FROM 
    UserTeamRoleJSON
GROUP BY 
    NationalCode, 
    Username, 
    FirstName, 
    LastName, 
    Gender, 
    IsActive

