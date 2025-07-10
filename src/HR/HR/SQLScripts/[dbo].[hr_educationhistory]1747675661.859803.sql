CREATE TABLE [dbo].[HR_educationhistory](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[StartDate] [date] NULL,
	[EndDate] [date] NULL,
	[StartYear] [smallint] NULL,
	[EndYear] [smallint] NULL,
	[IsStudent] [bit] NOT NULL,
	[GPA] [numeric](4, 2) NULL,
	[EducationTendency_id] [bigint] NULL,
	[Person_id] [varchar](100) NOT NULL,
	[University_id] [bigint] NULL,
	[Degree_Type_id] [bigint] NOT NULL,
	[PersonNationalCode] [nvarchar](10) NULL,
 CONSTRAINT [PK__HR_educa__3213E83F4D02780D] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
