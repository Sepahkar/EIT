CREATE view [dbo].[V_Payment_Average] As
SELECT 
ROW_NUMBER() Over(order by YearNumber, MonthNumber) As id,
YearNumber, MonthNumber,AVG(Payment) Payment, AVG(OtherPayment) OtherPayment, AVG(PaymentCost) PaymentCost, 
AVG(BasePayment) BasePayment, AVG(OverTimePayment) OverTimePayment, AVG(OverTime) OverTime,
AVG(Reward) Reward, AVG(TotalPayment) TotalPayment
  FROM [HR].[dbo].[HR_Payment]
  Group By YearNumber,MonthNumber
