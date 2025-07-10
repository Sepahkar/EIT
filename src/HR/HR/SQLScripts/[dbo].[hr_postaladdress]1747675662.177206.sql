CREATE TABLE [dbo].[HR_postaladdress](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](100) NULL,
	[AddressText] [nvarchar](500) NULL,
	[No] [nvarchar](20) NULL,
	[UnitNo] [smallint] NULL,
	[PostalCode] [bigint] NULL,
	[CityDistrict_id] [bigint] NULL,
	[Person_id] [varchar](100) NULL,
	[City_id] [int] NOT NULL,
	[IsDefault] [bit] NOT NULL,
	[PersonNationalCode] [nvarchar](10) NULL,
 CONSTRAINT [PK__HR_posta__3213E83F97BFA363] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
