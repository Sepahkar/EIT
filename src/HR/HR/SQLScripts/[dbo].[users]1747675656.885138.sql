ALTER TABLE [dbo].[Users]
ADD Username2 AS (left([Username],charindex('@',[UserName])-(1)))
