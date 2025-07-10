CREATE TABLE [dbo].[UserTeamRole](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[StartDate] [varchar](10) NOT NULL,
	[EndDate] [varchar](10) NULL,
	[RoleId] [int] NOT NULL,
	[TeamCode] [char](3) NOT NULL,
	[UserName] [varchar](100) NOT NULL,
	[LevelId_id] [bigint] NULL,
	[Superior] [bit] NOT NULL,
	[ManagerUserName_id] [varchar](100) NULL,
	[Comment] [nvarchar](1000) NULL,
	[ManagerNationalCode] [nvarchar](10) NULL,
	[NationalCode] [nvarchar](10) NULL,
 CONSTRAINT [PK__UserTeam__3213E83F6DF7641E] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
