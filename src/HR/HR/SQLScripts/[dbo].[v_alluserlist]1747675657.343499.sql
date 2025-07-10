CREATE VIEW [dbo].[V_AllUserList]
AS
SELECT     U.Username, FirstName, LastName, U.NationalCode, ContractDate, T .TeamCode, TeamName, UTR.RoleId, RoleName, U.IsActive UserActive, 1 RoleActive
FROM        UserTeamRole UTR INNER JOIN
                  Users U ON UTR.UserName = U.UserName INNER JOIN
                  Team T ON T .TeamCode = UTR.TeamCode INNER JOIN
                  Role R ON R.RoleId = UTR.RoleId
UNION
SELECT     U.Username, FirstName, LastName, U.NationalCode, ContractDate, T .TeamCode, TeamName, UTR.RoleId, RoleName, U.IsActive UserActive, 0 ActiveRole
FROM        PreviousUserTeamRole UTR INNER JOIN
                  Users U ON UTR.UserName = U.UserName INNER JOIN
                  Team T ON T .TeamCode = UTR.TeamCode INNER JOIN
                  Role R ON R.RoleId = UTR.RoleId
UNION
SELECT     Username, FirstName, LastName, NationalCode,  ContractDate, NULL, NULL, NULL, NULL, IsActive, 0
FROM        Users
WHERE     Username NOT IN
                      (SELECT     Username
                       FROM        UserTeamRole
                       UNION
                       SELECT     Username
                       FROM        PreviousUserTeamRole)
