CREATE VIEW [dbo].[TeamInformation]
AS
WITH CTE_teamcount AS (SELECT        TeamCode, COUNT(*) AS TeamCount
                                                         FROM            dbo.UserTeamRole AS utr
                                                         GROUP BY TeamCode)
    SELECT        Row_number() OVER (ORDER BY tc.TeamCount) AS Id, t.TeamCode, t.TeamName, ISNULL(std.TeamDescription, '') AS TeamDesc, ISNULL(std.ShortDescription, '') AS ShortDesc, tc.TeamCount, t.IsActive IsTeamActive
     FROM            ServiceBook.dbo.ServiceBook_teamdescription AS std RIGHT OUTER JOIN
                              dbo.Team AS t ON t.TeamCode = std.TeamCode AND std.YearNumber = 1402 INNER JOIN
                              CTE_teamcount AS tc ON tc.TeamCode = t.TeamCode
