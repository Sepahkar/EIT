CREATE TABLE [dbo].[HR_UserSlip](
	[id] [bigint] NULL,
	[PersonnelCode] [nvarchar](10) NOT NULL,
	[YearNumber] [smallint] NOT NULL,
	[MonthNumber] [smallint] NOT NULL,
	[ItemValue] [bigint] NOT NULL,
	[Code] [nvarchar](60) NULL,
	[UserName] [varchar](100) NOT NULL
) ON [PRIMARY]
