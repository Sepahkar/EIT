CREATE TABLE [dbo].[Cartable_documenrflow](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[ReciveDate] [date] NULL,
	[IsRead] [bit] NOT NULL,
	[SendDate] [date] NULL,
	[DueDate] [date] NULL,
	[PersonalDueDate] [date] NULL,
	[DocumentId_id] [bigint] NULL,
	[InboxOwner_id] [nvarchar](100) NOT NULL,
	[PreviousFlow_id] [bigint] NULL,
	[SenderUser_id] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
