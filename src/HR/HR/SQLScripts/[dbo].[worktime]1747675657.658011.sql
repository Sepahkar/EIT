CREATE TABLE [dbo].[WorkTime](
	[PersonnelCode] [varchar](10) NOT NULL,
	[YearNo] [smallint] NOT NULL,
	[MonthNo] [tinyint] NOT NULL,
	[WorkHours] [varchar](10) NULL,
	[RemoteHours] [varchar](10) NULL,
	[RemoteDays] [tinyint] NULL,
	[OverTime] [varchar](10) NULL,
	[DeductionTime] [varchar](10) NULL,
	[OffTimeHourly] [varchar](10) NULL,
	[OffTimeDaily] [int] NULL,
	[UserName] [varchar](100) NULL,
	[Id] [bigint] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK_EVA_WorkTime] PRIMARY KEY CLUSTERED 
(
	[PersonnelCode] ASC,
	[YearNo] ASC,
	[MonthNo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
