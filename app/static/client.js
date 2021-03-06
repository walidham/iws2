
function Client(data) {
    this.id = ko.observable(data.id);
    this.company_name = ko.observable(data.company_name);
    this.last_name = ko.observable(data.last_name);
    this.first_name = ko.observable(data.first_name);
    this.priority = ko.observable(data.priority);
    this.email = ko.observable(data.email);
    this.description = ko.observable(data.description);
    
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

function ClientListViewModel() {
    var self = this;
    self.clients = ko.observableArray([]);
    self.newClientCN = ko.observable();
    self.newLastName = ko.observable();
    self.newFirstName = ko.observable();
    self.newClientEmail = ko.observable();
    self.newPriority = ko.observable();
    self.newPassword = ko.observable();
    self.newConfPassword = ko.observable();
    self.error_save=0;
    self.addClient = function() {
	   
		self.save();
		if(self.error_save==0){
			self.newClientCN("");
			self.newLastName("");
			self.newFirstName("");
			self.newClientEmail("");
			self.newPassword("");
			self.newConfPassword("");
		}
       	    
    };

    $.getJSON('/clients_list', function(clientModels) {
	var t = $.map(clientModels.clients, function(item) {
		
	    return new Client(item);
	});
	
	self.clients(t);
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
	    url: '/new_client',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'company_name': self.newClientCN(),
		'email': self.newClientEmail(),
		
		'first_name': self.newFirstName(),
		'last_name': self.newLastName(),
		'password': self.newPassword()
	    }),
	    success: function(data) {
	    	if(data.result=="OK"){
			console.log("Pushing to clients array");
			self.clients.push(new Client(data));
			$('#new_client').modal('hide')
			return;
		}else{
			$('#new_client').modal('hide')
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

ko.applyBindings(new ClientListViewModel());
