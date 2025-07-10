CREATE VIEW [dbo].[ChangeUserTeamRole]
AS
SELECT     UTR.StartDate, UTR.EndDate, R.RoleName, RL.LevelName, T.TeamName, UTR.UserName
FROM        dbo.UserTeamRoleAll AS UTR INNER JOIN
                  dbo.Role AS R ON UTR.RoleId = R.RoleId INNER JOIN
                  dbo.Team AS T ON UTR.TeamCode = T.TeamCode LEFT OUTER JOIN
                  dbo.RoleLevel AS RL ON UTR.LevelId_id = RL.id
