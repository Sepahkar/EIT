CREATE TABLE [dbo].[EVA_Users](
	[UserName] [varchar](100) NOT NULL,
	[PersonnelCode] [varchar](10) NULL,
	[LastName] [nvarchar](200) NULL,
	[FirstName] [nvarchar](200) NULL,
	[FatherName] [nvarchar](100) NULL,
	[Gender] [bit] NULL,
	[IsActive] [bit] NOT NULL,
	[MobileNo] [varchar](12) NULL,
	[TelNo] [varchar](12) NULL,
	[Address] [nvarchar](2000) NULL,
	[BirthDate] [varchar](10) NULL,
	[MilitaryStatus] [tinyint] NULL,
	[ContractDate] [varchar](10) NULL,
	[MaridageStatus] [bit] NULL,
	[Comment] [nvarchar](max) NULL,
	[DegreeType] [tinyint] NULL,
	[FieldOfStudy] [nvarchar](255) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
