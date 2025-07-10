CREATE TABLE [dbo].[HR_Payment](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[YearNumber] [int] NOT NULL,
	[Payment] [bigint] NULL,
	[InsuranceAmount] [bigint] NULL,
	[OtherPayment] [bigint] NULL,
	[PaymentCost] [bigint] NULL,
	[MonthNumber] [int] NOT NULL,
	[PersonnelCode] [nvarchar](10) NOT NULL,
	[BasePayment] [bigint] NULL,
	[Username] [nvarchar](100) NULL,
	[OverTime] [int] NULL,
	[OverTimePayment] [bigint] NULL,
	[Reward] [bigint] NULL,
	[TotalPayment] [bigint] NULL,
	[DataType] [smallint] NOT NULL
) ON [PRIMARY]
