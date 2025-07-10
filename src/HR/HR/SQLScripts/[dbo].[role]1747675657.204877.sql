CREATE TABLE [dbo].[Role](
	[RoleId] [int] NOT NULL,
	[RoleName] [nvarchar](100) NOT NULL,
	[HasLevel] [bit] NOT NULL,
	[HasSuperior] [bit] NOT NULL,
	[Comment] [nvarchar](200) NULL,
	[NewRoleRequest_id] [bigint] NULL,
	[RoleTypeCode] [char](1) NULL,
	[ManagerType_id] [bigint] NULL,
	[ManagerType] [nvarchar](100) NULL,
	[RoleType] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[RoleId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
