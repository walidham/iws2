
function User(data) {
    this.id = ko.observable(data.id);
    
    this.last_name = ko.observable(data.last_name);
    this.first_name = ko.observable(data.first_name);
    
    this.email = ko.observable(data.email);
    
    
}

function validatePassword(p) {
    var errors = [];
    var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$");
    
    if (strongRegex.test(p)) {
        errors.push("Invalid password."); 
    }
    
    if (errors.length > 0) {
        alert(errors.join("\n"));
        return false;
    }
    return true;
}

function UserListViewModel() {
    var self = this;
    self.users = ko.observableArray([]);

    self.newLastName = ko.observable();
    self.newFirstName = ko.observable();
    self.newUserEmail = ko.observable();

    self.newPassword = ko.observable();
    self.newConfPassword = ko.observable();
    self.error_save=0;
    self.addUser = function() {
	   
		self.save();
		if(self.error_save==0){
			self.newLastName("");
			self.newFirstName("");
			self.newUserEmail("");
			self.newPassword("");
			self.newConfPassword("");
		}
       	    
    };

    $.getJSON('/users_list', function(userModels) {
	var t = $.map(userModels.users, function(item) {
		
	    return new User(item);
	});
	
	self.users(t);
    });

    self.save = function() {
        var pass = $('#passwordText').val();
        var passConf = $('#confPasswordText').val();
        
        if(pass!=passConf){
        	alert("Password is not identical to confirmation");
        	self.error_save=1;
        	return;
        }
        if(!validatePassword(pass)){
       		self.error_save=1;
        	return;
        }
        
        self.error_save=0;
	return $.ajax({
	    url: '/new_user',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({

		'email': self.newUserEmail(),
		
		'first_name': self.newFirstName(),
		'last_name': self.newLastName(),
		'password': self.newPassword()
	    }),
	    success: function(data) {
	    	if(data.result=="OK"){
			console.log("Pushing to users array");
			self.users.push(new User(data));
			$('#new_user').modal('hide')
			return;
		}else{
			$('#new_user').modal('hide')
			alert(data.msg);
			return;
		}
	    },
	    error: function(e) {
		return console.log("Failed"+e);
	    }
	});
    };
}

ko.applyBindings(new UserListViewModel());
