var old_global_priority =[]

function Client(data) {
    
    this.id = data.id;
    this.company_name = ko.observable(data.company_name);
    this.email = ko.observable(data.email);
    this.last_name = ko.observable(data.last_name);
    this.first_name = ko.observable(data.first_name);
}

function Product(data) {
    
    this.id = data.id;
    this.product_name = ko.observable(data.product_name);
    this.description = ko.observable(data.description);
}



function Feature(data,self) {
    this.id = ko.observable(data.id);
    this.title = ko.observable(data.title);
    this.target_date = ko.observable(data.target_date);
    this.description = ko.observable(data.description);
    this.ticket_url = ko.observable(data.ticket_url);
    this.client_priority = ko.observable(data.client_priority);
    this.global_priority = ko.observable(data.global_priority);
    this.client_id = ko.observable(data.client_id);
    this.product = ko.observable(GetProduct(data.product_id,self));
    this.client =  ko.observable(GetClient(data.client_id,self));
    this.company_name = ko.observable(this.client().company_name());
    
    this.product_id = ko.observable(this.product().id);
    
    this.product_name = ko.observable(GetProduct(data.product_id,self).product_name());
    
    this.target_date = ko.computed(function(){
    			   var target_date = new Date(data.target_date);
			   var year = target_date.getFullYear().toString();
			   var month = (target_date.getMonth() + 1).toString();
			   var day   = target_date.getDay().toString();
			   var pad = "00";

			   return month + '-' +
			    + day + '-' +
			     year;

			});
   
}

function save_priority(id,priority, global_priority){

    return $.ajax({
		    url: '/save_priorities',
		    contentType: 'application/json',
		    type: 'POST',
		    data: JSON.stringify({
			'id': ""+id,
			'priority': ""+priority,
			'global_priority': ""+global_priority
			
		    }),
		    success: function(data) {
			console.log("Save priorities");
			return;
			
		    },
		    error: function(e) {
			console.log("Failed"+e);
			return;
		    }
		});



}

function updateFeature(data){

    return $.ajax({
		    url: '/update_feature',
		    contentType: 'application/json',
		    type: 'POST',
		    data: JSON.stringify({
			'id': ""+data.id(),
			'title': ""+data.title(),
			'target_date': ""+data.target_date(),
			'ticket_url': ""+data.ticket_url(),
			'product_id': ""+data.product().id,

			
		    }),
		    success: function(data) {
			console.log("Save feature");
			return true;
			
		    },
		    error: function(e) {
			console.log("Failed"+e);
			return false;
		    }
		});



}

function delete_Feature(id){

    return $.ajax({
		    url: '/delete_feature',
		    contentType: 'application/json',
		    type: 'POST',
		    data: JSON.stringify({
			'id': ""+id,
			
		    }),
		    success: function(data) {
			console.log("Save feature");
			return true;
			
		    },
		    error: function(e) {
			console.log("Failed"+e);
			return false;
		    }
		});



}


Feature.prototype.clone = function() {

    var  data = {"id":this.id, "title":this.title(), "email":this.email(), "global_priority":this.global_priority(), 
                 "client_priority":this.client_priority(),
                 "description":this.description(),"client_name":this.client_name(),"client_id":this.client_id(),
                 "target_date":this.target_date(),"ticket_url":this.ticket_url()};
    return new Feature(data);
};


function GetClient(id,self){
    var client;

    ko.utils.arrayForEach(self.clients(), function(c) {
        if(c.id == id){
	    
            client= c;
	}
    });
  
    return client;
}

function GetProduct(id,self){
    var product;

    ko.utils.arrayForEach(self.products(), function(c) {
        if(c.id == id){
	    
            product= c;
	}
    });
  
    return product;
}

