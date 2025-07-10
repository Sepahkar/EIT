CREATE PROCEDURE [dbo].[HR_GetTargetRole] 

	@ID int,
	@Type bit =0


AS
BEGIN


	if @Type = 0
		Begin
			Select Distinct  RoleId,RoleName,HasLevel,HasSuperior 
			From Role
			Where RoleId Not in (
			Select RG2.RoleID_id
			From  HR_RoleGroupTargetException RTE
			Inner JOin HR_RoleGroup RG
			On RTE.RoleGroup=RG.RoleGroup
			Inner JOin HR_RoleGroup RG2
			On RTE.RoleGroupTarget=RG2.RoleGroup
			Inner JOin UserTeamRole UTR
			On UTR.RoleId=RG.RoleID_id
			Where UTR.ID=@id And RoleId<>127)
		End
		Else 
		Begin
			--Select Distinct RoleId,RoleName,HasLevel,HasSuperior 
			--From Role R
			--Inner Join HR_RoleGroup HG
			--On HG.RoleID_id=R.RoleId
			--Where RoleId<>127 And
			--HG.RoleGroup IN(
			--Select RoleGroup From Role R
			--Inner Join HR_RoleGroup HG
			--On HG.RoleID_id=R.RoleId
			--Where RoleId in (
			--Select  RoleId From UserTeamRole
			--Where UserName In
			--(Select UserName From UserTeamRole
			--WHere ID=@id)))
			Select Distinct  RoleId,RoleName,HasLevel,HasSuperior 
			From Role
			Where RoleId Not in (
			Select RG2.RoleID_id
			From  HR_RoleGroupTargetException RTE
			Inner JOin HR_RoleGroup RG
			On RTE.RoleGroup=RG.RoleGroup
			Inner JOin HR_RoleGroup RG2
			On RTE.RoleGroupTarget=RG2.RoleGroup
			Inner JOin UserTeamRole UTR
			On UTR.RoleId=RG.RoleID_id
			Where UTR.ID=@id And RoleId<>127)

		End

End


