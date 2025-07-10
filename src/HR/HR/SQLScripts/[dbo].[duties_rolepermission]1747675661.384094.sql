CREATE TABLE [dbo].[Duties_rolepermission](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[CreateDate] [datetime2](7) NULL,
	[ModifyDate] [datetime2](7) NULL,
	[CreatorUserName_id] [nvarchar](100) NULL,
	[ModifierUserName_id] [nvarchar](100) NULL,
	[Permission_id] [nvarchar](10) NOT NULL,
	[Role_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
