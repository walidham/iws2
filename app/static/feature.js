function Client(data) {
    
    this.id = data.id;
    this.company_name = data.company_name;
    this.email = ko.observable(data.email);
    this.last_name = ko.observable(data.last_name);
    this.first_name = ko.observable(data.first_name);
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
    this.client_name = ko.observable();
    this.product_id = ko.observable();
   
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

Feature.prototype.clone = function() {

    var  data = {"id":this.id, "title":this.title(), "email":this.email(), "global_priority":this.global_priority(), "client_priority":this.client_priority(),
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

function FeatureListViewModel() {


    var self = this;
    self.clients = ko.observableArray([]);

    $.getJSON('/clients_list', function(clientModels) {
	var t = $.map(clientModels.clients, function(item) {
	    return new Client(item);
	});
	
	self.clients(t);
    });



    self.features = ko.observableArray([]);

    self.newTitle = ko.observable();
    self.newDesc = ko.observable();
    self.newTargetDate = ko.observable();
    self.newTicketUrl = ko.observable();
    self.newClientPriority = ko.observable();
    self.newClient = ko.observable();
    

    self.addFeature = function() {
	self.save();
	self.newTitle("");
	self.newDesc("");
        self.newTargetDate("");
	self.newTicketUrl("");
	self.newClientPriority("");
	self.newClient("");
    };

    $.getJSON('/features_list', function(featureModels) {
   
	var t = $.map(featureModels.features, function(item) {
	
	    return new Feature(item,self);
	});
	self.features(t);
    });

    self.save = function() {

	return $.ajax({
	    url: '/new_feature',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'title': self.newTitle(),
		'target_date': self.newTargetDate(),
		'ticket_url': self.newTicketUrl(),
		'client_id': self.newClient().id,
		'client_priority': self.newClientPriority(),
		'description': self.newDesc()
	    }),
	    success: function(data) {
		console.log("Pushing to feature array");
		self.clients.push(new Client({ title: data.title, target_date: data.target_date, 
			description: data.description,ticket_url: data.ticket_url,client_priority: data.client_priority,client_id: data.client_id, id: data.id}));
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
    	var old_global_priority =[]
    	var index = 0;
    	//table of old global priorities
    	ko.utils.arrayForEach(self.features(), function(c) {
	 	
        
        	old_global_priority.push(c.global_priority());
        	
        	///////////:
    	});
    	
	 ko.utils.arrayForEach(self.features(), function(c) {
	 	priority = priority+1;
        	/////////////
        	
        	c.global_priority(priority);
        	save_priority(c.id(),priority,old_global_priority[index]);
        
        	index++;
        	
        	///////////:
    	});
	
    };
	// New code
	self.allowNewTask = ko.computed(function() {
		return self.features().length < 100;
	});
	
	self.selectedTask = ko.observable();
	
	self.clearTask = function(data, event) {
		if (data === self.selectedTask()) {
			self.selectedTask(null);
		}
		if (data.name() === "") {
			self.features.remove(data);
		}
	};
	
	self.isTaskSelected = function(task) {
		return task === self.selectedTask();
	};
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
        
ko.applyBindings(new FeatureListViewModel());
