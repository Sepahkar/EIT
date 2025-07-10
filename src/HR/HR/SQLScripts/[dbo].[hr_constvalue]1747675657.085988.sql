CREATE TABLE [dbo].[HR_constvalue](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[Caption] [nvarchar](50) NOT NULL,
	[Code] [nvarchar](100) NOT NULL,
	[IsActive] [bit] NOT NULL,
	[OrderNumber] [smallint] NULL,
	[ConstValue] [int] NULL,
	[Parent_id] [bigint] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
