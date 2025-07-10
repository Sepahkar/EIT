CREATE VIEW [dbo].[KeyMembers]
AS
SELECT DISTINCT 0 AS Id, u.UserName, REPLACE(u.UserName, '@eit', '') AS UserAlone, u.FirstName, u.LastName, t.TeamName, t.TeamCode, r.RoleName, r.RoleId, utr.Superior
FROM            dbo.HR_rolegroup AS rg INNER JOIN
                         dbo.UserTeamRole AS utr ON utr.RoleId = rg.RoleID_id INNER JOIN
                         dbo.Users AS u ON u.UserName = utr.UserName INNER JOIN
                         dbo.Team AS t ON t.TeamCode = utr.TeamCode INNER JOIN
                         dbo.Role AS r ON r.RoleId = utr.RoleId
WHERE        (rg.RoleGroup = 'Manager') OR
                         (utr.Superior = 1)
