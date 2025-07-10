CREATE PROCEDURE [dbo].[HR_GetAssessorsAndEducators]   

  @TeamCode CHar(3)----اگر تیم جدید داشت جدید اگر نه قبلی  
  ,@InfoID Int  
 , @RoleIdTarget int----اگر سمت جدید داشت جدید اگر نه قبلی  
 , @LevelIdTarget int----اگر سطح جدید داشت جدید اگر نه قبلی  
 , @SuperiorTarget Bit----اگر ارشدیت جدید داشت جدید اگر نه قبلی  
 , @Temporary Bit=0 -----اگر 1 باشد موقت اگر 0 باشد دائمی است
 ,	@Type bit =0--اگر تایپ 0 بود یعنی تغییر اگر 1 بود یعنی جدید
  
AS  
BEGIN  
-----سمت و تیم و سطح قبلی و به دست میاریم  
  Declare @RoleId int  
  Declare @LevelId int  
  Declare @Superior Bit  
  Declare @TeamCodeOld CHar(3) 
  Declare @Test Tinyint
  Select  @RoleId=RoleId,@LevelId=LevelId_id,@Superior=Superior  
  ,@TeamCodeOld=TeamCode  
  From UserTeamRole  
  WHere Id=@InfoID  

-----برای پرسنل آموزشی 
if @RoleId=117 And @TeamCodeOld='EDU'
	Begin
		Select Convert(bit,1) As Education,(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U')) Educator
		,Convert(bit,1) As Evaluation
		,Convert(bit,1) As PmChange ,Convert(bit,1) As ITChange ,''RequestGap
		,Convert(bit,1) As ReEvaluation
		,(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U')) Assessor2
		,(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'N')) EducatorName,(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'N'))  AssessorName ,(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'N')) Assessor2Name,
		(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U')) Assessor,Convert(bit,1) As Confirm
	
			
	
	
	End
	Else 
Begin 

-------اگر مدیر محصول باشد حتما ارشد است
If @RoleIdTarget = 58 
	Begin
	Set @SuperiorTarget = 1
	Set @LevelIdTarget = NULL
	End
-----چک میشود که با هیچ سمت و تیم و سطح در حال حاضر یکی نباشد.
	;With CTE_UserReq 
	As (Select @TeamCode TeamCode,@RoleIdTarget RoleIdTarget
	,ISNull(@LevelIdTarget,0) LevelIdTarget,@SuperiorTarget SuperiorTarget)
	 ,CTE_UserOld As (
	 Select *,COUNT(*) Over ()  As CountRow
	From UserTeamRole U
	Where username in (Select UserName From UserTeamRole WHere Id=@InfoID  )
	)
 	Select Distinct @Test=CountRow-COUNT(*)Over () From CTE_UserOld U
	 Cross JOin CTE_UserReq R
	 Where (U.TeamCode<>R.TeamCode Or RoleId<>RoleIdTarget OR Isnull(LevelId_id,0)<>isnull(LevelIdTarget,0)
	 OR Superior<>SuperiorTarget)
if 
	((@RoleId Not In (63,55,56,57,68,69,72,58) And @RoleIdTarget In (63,55,56,57) And @LevelIdTarget<>6
	And @Temporary = 0))

	Or 
	(@Type=1 And @RoleId=@RoleIdTarget And Isnull(@LevelId,1)<>Isnull(@LevelIdTarget,0) And @Superior=@SuperiorTarget)
	Begin
		Select '' Education,'' Educator,'' Evaluation,'' PmChange ,'' ITChange ,''RequestGap
		,'' ReEvaluation ,'' Assessor2,'' EducatorName,''  AssessorName ,'' Assessor2Name,'' Assessor, Convert(bit,0) As Confirm
	
	
	End Else 

	Begin
If
	@Test=0 
Begin

----اگر جدید باشدو سمت تغییر کند
	if ((@Type = 1 And ( (@RoleId<>@RoleIdTarget  
---اگر سمت های بالاتر تولید باشد سطح آن نیمتواند بالا باشد
	And @RoleId Not In (63,55,56,57) And @RoleIdTarget In (63,55,56,57) And @LevelIdTarget=6)
	Or (@RoleId<>@RoleIdTarget  
	And @RoleId In (63,55,56,57) And @RoleIdTarget  In (63,55,56,57) )
	Or (@RoleId<>@RoleIdTarget  
	And @RoleId Not In (63,55,56,57) And @RoleIdTarget Not In (63,55,56,57) )
	Or (@RoleId<>@RoleIdTarget  
	And @RoleId  In (63,55,56,57) And @RoleIdTarget Not In (63,55,56,57) )
-----اگر سمت یکی است و سطح فرق میکند در حالتی که جدید است نمیتواند سطح از یکی بالاتر برود
	Or (@RoleId=@RoleIdTarget And @TeamCode NOt IN (Select TeamCode
	From UserTeamRole U
	Where username in (Select UserName From UserTeamRole WHere Id=@InfoID ))
	 And Isnull(@LevelId,1)-Isnull(@LevelIdTarget,0) BetWeen 0 And 1 )
	)) 
	Or @Type = 0 
		)
	And ( (SELECT [dbo].[HR_Name_GetTeamManager](@RoleIdTarget,@TeamCode,'U')) is NOt NUll)
	
	Or @Temporary = 1

	Begin
-----اگر سمت شخص در تیم های عملیاتی نباشد یا از تیم عملیاتی به غیر عملیاتی و برعکس انجام شود
		If 		('TechnicalRole' Not in (Select RoleGroup From HR_RoleGroup
				Where RoleID_id=@RoleIdTarget)
				OR 
				'TechnicalRole' Not in
				(Select RoleGroup From HR_RoleGroup
				Where RoleID_id=@RoleId))
				Or(@RoleId=@RoleIdTarget And Isnull(@LevelId,0)=Isnull(@LevelIdTarget,0)
				And @Superior=@SuperiorTarget And @TeamCode<>@TeamCodeOld)
				Or @Type=1
				Or @Temporary = 1
				--Or (@TeamCode<>@TeamCodeOld And (@RoleId=@RoleIdTarget And
				--  Isnull(@LevelId,0)-Isnull(@LevelIdTarget,0)=0 
				----Isnull(@LevelId,0)=isnull(@LevelIdTarget,0)
				--	 And @Superior=@SuperiorTarget))
			Begin
				 ;With CTE_User AS (  
				Select Distinct 
				Case When --(  @TeamCode=@TeamCodeOld ) Or
				 ( @RoleId=@RoleIdTarget) 
				Or (@Temporary = 1)
				Then '' 
				When @RoleIdTarget IN(69,72,63,57,56,58,68,55)
				And @RoleId Not IN (69,72,63,57,56,58,68,55)
				Then 'زهرا معيني امجد'
				When( (@RoleIdTarget=52 And  @RoleId IN (69,72,63,57,56,58,68,55)
				OR @RoleId=52 And @RoleIdTarget IN(69,72,63,57,56,58,68,55))
				And @RoleId<>@RoleIdTarget)
				Then  'زهرا معيني امجد' 
				Else
				(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'N'))
				--'زهرا معيني امجد'
				End EducatorName   
				,Case When
				--(  @TeamCode=@TeamCodeOld ) Or 
				( @RoleId=@RoleIdTarget) 
				Or (@Temporary = 1)
				Then '' 
				When @RoleIdTarget IN(69,72,63,57,56,58,68,55)
				And @RoleId Not IN (69,72,63,57,56,58,68,55)
				Then 'z.moeini@eit' 
				When( (@RoleIdTarget=52 And  @RoleId IN (69,72,63,57,56,58,68,55)
				OR @RoleId=52 And @RoleIdTarget IN(69,72,63,57,56,58,68,55))
				And @RoleId<>@RoleIdTarget)
				Then 'z.moeini@eit' 
				Else
				(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U'))
				--'z.moeini@eit' 
				End Educator  
				,Case When  (@Temporary=1 )
				Or (@RoleId=@RoleIdTarget And @RoleIdTarget IN (69,72))
				Then 
				Convert(Bit,0)
				ELse
				Convert(Bit,1) End  Evaluation  
				,Convert(Bit,1) PmChange  
				,Convert(Bit,1) ITChange  
				,'' RequestGap  
				,Case When  
				---یا موقت باشد
				(@Temporary=1)
				---یا ارشد بشود
				OR (@SuperiorTarget=1 And @Superior=0) 
				---یا پشتیبان و تستر ارتقا سطح داشته باشند
				Or (@RoleId=@RoleIdTarget And @RoleIdTarget IN (69,72))
				Then CONVERT(bit,0) 
				Else CONVERT(bit,1)  End
				ReEvaluation
				,Case When 
				--(  @TeamCode=@TeamCodeOld ) Or
				( @RoleId=@RoleIdTarget) 
				Or (@Temporary = 1)
				Then Convert(bit,0) Else
				Convert(bit,1) End
				Education  
				
				,Case When  
				(@Temporary=1 OR (@SuperiorTarget=1 And @Superior=0)) Then ''
				When @RoleIdTarget  IN (57,58) And @Type=1 Then
				 (Select FirstName + ' ' + LastName From UserTeamRole UT
				 Inner JOIn Users U3
				 On UT.UserName=U3.UserName
				 Where RoleId=111)
				  When @RoleId=@RoleIdTarget And @RoleIdTarget IN (69,72)
				 Then ''
				 When   @RoleIdTarget  IN (63,55,56,68)And @Type=1 Then
				 (Select FirstName + ' ' + LastName From UserTeamRole UT
				 Inner JOIn Users U2
				 On UT.UserName=U2.UserName
				 Where RoleId=108)
				Else (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'N')) End
				Assessor2Name  
				,Case When  (@Temporary=1 OR (@SuperiorTarget=1 And @Superior=0))  Then ''  
				When @RoleIdTarget  IN (57,58)And @Type=1 Then
				 (Select UT.UserName From UserTeamRole UT
				 Where RoleId=111)
				 When @RoleId=@RoleIdTarget And @RoleIdTarget IN (69,72)
				 Then ''
				 When   @RoleIdTarget  IN (63,55,56,68)And @Type=1 Then
				 (Select UT.UserName From UserTeamRole UT
				  Where RoleId=108)
					Else (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U')) End
					Assessor2 
				,Case When  @Temporary=1 Then ''   
				When @RoleIdTarget  IN (57,58)And @Type=1 Then
				 (Select FirstName + ' ' + LastName From UserTeamRole UT
				 Inner JOIn Users U3
				 On UT.UserName=U3.UserName
				 Where RoleId=111)
				  When @RoleId=@RoleIdTarget And @RoleIdTarget IN (69,72)
				 Then ''
				 When   @RoleIdTarget  IN (63,55,56,68)And @Type=1 Then
				 (Select FirstName + ' ' + LastName From UserTeamRole UT
				 Inner JOIn Users U2
				 On UT.UserName=U2.UserName
				 Where RoleId=108)
				Else 	(Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'N')) End
				AssessorName
				,Case When  @Temporary=1 Then ''  
				When @RoleIdTarget  IN (57,58) And @Type=1 Then
				 (Select UT.UserName From UserTeamRole UT
				 Where RoleId=111)
				 When @RoleId=@RoleIdTarget And @RoleIdTarget IN (69,72)
				 Then ''
				 When   @RoleIdTarget  IN (63,55,56,68)And @Type=1 Then
				(Select UT.UserName From UserTeamRole UT
				Where RoleId=108)
				Else (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U')) End
				Assessor 
				From UserTeamRole TR  
				Where TR.TeamCode=@TeamCode )

				Select *  ,(Case When COUNT(*) over()=0 Then  Convert(bit,0) Else Convert(bit,1) End ) As Confirm
				From CTE_User

			End
			ELse	
			Begin
				-----اگر فرد در تیم های عملیاتی جا به جا شود  
				 ;With CTE_User AS (  
				 Select  
				 ----اگر شخص تغییر تیم یا سطح داشته باشد به آموزش احتیاجی ندارد
				 Case When @RoleId=@RoleIdTarget And @Superior=@SuperiorTarget
				 Then CONVERT(Bit,0) ELse 
				 Education  End Education
				 ----اگر ارشد اموزش دهنده باشد و در تیم سمت ارشد وجود داشته باشد
				,Case When Educator='Superior' 
				 And (Select Count(*)
				 From UserTeamRole Where RoleId=@RoleIdTarget And Superior=1 And TeamCode=@TeamCode)>0
				 Then   
				 (Select Top (1)UserName From UserTeamRole Where RoleId=@RoleIdTarget And Superior=1 And TeamCode=@TeamCode)
				 When  Educator='Superior'  And ----ارشد در آن تیم وجود نداشته باشد
				 (Select Count(*)
				 From UserTeamRole Where RoleId=@RoleIdTarget And Superior=1 And TeamCode=@TeamCode)=0
				 Then 
				 (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U'))
				 ----اگر مسئول آموزش مدیر مسئول باشد و وجود داشته باشد
				 When Educator=58 And
				 (Select Count(*) From UserTeamRole Where RoleId=58 And Superior=1 And TeamCode=@TeamCode) >0
				 Then   
				 (Select Top (1)UserName From UserTeamRole Where RoleId=58 And Superior=1 And TeamCode=@TeamCode) 
				 ----اگر مسئول آموزش مدیر محصول باشد و وجود نداشته باشد
				 When Educator=58 And
				 (Select Count(*) From UserTeamRole Where RoleId=58 And Superior=1 And TeamCode=@TeamCode)=0
				 Then   
				  (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U'))
				 ELse (Select UserName From UserTeamRole Where RoleId=Educator) End As Educator 
				 ,CR.Evaluation  
				 ,Case When Assessor='Superior'  And 
				 (Select Count(*)
				 From UserTeamRole Where RoleId=RoleIdTarget_id And Superior=1 And TeamCode=@TeamCode)>0
					Then 
				 (Select Top(1) UserName
				 From UserTeamRole Where RoleId=RoleIdTarget_id And Superior=1 And TeamCode=@TeamCode) 
				  When Assessor='Superior'  And 
				  ----ارشد در آن تیم وجود نداشته باشد
				 (Select Count(*)
				 From UserTeamRole Where RoleId=RoleIdTarget_id And Superior=1 And TeamCode=@TeamCode)=0
				 Then 
				 (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U'))
				 When Assessor=58 Then   
				 (Select Top (1)UserName From UserTeamRole Where RoleId=58 And Superior=1 And TeamCode=@TeamCode) 
				 When Assessor=63 Then
				  (Select Top (1)UserName From UserTeamRole Where RoleId=63 And Superior=1 And TeamCode=@TeamCode)  
				 ELse (Select UserName From UserTeamRole Where RoleId=Assessor) End As Assessor 
				 ,Case When @TeamCode<>@TeamCodeOld Then Convert(bit,1) Else   CR.PmChange  End PmChange
				,Case When @TeamCode<>@TeamCodeOld Then Convert(bit,1) Else  CR.ITChange  End ITChange
				 ,CR.RequestGap  
				 ,CR.ReEvaluation  
				 ,Case When Assessor='Superior'  And 
				 (Select Count(*)
				 From UserTeamRole Where RoleId=RoleIdTarget_id And Superior=1 And TeamCode=@TeamCode)>0
					Then 
				 (Select Top(1) UserName
				 From UserTeamRole Where RoleId=RoleIdTarget_id And Superior=1 And TeamCode=@TeamCode) 
				  When Assessor='Superior'  And 
				  ----ارشد در آن تیم وجود نداشته باشد
				 (Select Count(*)
				 From UserTeamRole Where RoleId=RoleIdTarget_id And Superior=1 And TeamCode=@TeamCode)=0
				 Then 
				 (Select dbo.HR_Name_GetTeamManager(@RoleIdTarget,@TeamCode,'U'))
				 When Assessor=58 Then   
				 (Select Top (1)UserName From UserTeamRole Where RoleId=58 And Superior=1 And TeamCode=@TeamCode) 
				 When Assessor=63 Then
				  (Select Top (1)UserName From UserTeamRole Where RoleId=63 And Superior=1 And TeamCode=@TeamCode)  
				 ELse (Select UserName From UserTeamRole Where RoleId=Assessor) End As Assessor2  
				 From HR_ChangeRole CR  
				 Where RoleID_id=@RoleId  
				 And RoleIdTarget_id=@RoleIdTarget  
				 And Isnull(LevelId_id,0)=Isnull(@LevelId,0)  
				 And Isnull(LevelIdTarget_id,0)=Isnull(@LevelIdTarget,0)  
				 And Superior=@Superior  
				 And SuperiorTarget=@SuperiorTarget)  
				Select Education,Educator,Evaluation,PmChange,ITChange,RequestGap
				,ReEvaluation,Case When ReEvaluation = 1 Then IsNull(Assessor2,Assessor) Else Assessor2 End Assessor2
				 ,(select FirstName+ ' ' +LastName From Users u where u.UserName=Educator) EducatorName  
				 ,(select FirstName+ ' ' +LastName From Users u where u.UserName=Assessor) AssessorName  
				 ,Case When ReEvaluation = 1 Then 
				 (Select FirstName+ ' ' +LastName From Users u where u.UserName= IsNull(Assessor2,Assessor))
				Else NULL End Assessor2Name, Assessor
				 ,(Case When (Select COUNT(*) From CTE_User)=0 Then  Convert(bit,0) Else Convert(bit,1) End ) As Confirm
				From CTE_User  
				Union 
				Select '' Education,'' Educator,'' Evaluation,'' PmChange ,'' ITChange ,''RequestGap
				,'' ReEvaluation ,'' Assessor2,'' EducatorName,''  AssessorName ,'' Assessor2Name ,'' Assessor, Convert(bit,0) As Confirm
				Where (Select COUNT(*) From CTE_User)=0
			End
		End Else 
		Begin
			Select '' Education,'' Educator,'' Evaluation,'' PmChange ,'' ITChange ,''RequestGap
			,'' ReEvaluation ,'' Assessor2,'' EducatorName,''  AssessorName ,'' Assessor2Name,'' Assessor , Convert(bit,0) As Confirm
		End  
	End Else 
	Begin
		Select '' Education,'' Educator,'' Evaluation,'' PmChange ,'' ITChange ,''RequestGap
		,'' ReEvaluation ,'' Assessor2,'' EducatorName,''  AssessorName ,'' Assessor2Name,'' Assessor, Convert(bit,0) As Confirm
	End  
 End 
End
End
  
  
  
