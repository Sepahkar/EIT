CREATE TABLE [dbo].[HR_newrolerequest](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[RoleTitle] [nvarchar](100) NOT NULL,
	[HasLevel] [bit] NOT NULL,
	[HasSuperior] [bit] NOT NULL,
	[AllowedTeams] [nvarchar](1000) NOT NULL,
	[RequestorId] [nvarchar](10) NOT NULL,
	[RequestDate] [date] NOT NULL,
	[ManagerId] [nvarchar](10) NOT NULL,
	[ManagerOpinion] [bit] NOT NULL,
	[ManagerDate] [date] NULL,
	[CTOId] [nvarchar](10) NULL,
	[CTOOpinion] [bit] NULL,
	[CTODate] [date] NULL,
	[ConditionsText] [nvarchar](1000) NULL,
	[DutiesText] [nvarchar](1000) NULL,
	[StatusCode] [nvarchar](6) NULL,
	[DocId] [int] NULL,
	[ManagerType_id] [bigint] NULL,
	[NewRoleTypeTitle] [nvarchar](100) NULL,
	[RoleType_id] [bigint] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
