CREATE TABLE [dbo].[AccessControl_userrolegrouppermission](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[OwnerPermissionGroup] [bigint] NULL,
	[OwnerPermissionRole] [int] NULL,
	[OwnerPermissionUser] [nvarchar](100) NULL,
	[PermissionCode] [nvarchar](10) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
