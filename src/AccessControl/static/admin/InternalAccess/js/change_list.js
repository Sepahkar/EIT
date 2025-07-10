jQuery(function($){

});

function initXData(){
    return {
        'showLoading':false,
        'searchValue':'',
        'selectedUser':{
            'full_name':'',
            'user_image_name':'',
            'age':'',
            'contract':'',
            'degree':'',
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
                    this.allUsers = data;
                    this.users = this.allUsers;
                    this.showLoading=false;
                })
                .catch(error => {
                    this.showLoading=false;
                })
        },
        searchInTable(event){
            if(event.target.value.length <1)
                return;
            let newUsers = [];
            this.allUsers.filter( item =>{
                if(item.username.indexOf(event.target.value) > -1 || item.full_name.indexOf(event.target.value) > -1)
                    newUsers.push(item);
            });
            this.users = newUsers;
        },
        setUserToSelectedUser(username){
            this.allUsers.forEach((item)=>{
                if(item.username.indexOf(username)>-1){
                    this.selectedUser = item;
                    this.selectedUser.user_image_name = "/media_hr/HR/PersonalPhoto/" + this.selectedUser.user_image_name;
                    return;
                }
            });
        },
    }
}