CREATE TABLE [dbo].[HR_teamallowedroles](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[AllowedRoleCount] [smallint] NULL,
	[Comment] [nvarchar](500) NOT NULL,
	[RoleId] [int] NOT NULL,
	[SetTeamAllowedRoleRequest_id] [bigint] NULL,
	[TeamCode] [char](3) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
