CREATE VIEW [dbo].[UserTeamRoleAll]
AS
SELECT        UTR.ID, StartDate, EndDate, UTR.RoleId, R.RoleName, T .TeamCode, TeamName, UTR.UserName, FirstName, LastName, U.NationalCode, LevelId_id, LevelName, Superior, ManagerUserName_id
FROM            UserTeamRole UTR INNER JOIN
                         Users U ON UTR.Username = U.Username INNER JOIN
                         Role R ON UTR.RoleId = R.RoleId LEFT JOIN
                         RoleLevel RL ON LevelId_id = RL.id LEFT JOIN
                         Team T ON UTR.TeamCode = T .TeamCode
UNION
/* دو تا سلکتور ور با هم یکی میکند*/ SELECT UTR.ID, StartDate, EndDate, UTR.RoleId, R.RoleName, T .TeamCode, TeamName, UTR.UserName, FirstName, LastName, U.NationalCode, LevelId_id, LevelName, Superior, ManagerUserName_id
FROM            PreviousUserTeamRole UTR INNER JOIN
                         Users U ON UTR.Username = U.Username INNER JOIN
                         Role R ON UTR.RoleId = R.RoleId LEFT JOIN
                         RoleLevel RL ON LevelId_id = RL.id LEFT JOIN
                         Team T ON UTR.TeamCode = T .TeamCode
