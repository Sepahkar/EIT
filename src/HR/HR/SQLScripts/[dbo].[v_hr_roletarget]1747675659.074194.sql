CREATE View [dbo].[V_HR_RoleTarget] As 
----سطح رو به دست میاریم برای همه سمت ها
With CTE_RoleLevel As (
Select R.RoleId,R.RoleName
,RL.LevelName,RL.id LevelId,R.HasLevel,R.HasSuperior
From Role R
Cross Join RoleLevel RL
Where R.HasLevel=1 And RoleId<>127
Union 
Select R.RoleId,R.RoleName
,'','' LevelId,R.HasLevel,R.HasSuperior From Role R
Where R.HasLevel=0 And RoleId<>127
)
---برای سمت های عملیاتی به غیر عملیاتی
,CTE_NoneTechnicalRoleTarget as (
Select ChR.RoleID_id RoleID,RG.RoleID_id RoleTargetID
,CHR.LevelId_id LevelID,L.LevelId LevelIdTargetID
,CHR.Superior,CHR.SuperiorTarget
,Education,Evaluation,ReEvaluation,Assessor,PmChange,ITChange

From HR_changerole CHR
Inner Join HR_rolegroup RG
-----سمت های غیر عملیاتی رو به دست میاریم
On RG.RoleGroup='NoneTechnicalRole'
Inner Join CTE_RoleLevel L
on L.RoleId=RG.RoleID_id

Where  CHR.RoleIdTarget_id=127
And  RG.RoleID_id<>127
And CHR.RoleID_id<>CHR.RoleIdTarget_id
),CTE_NoneTechnicalRole As (

---برای سمت های غیر عملیاتی به عملیاتی
Select RG.RoleID_id RoleID,CHR.RoleIdTarget_id RoleTargetID
,L.LevelId LevelID,CHR.LevelIdTarget_id LevelIdTargetID
,CHR.Superior,CHR.SuperiorTarget
,Education,Evaluation,ReEvaluation,Assessor,PmChange,ITChange

From HR_changerole CHR
Inner Join HR_rolegroup RG
-----سمت های غیر عملیاتی رو به دست میاریم
On RG.RoleGroup='NoneTechnicalRole'
Inner Join CTE_RoleLevel L
on L.RoleId=RG.RoleID_id
Where  CHR.RoleId_id=127
And  RG.RoleID_id<>127
And RG.RoleID_id<>CHR.RoleIdTarget_id)
,CTE_RoleBase As (
--برای سمت پرسنل آزمایشی
Select 117 RoleID
,RL.RoleId RoleTargetID
,'' LevelID,RL.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange

From CTE_RoleLevel RL
Where RL.RoleId Not IN (Select RoleID_id From HR_rolegroup Where RoleGroup='Manager')
And RL.RoleId<>117
)
,CTE_RoleBaseSuprier As (
--برای ارشد سمت پرسنل آزمایشی
Select 117 RoleID
,RL.RoleId RoleTargetID
,0 LevelID,RL.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,0) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange

From CTE_RoleLevel RL
Where RL.RoleId Not IN (Select RoleID_id From HR_rolegroup Where RoleGroup='Manager')
And RL.HasSuperior=1 
And LevelId<=5
And RL.RoleId<>117)
,CTE_TechnicalRole As(
---برای سمت های  عملیاتی به عملیاتی
Select CHR.RoleID_id RoleID,CHR.RoleIdTarget_id RoleTargetID
,CHR.LevelId_id LevelID,CHR.LevelIdTarget_id LevelIdTargetID
,CHR.Superior,CHR.SuperiorTarget
,Education,Evaluation,ReEvaluation,Assessor,PmChange,ITChange

From HR_changerole CHR
Where  CHR.RoleId_id<>127
And  CHR.RoleIdTarget_id<>127
)
,CTE_NoneTechnicalRoleSelf As(
---برای سمت های غیر عملیاتی به غیر عملیاتی
Select 
R.RoleId RoleID,R2.RoleId RoleTargetID
,R.LevelId LevelID,R2.LevelId LevelIdTargetID
,Convert(bit,0)  Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education, Convert(bit,1) Evaluation,
Convert(bit,1) ReEvaluation
,'' Assessor
,Convert(bit,0) PmChange,Convert(bit,1) ITChange

From CTE_RoleLevel R
Cross Join CTE_RoleLevel R2
Where R.RoleId in (Select RoleID_id From HR_rolegroup Where RoleGroup='NoneTechnicalRole')
And  R2.RoleId in (Select RoleID_id From HR_rolegroup Where RoleGroup='NoneTechnicalRole')
),
----برای تبدیل مدیران به همه سمت ها
CTE_Manager As (
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleId  IN (Select RoleID_id From HR_rolegroup Where RoleGroup='Manager')
And RL.RoleId<>RL2.RoleId
),
----برای تبدیل مدیران به ارشد همه سمت ها
CTE_ManagerSuprier As (
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,0) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleId  IN (Select RoleID_id From HR_rolegroup Where RoleGroup='Manager')
And RL.RoleId<>RL2.RoleId
And RL2.HasSuperior=1
And RL2.LevelId <= 5
),
--برای پشتیبان جونیور به ارشد
CTE_JuniorSupporterSuprier As (
Select  RL.RoleId --پشتیبان
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,0) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleId  =69 --پشتیبان
And RL2.RoleId = 69
And RL2.HasSuperior=1
And RL2.LevelId <= RL.LevelId
And RL2.LevelId <= 5)

