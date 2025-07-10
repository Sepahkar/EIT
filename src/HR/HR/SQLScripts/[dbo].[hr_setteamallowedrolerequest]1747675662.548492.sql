CREATE TABLE [dbo].[HR_setteamallowedrolerequest](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[TeamAllowedRoles] [nvarchar](2000) NOT NULL,
	[RequestorId] [nvarchar](10) NOT NULL,
	[RequestDate] [date] NOT NULL,
	[ManagerId] [nvarchar](10) NOT NULL,
	[ManagerOpinion] [bit] NULL,
	[ManagerDate] [date] NULL,
	[CTOId] [nvarchar](10) NOT NULL,
	[CTOOpinion] [bit] NULL,
	[CTODate] [date] NULL,
	[DocId] [int] NULL,
	[StatusCode] [nvarchar](6) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
