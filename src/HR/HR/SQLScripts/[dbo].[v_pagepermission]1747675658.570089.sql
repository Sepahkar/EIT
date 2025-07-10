CREATE VIEW [dbo].[V_PagePermission]
AS
SELECT        u.username AS username_id,
mu.NationalCode,
P.id, P.GroupId, P.Editable, P.Page_id,i.OrderNumber
FROM            dbo.auth_group AS g INNER JOIN
                         dbo.auth2_user_groups AS ug ON ug.group_id = g.id INNER JOIN
                         dbo.auth2_user AS u ON u.national_code = ug.user_id INNER JOIN
                         dbo.HR_pagepermission AS P ON P.GroupId = g.id
						 Inner Join HR_pageinformation i on i.id=p.Page_id
						inner join Users mU on mu.NationalCode = u.national_code 
