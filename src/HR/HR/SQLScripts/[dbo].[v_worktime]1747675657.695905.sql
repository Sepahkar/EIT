CREATE View [dbo].[V_WorkTime] As
SELECT  [YearNo]

      ,Sum(dbo.HR_ConvertTimeToMinutes([WorkHours]))/60 WorkHours
	  
       ,Sum(dbo.HR_ConvertTimeToMinutes([RemoteHours]))/60.0 RemoteHours
      ,Sum([RemoteDays])RemoteDays
     , Sum(dbo.HR_ConvertTimeToMinutes([OverTime]))/60.0 OverTime
     , Sum(dbo.HR_ConvertTimeToMinutes([DeductionTime]))/60.0 DeductionTime
      ,Sum(dbo.HR_ConvertTimeToMinutes([OffTimeHourly]))/60.0 OffTimeHourly
      ,Sum([OffTimeDaily])OffTimeDaily
      ,[UserName]
	  ,ROW_NUMBER() Over (order by YearNo) Id
  FROM [dbo].[WorkTime]
  Group By UserName,YearNo