---تغییرات برای تغییر سمت 
,CTE_RoleChaneg As (
Select * From CTE_NoneTechnicalRole
Union
Select *  From CTE_NoneTechnicalRoleTarget
Union 
Select * From CTE_RoleBase
Union 
Select * From CTE_RoleBaseSuprier
union 
Select * From CTE_TechnicalRole
union 
Select * From CTE_Manager
union
Select * From CTE_ManagerSuprier
union
select * From CTE_JuniorSupporterSuprier
union
Select * From CTE_NoneTechnicalRoleSelf),CTE_RequestType As (
----برای تایپ 4 یعنی تعریف جدیدسمت میتواند از گروه خود انتخاب کند
Select RC.*,'4' RequestType From CTE_RoleChaneg RC
Inner Join HR_rolegroup  Rg
On RC.RoleID=RG.RoleID_id
Inner Join HR_rolegroup  Rg2
On RC.RoleTargetID=RG2.RoleID_id
Where RG.RoleGroup=RG2.RoleGroup
And RoleID<>RoleTargetID
Union 
----برای حالتی که میخواد استثنا انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'4' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
Union 
----برای حالتی که میخواد استثنا ارشد باشه انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,1) Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'4' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
And RL.LevelId <= 5
Union 
----برای حالتی که میخواد استثنا ارشد باشه ارشد  انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,1) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'4' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
And RL.LevelId <= 5
And RL2.LevelId <= 5
Union 
----برای حالتی که میخواد استثنا  باشه ارشد  انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'4' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
And RL2.LevelId <= 5
Union 
--برای تایپ سمت و تیم جدید
Select RC.*,'6' RequestType From CTE_RoleChaneg RC
Inner Join HR_rolegroup  Rg
On RC.RoleID=RG.RoleID_id
Inner Join HR_rolegroup  Rg2
On RC.RoleTargetID=RG2.RoleID_id
Where RG.RoleGroup=RG2.RoleGroup
And RoleID<>RoleTargetID
Union
----برای حالتی که میخواد استثنا انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'6' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
Union 
----برای حالتی که میخواد استثنا ارشد باشه انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,1) Superior,Convert(bit,0) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'6' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
And RL.LevelId <= 5
Union 
----برای حالتی که میخواد استثنا ارشد باشه ارشد  انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,1) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'6' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
And RL.LevelId <= 5
And RL2.LevelId <= 5
Union 
----برای حالتی که میخواد استثنا  باشه ارشد  انتخاب کند
Select  RL.RoleID
,RL2.RoleId RoleTargetID
,RL.LevelId LevelID,RL2.LevelId LevelIdTargetID
,Convert(bit,0) Superior,Convert(bit,1) SuperiorTarget
,Convert(bit,1) Education,Convert(bit,1) Evaluation,Convert(bit,1) ReEvaluation
,'' Assessor,Convert(bit,1) PmChange,Convert(bit,1) ITChange
,'6' RequestType
From CTE_RoleLevel RL
Cross Join CTE_RoleLevel RL2
Where RL.RoleID in(63,57,58,55,56)
And RL2.RoleId In (72,69)
And RL2.LevelId <= 5
Union 
--برای تایپ جابه جایی سمت 
Select RC.*,'1' RequestType From CTE_RoleChaneg RC
Where RoleID<>RoleTargetID
Union 
--برای تایپ جابهجایی سمت و تیم 
Select RC.*,'3' RequestType From CTE_RoleChaneg RC
Where RoleID<>RoleTargetID
union 
---برای تایپ تغییر سطح
Select RC.*,'8' RequestType From CTE_RoleChaneg RC
Where RoleID=RoleTargetID 
And ((Isnull(LevelIdTargetID,0)+1=Isnull(LevelID,0)) Or 
(RC.Superior<>RC.SuperiorTarget And Isnull(LevelIdTargetID,0)=Isnull(LevelID,0)))
)
Select R.RoleID,R.RoleTargetID
,RO.RoleName RoleTargetName
,R.Education,R.Evaluation
,R.ITChange,isnull(R.LevelID,0)LevelID
,isnull(R.LevelIdTargetID,0) LevelIdTargetID,R.PmChange,R.ReEvaluation,R.Superior,R.SuperiorTarget
,R.RequestType
,(Case When R.Assessor in('106','108','111','115','88') Then 
(Select UserName From UserTeamRole Where RoleId=Assessor) Else '' End) Assessor
,ROW_NUMBER()Over(order by R.RoleID) Id
From CTE_RequestType R
Inner Join Role Ro
On Ro.RoleId=R.RoleTargetID


