CREATE TABLE [dbo].[HR_changerole](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[Superior] [bit] NOT NULL,
	[SuperiorTarget] [bit] NOT NULL,
	[Education] [bit] NOT NULL,
	[Educator] [nvarchar](100) NULL,
	[Evaluation] [bit] NOT NULL,
	[Assessor] [nvarchar](100) NULL,
	[RequestGap] [int] NULL,
	[Assessor2] [nvarchar](100) NULL,
	[ReEvaluation] [bit] NOT NULL,
	[PmChange] [bit] NOT NULL,
	[ITChange] [bit] NOT NULL,
	[LevelId_id] [bigint] NULL,
	[LevelIdTarget_id] [bigint] NULL,
	[RoleID_id] [int] NOT NULL,
	[RoleIdTarget_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
