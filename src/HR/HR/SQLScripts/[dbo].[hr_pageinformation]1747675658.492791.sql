CREATE TABLE [dbo].[HR_pageinformation](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[PageName] [nvarchar](30) NOT NULL,
	[ColorSet] [nvarchar](30) NOT NULL,
	[EnglishName] [nvarchar](30) NOT NULL,
	[IconName] [nvarchar](30) NOT NULL,
	[ShowDetail] [bit] NOT NULL,
	[OrderNumber] [smallint] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
