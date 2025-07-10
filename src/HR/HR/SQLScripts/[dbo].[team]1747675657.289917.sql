CREATE TABLE [dbo].[Team](
	[TeamCode] [char](3) NOT NULL,
	[TeamName] [nvarchar](100) NOT NULL,
	[ActiveInService] [bit] NOT NULL,
	[ActiveInEvaluation] [bit] NOT NULL,
	[GeneralManager_id] [varchar](100) NULL,
	[SupportManager_id] [varchar](100) NULL,
	[TestManager_id] [varchar](100) NULL,
	[IsActive] [bit] NOT NULL,
	[GeneralManagerNationalCode] [nvarchar](10) NULL,
	[SupportManagerNationalCode] [nvarchar](10) NULL,
	[TestManagerNationalCode] [nvarchar](10) NULL,
	[TeamDescription] [nvarchar](max) NULL,
	[ShortDescription] [nvarchar](1000) NULL,
	[UserCount]  AS ([dbo].[HR_GetTeamMemberCount]([TeamCode])),
 CONSTRAINT [PK__Team__550135094BD77BFA] PRIMARY KEY CLUSTERED 
(
	[TeamCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
