CREATE TABLE [dbo].[HR_organizationchartteamrole](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[RoleCount] [int] NULL,
	[ManagerUserName_id] [varchar](100) NULL,
	[OrganizationChartRole_id] [bigint] NOT NULL,
	[TeamCode_id] [char](3) NOT NULL,
	[ManagerNationalCode] [nvarchar](10) NULL,
 CONSTRAINT [PK__HR_organ__3213E83F074C4FF4] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
