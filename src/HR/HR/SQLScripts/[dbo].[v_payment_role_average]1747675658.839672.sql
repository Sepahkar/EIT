CREATE view [dbo].[V_Payment_Role_Average] As
SELECT ROW_NUMBER() Over(order by YearNumber, MonthNumber,UTR.RoleId, UTR.LevelId_id) As id,
YearNumber,MonthNumber, UTR.RoleId, UTR.LevelId_id,
AVG(Payment) Payment, AVG(OtherPayment) OtherPayment, AVG(PaymentCost) PaymentCost, 
AVG(BasePayment) BasePayment, AVG(OverTimePayment) OverTimePayment,  AVG(OverTime) OverTime,
AVG(Reward) Reward, AVG(TotalPayment) TotalPayment
  FROM [HR].[dbo].[HR_Payment] P
  Inner Join UserTeamRoleAll UTR
  On P.Username = UTR.UserName
  Group By YearNumber,MonthNumber, UTR.RoleId, UTR.LevelId_id
