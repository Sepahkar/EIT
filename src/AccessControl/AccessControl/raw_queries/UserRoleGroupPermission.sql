SELECT OwnerPermissionUser, PermissionCode
FROM AccessControl_userrolegrouppermission
WHERE OwnerPermissionUser = %s AND
      PermissionCode = %s