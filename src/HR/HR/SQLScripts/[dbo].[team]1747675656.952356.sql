ALTER TABLE [dbo].[Team]
ADD [UserCount]  AS ([dbo].[HR_GetTeamMemberCount]([TeamCode]))
