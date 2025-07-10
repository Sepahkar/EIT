Create PROCEDURE [dbo].[HR_GetChoiceAssessorsAndEducators]   

  @TeamCode CHar(3)----اگر تیم جدید داشت جدید اگر نه قبلی  
  ,@InfoID Int  
 , @RoleIdTarget int----اگر سمت جدید داشت جدید اگر نه قبلی  
 , @LevelIdTarget int----اگر سطح جدید داشت جدید اگر نه قبلی  
 , @SuperiorTarget Bit----اگر ارشدیت جدید داشت جدید اگر نه قبلی  
 , @Temporary Bit=0 -----اگر 1 باشد موقت اگر 0 باشد دائمی است
 ,	@Type bit =0--اگر تایپ 0 بود یعنی تغییر اگر 1 بود یعنی جدید
AS  
BEGIN  
 
	Select 'z.moeini@eit' UserName , 'زهرا معيني امجد' FullName
	Union 
	Select H.UserName,U.FirstName+ ' ' + U.LastName FullName
	From UserTeamRole H
	Inner Join Users U 
	On U.UserName=H.UserName
	Where H.TeamCode = @TeamCode
	And H.UserName <>(Select HR.UserName
	From UserTeamRole HR
	Where HR.ID=@InfoID)
End
