CREATE TABLE [dbo].[HR_userhistory](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[UserName] [nvarchar](300) NOT NULL,
	[AuthLoginKey] [nvarchar](300) NULL,
	[RequestDate] [datetime2](7) NOT NULL,
	[EnterDate] [datetime2](7) NULL,
	[RequestUrl] [nvarchar](300) NULL,
	[EnterUrl] [nvarchar](300) NULL,
	[IP] [nvarchar](39) NULL,
	[UserAgent] [nvarchar](300) NULL,
	[ChangedUserInfo] [bit] NULL,
	[AppName] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
