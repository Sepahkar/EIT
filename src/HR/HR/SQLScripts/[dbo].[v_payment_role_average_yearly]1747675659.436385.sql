CREATE view [dbo].[V_Payment_Role_Average_Yearly] as
Select ROW_NUMBER() Over(order by YearNumber,RoleId,LevelId_id) Id,
YearNumber,RoleId,LevelId_id,
AVG(Payment) Payment, AVG(OtherPayment) OtherPayment, AVG(PaymentCost) PaymentCost, 
AVG(OverTime) OverTime, AVG(OverTimePayment) OverTimePayment, AVG(Reward) Reward, 
AVG(TotalPayment) TotalPayment , AVG(BasePayment) BasePayment
From V_Payment_Role_Average
Group By YearNumber,RoleId,LevelId_id
