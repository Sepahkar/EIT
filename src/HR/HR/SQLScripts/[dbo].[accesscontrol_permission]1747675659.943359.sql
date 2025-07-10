CREATE TABLE [dbo].[AccessControl_permission](
	[Code] [nvarchar](10) NOT NULL,
	[Title] [nvarchar](100) NOT NULL,
	[PermissionType] [nvarchar](1) NOT NULL,
	[AppCode_id] [nvarchar](6) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