function FeatureListViewModel() {


    var self = this;
    self.clients = ko.observableArray([]);
    self.products = ko.observableArray([]);

    $.getJSON('/clients_list', function(clientModels) {
	var t = $.map(clientModels.clients, function(item) {
	    return new Client(item);
	});
	
	self.clients(t);
    });

    $.getJSON('/products_list', function(productsModels) {
	var t = $.map(productsModels.products, function(item) {
	    return new Product(item);
	});
	
	self.products(t);
    });

    self.features = ko.observableArray([]);

    self.newTitle = ko.observable();
    self.newDesc = ko.observable();
    self.newTargetDate = ko.observable();
    
    
    self.newTicketUrl = ko.observable();
    self.newClientPriority = ko.observable();
    self.newClient = ko.observable();
    self.newProduct = ko.observable();
    
    self.addFeature = function() {
	self.save();
	self.newTitle("");
	self.newDesc("");
        self.newTargetDate("");
	self.newTicketUrl("");
	self.newClientPriority("");
	self.newClient("");
	self.newProduct("");
    };

    
    
    $.getJSON('/features_list', function(featureModels) {
   
	var t = $.map(featureModels.features, function(item) {
	
	    return new Feature(item,self);
	});
	self.features(t);
	old_global_priority=[];
		//table of old global priorities
	    	ko.utils.arrayForEach(self.features(), function(c) {
		 	
	
			old_global_priority.push(c.global_priority());
		
			///////////:
	    	});
    });

    self.save = function() {
	var rol = $("#role_user").val();
	var client_id = "0";
	
	if(rol =="3")
		client_id = $("#current_user_id").val();
	else
		client_id = self.newClient().id;
		
		
	return $.ajax({
	    url: '/new_feature',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'title': self.newTitle(),
		'target_date': self.newTargetDate(),
		'ticket_url': self.newTicketUrl(),
		'client_id': client_id,
		
		'description': self.newDesc(),
		'product_id': self.newProduct().id
	    }),
	    success: function(data) {
		console.log("Pushing to feature array");
		self.features.push(new Feature(data,self));
		old_global_priority.push(data.global_priority);
		$('#new_feature').modal('hide')
		return;
	    },
	    error: function(e) {
		return console.log("Failed"+e);
	    }
	});
    };
    
    self.savePriorities = function() {
    	var priority = 0;
    	
    	var index = 0;
    	
    	
	 ko.utils.arrayForEach(self.features(), function(c) {
	 	priority = priority+1;
        	save_priority(c.id(),priority,old_global_priority[index]);
        	index++;
        	
    	});
    	
    	$.getJSON('/features_list', function(featureModels) {
   
		var t = $.map(featureModels.features, function(item) {
	
		    return new Feature(item,self);
		});
		self.features(t);
		old_global_priority=[];
		//table of old global priorities
	    	ko.utils.arrayForEach(self.features(), function(c) {
		 	
			old_global_priority.push(c.global_priority());
		
	    	});
	    });
	
    };
	// Set feature editable
	
	self.selected_fr=null;
	//Title
	self.selectedTitle = ko.observable();
	
	self.clearTitle = function(data, event) {
		if (data === self.selectedTitle()) {
			self.selectedTitle(null);
		}
		if (data.title() === "") {
 			alert("Title can't be empty");
			data.title(self.selected_fr.title());
			return;
		}
		self.update_Feature(data);
		
	};
	
	self.isTitleSelected = function(data) {
		self.selected_fr = data;
		return data === self.selectedTitle();
	};
	
	// Target date
	self.selectedTargetDate = ko.observable();
	
	self.clearTargetDate = function(data, event) {
		if (data === self.selectedTargetDate()) {
			self.selectedTargetDate(null);
		}
		if (data.target_date() === "") {
 			alert("Target Date can't be empty");
			data.target_date(self.selected_fr.target_date());
			return;
		}
		self.update_Feature(data);
		
	};
	
	self.isTargetDateSelected = function(data) {
		self.selected_fr = data;
		return data === self.selectedTargetDate();
	};
	
	// Product
	self.selectedProduct = ko.observable();
	
	self.clearProduct = function(data, event) {
		if (data === self.selectedProduct()) {
			self.selectedProduct(null);
		}
		data.product_name(data.product().product_name());
		self.update_Feature(data);
		
		
	};
	
	self.isProductSelected = function(data) {
		
		return data === self.selectedProduct();
	};
	//Ticket URL
	self.selectedTicketUrl = ko.observable();
	
	self.clearTicketUrl = function(data, event) {
		if (data === self.selectedTicketUrl()) {
			self.selectedTicketUrl(null);
		}
		if (data.ticket_url() === "") {
 			alert("Ticket Url can't be empty");
			data.ticket_url(self.selected_fr.ticket_url());
			return;
		}
		self.update_Feature(data);
		
	};
	
	self.isTicketUrlSelected = function(data) {
		self.selected_fr = data;
		return data === self.selectedTicketUrl();
	};
	
	
	
	
	self.update_Feature = function(data) {
		return  updateFeature(data);
	};
	
	//Save change after sort table
	this.updateLastAction = function(arg) {
		self.savePriorities();
	}
	
	//Delete feature
	self.deleteFeature = function(data){
	
		    $( "#dialog-confirm" ).dialog({
		      resizable: false,
		      height: "auto",
		      width: 400,
		      modal: true,
		      buttons: {
			"Delete Feature": function() {
			  delete_Feature(data.id());
			  self.features.remove(data);
			  $( this ).dialog( "close" );
			},
			Cancel: function() {
			  $( this ).dialog( "close" );
			}
		      }
		    });
		  
	}
}

 //control visibility, give element focus, and select the contents (in order)
        ko.bindingHandlers.visibleAndSelect = {
            update: function(element, valueAccessor) {
                ko.bindingHandlers.visible.update(element, valueAccessor);
                if (valueAccessor()) {
                    setTimeout(function() {
                        $(element).find("input").focus().select();
                    }, 0); //new tasks are not in DOM yet
                }
            }
        };
        
var fm = new FeatureListViewModel();
        
ko.bindingHandlers.sortable.afterMove = fm.updateLastAction;      
ko.applyBindings(fm);
