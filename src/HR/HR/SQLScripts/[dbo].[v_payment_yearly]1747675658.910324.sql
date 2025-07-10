CREATE view [dbo].[V_Payment_Yearly] as
Select ROW_NUMBER() Over(order by YearNumber,Username) Id,
YearNumber, PersonnelCode, Username,
AVG(Payment) Payment, AVG(OtherPayment) OtherPayment, AVG(PaymentCost) PaymentCost, 
AVG(OverTime) OverTime, AVG(OverTimePayment) OverTimePayment, AVG(Reward) Reward, 
AVG(TotalPayment) TotalPayment , AVG(BasePayment) BasePayment
From HR_Payment
Group By YearNumber, PersonnelCode, Username
