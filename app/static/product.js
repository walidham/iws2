function Product(data) {
    this.id = ko.observable(data.id);
    this.product_name = ko.observable(data.product_name);
    this.description = ko.observable(data.description);
}

function ProductListViewModel() {
    var self = this;
    self.products = ko.observableArray([]);
    self.newProductName = ko.observable();
    self.newProductDesc = ko.observable();

    self.addProduct = function() {
	self.save();
	self.newProductName("");
        self.newProductDesc("");
    };

    $.getJSON('/products_list', function(productModels) {
	var t = $.map(productModels.products, function(item) {
	    return new Product(item);
	});
	self.products(t);
    });

    self.save = function() {

	return $.ajax({
	    url: '/new_product',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'product_name': self.newProductName(),
		'description': self.newProductDesc()
	    }),
	    success: function(data) {
		console.log("Pushing to products array");
		self.products.push(new Product(data));
		if(data.result=="OK"){
			$('#new_product').modal('hide')
			return;
		}else{
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

ko.applyBindings(new ProductListViewModel());
