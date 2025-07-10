jQuery(function($){

});

function initXData(){

    return {
        'showLoading':false,
        'ALL_APPS': ALL_APPS,
        'searchValue':'',
        'selectedApp':'',
        'selectedUser':{
            'UserName':'',
            'FullName':'',
            'user_image_name':'',
            'age':'',
            'contract':'',
            'degree':'',
        },
        'accessDataUser':{
            'username':'',
            'is_active':false,
            'is_staff':false,
            'is_superuser':false,
        },
        'allUsers':[],
        'users':[],
        init(){
            this.showLoading=true;
            fetch('http://192.168.20.81:14000/HR/api/all-users/')
                .then(response=> {
                    return response.json();
                })
                .then(data => {
                    this.allUsers = data['data'];
                    this.users = this.allUsers;
                    this.showLoading=false;
                })
                .catch(error => {
                    this.showLoading=false;
                })
        },
        changeApp(event){
            this.selectedApp = event.target.value;
        },
        searchInTable(event){
            if(event.target.value.length <1)
                return;
            let newUsers = [];
            this.allUsers.filter( item =>{
                if(item.UserName.indexOf(event.target.value) > -1 || item.FullName.indexOf(event.target.value) > -1)
                    newUsers.push(item);
            });
            this.users = newUsers;
        },
        setUserToSelectedUser(username){
                var url = window.location.href;
                var curr_app = url.split("admin/")[1].split("/")[0];
                fetch('/'+curr_app+"/api/user/get-internal-token/")
                    .then( response => {return response.json()})
                    .then(data => {
                        if(data.state == "ok"){
                            var token = data.token;
                            if(this.selectedApp != "0"){
                                var url = this.search_in_all_apps(this.selectedApp,'APPSCHEMA') + this.search_in_all_apps(this.selectedApp,'APPIP') + ":" + this.search_in_all_apps(this.selectedApp,'APPPORT');
                                var formData = new FormData();
                                formData.append('token',token);
                                fetch(url+'/'+this.selectedApp+'/api/user/access/'+username+'/',{
                                    method:'POST',
                                    body: formData,
                                    headers: {
                                        'X-CSRFToken':this.getCSRFToken(),
                                    }})
                                .then(response => {return response.json()})
                                .then(data => {
                                    this.accessDataUser = data['data'];
                                    this.allUsers.forEach((item)=>{
                                        if(item.UserName.indexOf(username)>-1){
                                            this.selectedUser = item;
                                            this.selectedUser.user_image_name = "/media_hr/HR/PersonalPhoto/" + this.selectedUser.user_image_name;
                                            return;
                                        }
                                    });
                                })
                                .catch(error => {
                                    console.log("error",error)
                                })
                            }
                        }
                    }).catch(error => {
                        console.log(error)
                    })
        },
        changeUserAccessData(){
                var url = window.location.href;
                var curr_app = url.split("admin/")[1].split("/")[0];
                fetch('/'+curr_app+"/api/user/get-internal-token/")
                .then( response => {return response.json()})
                .then(data => {
                    if(data.state == "ok"){
                        var token = data.token;
                        if(this.accessDataUser.username != '' && this.selectedApp != ''){
                            var url = this.search_in_all_apps(this.selectedApp,'APPSCHEMA') + this.search_in_all_apps(this.selectedApp,'APPIP') + ":" + this.search_in_all_apps(this.selectedApp,'APPPORT');
                            var newData = this.accessDataUser;
                            var formData = new FormData();
                            formData.append('token',token);
                            formData.append('is_active',(this.accessDataUser.is_active==true) ? 1 : 0);
                            formData.append('is_staff',(this.accessDataUser.is_staff==true) ? 1 : 0);
                            formData.append('is_superuser',(this.accessDataUser.is_superuser==true) ? 1 : 0);
                            fetch(url+'/'+this.selectedApp+'/api/user/set-access/'+this.accessDataUser.username+'/',{
                                    method:'POST',
                                    body: formData,
                                    headers: {
                                        'X-CSRFToken':this.getCSRFToken(),
                                    },
                             })
                            .then( response => {return response.json()})
                            .then(data=>{
                                if(data.data.state == "ok"){
                                    this.accessDataUser = newData;
                                    alert("انجام شد");
                                }
                            }).catch(error => console.log("error",error));
                        }
                    }
                })
        },
        changeChecked(event,type){
            if(type=="superuser"){
                this.accessDataUser.is_superuser = event.target.checked;
            }
            else if(type=="superactiveuser"){
                this.accessDataUser.is_active = event.target.checked;
            }
            else if(type=="staff"){
                this.accessDataUser.is_staff = event.target.checked;
            }
            console.log(this.accessDataUser)
        },
        search_in_all_apps(appName,k){
            var finded = ''
            this.ALL_APPS.forEach(function(item){
                if(item['AppName'] == appName){
                    finded = item[k];
                }
            });
            return finded;
        },
        getCSRFToken() {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(10));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }
}