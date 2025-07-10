CREATE TABLE [dbo].[Duties_roledescription](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[CreateDate] [datetime2](7) NULL,
	[ModifyDate] [datetime2](7) NULL,
	[Superior] [bit] NOT NULL,
	[Title] [nvarchar](4000) NOT NULL,
	[IsConfirm] [bit] NOT NULL,
	[Category_id] [bigint] NOT NULL,
	[CreatorUserName_id] [nvarchar](100) NULL,
	[LevelId] [bigint] NULL,
	[ModifierUserName_id] [nvarchar](100) NULL,
	[RoleId] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
