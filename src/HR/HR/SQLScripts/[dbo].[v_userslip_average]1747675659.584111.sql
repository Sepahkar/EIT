	CREATE View [dbo].[V_UserSlip_Average] as
  Select    ROW_NUMBER() Over(order by YearNumber, MonthNumber) As id,
  YearNumber, MonthNumber, AVG(ItemValue) ItemValue, Code 
  From HR_UserSlip
Group By  YearNumber, MonthNumber,  Code
