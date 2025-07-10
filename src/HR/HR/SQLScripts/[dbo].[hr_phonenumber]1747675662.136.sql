CREATE TABLE [dbo].[HR_phonenumber](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[TelNumber] [bigint] NOT NULL,
	[Title] [nvarchar](50) NULL,
	[Person_id] [varchar](100) NULL,
	[TelType_id] [bigint] NOT NULL,
	[Province_id] [bigint] NULL,
	[IsDefault] [bit] NOT NULL,
	[PersonNationalCode] [nvarchar](10) NULL,
 CONSTRAINT [PK__HR_phone__3213E83F7168D750] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
