// newRoleRequest.js
(function($){

    // ====== ابزارهای کمکی ======
    function darkenColor(color, amount) {
      const [r,g,b] = color.match(/\d+/g).map(Number);
      return `rgb(${Math.max(0,r-amount)},${Math.max(0,g-amount)},${Math.max(0,b-amount)})`;
    }
    function isLightColor(color) {
      const [r,g,b] = color.match(/\d+/g).map(Number);
      return (0.2126*r + 0.7152*g + 0.0722*b) > 128;
    }
  
    function checkDuplicate(selector, attr, val, label) {
      const dup = $(selector).children().filter((_,el) => $(el).attr(attr)===val).length>0;
      if(dup){
        $.confirm({
          title: `❌ خطا در اضافه کردن ${label}`,
          content: `شما نمیتوانید ${label} تکراری اضافه کنید.`,
          type:"red", theme:"modern", columnClass:"medium", boxWidth:"400px",
          useBootstrap:false,
          buttons:{ ok:{ text:"باشه", btnClass:"btn-red" } }
        });
      }
      return dup;
    }
  
    function createHeader(teamCode, teamName) {
      const url = window.STATIC_URL + 'roleManager/images/TeamIcon/' + teamCode + '.png';
      return $('<th>').attr('teamCode',teamCode).append(`
        <div class="teamContainer">
          <div class="teamInfo">
            <img src="${url}" alt="Team" style="width:50px">
            <p id="teamName">${teamName}</p>
          </div>
          <div class="teamFunctions">
            <div>
              <p class="deleteAllText">حذف همه</p>
              <img id="deleteTeam" class="icon" teamCode="${teamCode}"
                   src="${window.STATIC_URL}roleManager/images/Icons/deleteAll_Icon.png" alt="">
            </div>
            <div>
              <p class="showAllText">نمایش همه</p>
              <img id="plusRole_forTeam" class="icon" teamCode="${teamCode}"
                   src="${window.STATIC_URL}roleManager/images/Icons/showAll_Ico.png" alt="">
            </div>
          </div>
        </div>`);
    }
  
    function createRow(roleID, roleName) {
      return $(`<tr roleID="${roleID}"><td>
        <div class="roleContainer">
          <div class="deleteContainer">
            <p class="deleteAllText">حذف همه</p>
            <img id="deleteRole" class="icon" roleID="${roleID}"
                 src="${window.STATIC_URL}roleManager/images/Icons/deleteAll_Icon.png" alt="">
          </div>
          <div class="textContainer"><p id="roleID">${roleName}</p></div>
          <div class="showContainer">
            <p class="showAllText">نمایش همه</p>
            <img id="plusTeam_forRole" class="icon" roleID="${roleID}"
                 src="${window.STATIC_URL}roleManager/images/Icons/showAll_Ico.png" alt="">
          </div>
        </div>
      </td></tr>`);
    }
  
    function createAllowedCell(teamCode, roleId, finder) {
      const td = $('<td>').attr('teamCode',teamCode);
      if(!finder) return td;
  
      const bg = finder.AllowedRoleCount===0 ? '#AEAEAE69' : '#6B92E7CC';
      const parent = $('<div id="allowedParent">').css('background-color',bg);
  
      function makeItem(label, val, icon, editable, extra={}) {
        const cont = $('<div class="itemContainer">');
        cont.append($('<div>').append($('<p>').text(label)));
        cont.append($(`<img class="allowedParentIcon" src="${window.STATIC_URL}roleManager/images/Icons/${icon}.png">`));
        const inp = $('<input class="allowedParentInput">')
          .attr({type:'number', value:val, ...extra, readonly:!editable});
        cont.append(inp);
        if(editable){
          cont.append($(`<img id="editIcon" src="${window.STATIC_URL}roleManager/images/Icons/editIcon.png">`));
        }
        return cont;
      }
  
      const up   = makeItem('ظرفیت کل', finder.AllowedRoleCount, 'blueUserIcon', true, {prevValue:finder.AllowedRoleCount,modified:false,teamCode,roleId,min:0,max:100});
      const mid  = makeItem('نفرات فعلی', finder.EntryCount, 'yellowUserIcon', false);
      const lowV = Math.max(0, finder.AllowedRoleCount - finder.EntryCount);
      const low  = makeItem('ظرفیت باقی‌مانده', lowV, 'greenUserIcon', false);
  
      parent.append(up, mid, low);
      return td.append(parent);
    }
  
    // ====== بایند کردن رویدادها ======
    function bindForm() {
      $('#roleRequestForm').on('submit', e=>e.preventDefault());
      $('#submitBtn').on('click', ()=>{
        const data = [];
        $("input[modified='true']").each(function(){
          const $t = $(this), tc=$t.attr('teamCode'), rid=$t.attr('roleId');
          const val=$t.val(), prev=$t.attr('prevValue');
          let team = data.find(x=>x.TeamCode===tc);
          if(!team) data.push(team={TeamCode:tc,Roles:[]});
          team.Roles.push({RoleId:rid,RoleCount:val,PrevRoleCount:prev});
        });
  
        $.ajax({
          url: window.location.href,
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify(data),
          headers: {
            "X-CSRFToken": $("meta[name='csrf_holder']").attr("content"),
            "Content-Type": "application/json"
          },
          beforeSend: ()=>$.LoadingOverlay("show"),
          complete: ()=>$.LoadingOverlay("hide"),
          success: resp => {
            $.confirm({
              title: resp.Error?"❌ خطا":"✅ موفقیت",
              content: resp.Message,
              type: resp.Error?"red":"green", theme:"modern",
              columnClass:"medium", boxWidth:"400px", useBootstrap:false,
              buttons:{ ok:{ text:"باشه", btnClass:resp.Error?"btn-red":"btn-green", action:()=>window.location.reload() } }
            });
          },
          error: ()=> {
            $.confirm({
              title:"❌ خطا در ارتباط",
              content:"خطایی در ارتباط با سرور رخ داده است.",
              type:"red", theme:"modern",
              columnClass:"medium", boxWidth:"400px", useBootstrap:false,
              buttons:{ ok:{ text:"باشه", btnClass:"btn-red" } }
            });
          }
        });
      });
    }
  
    function bindInputs() {
      $(document).on('input','#allowedParent input',function(){
        const $this=$(this);
        const prev=+($this.attr('prevValue'))||0;
        const val = +($this.val())||0;
        $this.attr('modified', val!==prev);
        const par=$this.closest('#allowedParent');
        const col= val!==prev ? '#4E9F3D' : (prev===0?'#c3cbd9':'#6EACDA');
        par.css('background-color',col).data('bgColor',col);
        $this.css('background-color', val!==prev?'#348144':(prev===0?'#bfbfbf':'#9EDDFF'));
        $this.css('color', isLightColor($this.css('background-color'))?'black':'white');
        checkModified();
      });
    }
  
    function bindDeletes() {
      $(document).on('click','#deleteTeam',function(){
        const tc=$(this).attr('teamCode');
        $(`th[teamCode="${tc}"],td[teamCode="${tc}"]`).fadeOut(500,function(){ $(this).remove(); });
        const name=$(`th[teamCode="${tc}"] p#teamName`).text();
        const item=$('<div>').addClass('team-item').attr('teamCode',tc).text(name).hide();
        $('#teamList .items-list').prepend(item).fadeIn();
      });
      $(document).on('click','#deleteRole',function(){
        const rid=$(this).attr('roleID');
        const name=$(`tr[roleID="${rid}"] p#roleID`).text();
        const item=$('<div>').addClass('role-item').attr('roleID',rid).text(name).hide();
        $(`tr[roleID="${rid}"]`).remove();
        $('#roleList .items-list').prepend(item).fadeIn();
      });
    }
  
    function bindAdds() {
      $(document).on('click','.team-item',function(){
        const tc=$(this).attr('teamCode'), nm=$(this).text();
        const hdr=createHeader(tc,nm);
        if(!checkDuplicate('#table_header','teamCode',tc,'تیم')){
          $('#table_header').children().length && $('#tbody tr').each((_,tr)=>{
            const rid=$(tr).attr('roleID');
            const f=window.ALLOWED_TEAM.find(x=>x.TeamCode===tc&&x.RoleId==rid);
            $(tr).append(createAllowedCell(tc,rid,f));
          });
          hdr.hide().insertBefore('#teamBtn').fadeIn(500);
          $(this).slideUp(1000,()=>$(this).remove());
        }
      });
      $(document).on('click','.role-item',function(){
        const rid=$(this).attr('roleID'), nm=$(this).text();
        const row=createRow(rid,nm);
        if(!checkDuplicate('#tbody','roleID',rid,'سمت')){
          $('#table_header th').length>2 && $('#table_header th:gt(0)').each((_,th)=>{
            const tc=$(th).attr('teamCode');
            const f=window.ALLOWED_TEAM.find(x=>x.TeamCode===tc&&x.RoleId==rid);
            row.append(createAllowedCell(tc,rid,f));
          });
          row.hide().insertBefore('#roleBtn').fadeIn(500);
          $(this).slideUp(1000,()=>$(this).remove());
        }
      });
    }
  
    function bindToggles() {
      $('#teamPlusButton').on('click',()=>$('#teamList').slideToggle('slow'));
      $('#rolePlusButton').on('click',()=>$('#roleList').slideToggle('slow'));
      const search=(inSel,itemSel)=>{
        $(inSel).on('input',function(){
          const term=$(this).val().trim().toLowerCase().replace(/\s+/g,'');
          let any=false;
          $(itemSel).each(function(){
            const t=$(this).text().toLowerCase().replace(/\s+/g,'');
            $(this)[t.includes(term)?'show':'hide']();
            any=any||t.includes(term);
          });
          $('.no-results').toggle(!any);
        });
      };
      search('#teamSearchInput','#teamList .team-item');
      search('#roleSearchInput','#roleList .role-item');
    }
  
    // همه چیز رو راه‌اندازی کن
    $(function(){
      bindForm();
      bindInputs();
      bindDeletes();
      bindAdds();
      bindToggles();
    });
  
  })(jQuery);
  