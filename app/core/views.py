# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint, jsonify
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted, roles_required
from app import app, db
from app.core.models import UserProfileForm, FeatureRequest, User, Product, UsersRoles, Role
from flask_wtf import csrf
from datetime import datetime
from sqlalchemy import func

core_blueprint = Blueprint('core', __name__, url_prefix='/')


# The Home page is accessible to anyone
@core_blueprint.route('')
def home_page():
    if not current_user.is_authenticated:
        return render_template('core/guest_page.html')
    else:
        return render_template('core/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@core_blueprint.route('user')
@login_required  # Limits access to authenticated users
def user_page():
    return render_template('core/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@core_blueprint.route('admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('core/admin_page.html')


@core_blueprint.route('user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('core.home_page'))

    # Process GET or invalid POST
    return render_template('core/user_profile_page.html',
                           form=form)


# Register blueprint
app.register_blueprint(core_blueprint)

# Feature Route
@app.route('/features')
@login_required
def feature_request():
    # Test if user is IWS user or client
    if current_user.roles[0].name == 'client':
        features = FeatureRequest.query.filter(FeatureRequest.user_id == current_user.id)
        return render_template('core/feature_requests.html',
                           features=features)
    else:
        features = FeatureRequest.query.all()
        return render_template('core/feature_requests.html',
                           features=features)
                           
                           
                           
@app.route('/new_feature', methods=['POST'])
def new_feature():
    if current_user.roles[0].name == 'client':
        #If feature added by client
        
        #get the count of FR gp : global priority
       
        gp = db.session.query(func.count(FeatureRequest.id)).scalar()  
        #by default the priority will be in the end      
        gp = gp +1                                    
         
        #get the count of FR cp : client priority
        cp = db.session.query(func.count(FeatureRequest.id)).filter(FeatureRequest.user_id == current_user.id).scalar()        
        #by default the priority will be in the end
        cp = cp +1                                     
        date_object = datetime.strptime(request.json['target_date'], '%m-%d-%Y')
        feature = FeatureRequest(title=request.json['title'],description=request.json['description'],
                                 target_date=date_object,ticket_url=request.json['ticket_url'],
                                 user_id=current_user.id,product_id=request.json['product_id'],
                                 global_priority=gp,client_priority=cp)

        db.session.add(feature)
        db.session.commit()
        #id = cur.lastrowid
        return jsonify({"title": request.json['title'], 
                    "description": request.json['description'],
                    "client_priority": cp,
                    "global_priority": gp,
                    "target_date": request.json['target_date'],
                    "ticket_url": request.json['ticket_url'],
                    "client_id": request.json['client_id'],
                    "id": feature.id,
                    "product_id": request.json['product_id']})
    else:
        #If feature added by IWS USER
        
        #get the count of FR gp : global priority
        gp = db.session.query(func.count(FeatureRequest.id)).scalar()
        #by default the priority will be in the end       
        gp = gp +1                                     
        
        #get the count of FR cp : client priority
        cp = db.session.query(func.count(FeatureRequest.id)).filter(FeatureRequest.user_id == request.json['client_id']).scalar()        
        
        
        cp = cp + 1                                     
        date_object = datetime.strptime(request.json['target_date'], '%m-%d-%Y')
        feature = FeatureRequest(title=request.json['title'],description=request.json['description'],
                                 target_date=date_object,ticket_url=request.json['ticket_url'],
                                 user_id=request.json['client_id'],product_id=request.json['product_id'],
                                 global_priority=gp,client_priority=cp)

        db.session.add(feature)
        db.session.commit()
        #id = cur.lastrowid
        return jsonify({"title": request.json['title'], 
                    "description": request.json['description'],
                    "client_priority": cp,
                    "global_priority": gp,
                    "target_date": request.json['target_date'],
                    "ticket_url": request.json['ticket_url'],
                    "client_id": request.json['client_id'],
                    "id": feature.id,
                    "product_id": request.json['product_id']})
    
                    
                    
@app.route('/save_priorities', methods=['POST'])
def save_priorities():
    if current_user.roles[0].name == 'client':
        id_feature = request.json['id']
        client_priority = request.json['priority']
        global_pri = request.json['global_priority']
        
        fr = FeatureRequest.query.filter_by(id=id_feature).first()
        fr.global_priority = global_pri
        fr.client_priority = client_priority
        #db.session.query(FeatureRequest).filter_by(id = id_feature).update({'global_priority': int(priority)})
        db.session.commit()
        return jsonify(reponse=dict(result="ok"))
    else:
        id_feature = request.json['id']
        priority = request.json['priority']
      
        fr = FeatureRequest.query.filter_by(id=id_feature).first()
        fr.global_priority = priority
        
        #db.session.query(FeatureRequest).filter_by(id = id_feature).update({'global_priority': int(priority)})
        db.session.commit()
        #FeatureRequest.query.filter(FeatureRequest.id == id_feature).update(dict(global_priority = priority))
        #db.session.commit()
        return jsonify(reponse=dict(result="ok"))

@app.route('/features_list')
def features_list():
    if current_user.roles[0].name == 'client':
        cur =  FeatureRequest.query.filter(FeatureRequest.user_id == current_user.id).order_by(FeatureRequest.client_priority)
        entries = [dict(id=row.id,title=row.title,
        target_date=row.target_date,description=row.description,ticket_url=row.ticket_url, client_priority=row.client_priority,
        global_priority=row.global_priority, client_id = row.user_id, product_id=row.product_id) for row in cur]
        return jsonify(features=entries)
    else:
        cur =  FeatureRequest.query.order_by(FeatureRequest.global_priority).all()
        entries = [dict(id=row.id,title=row.title,
        target_date=row.target_date,description=row.description,ticket_url=row.ticket_url, client_priority=row.client_priority,
        global_priority=row.global_priority, client_id = row.user_id, product_id=row.product_id) for row in cur]
        return jsonify(features=entries)

# Client Route
@app.route('/clients')
@roles_required('admin')
@login_required
def clients():
           
    clients = User.query.join(User.roles).filter(Role.name == 'client').group_by(User).all()
    return render_template('core/clients.html',
                       clients=clients)

@app.route('/clients_list')
@roles_required('admin')
@login_required
def clients_list():

    cur =  User.query.join(User.roles).filter(Role.name == 'client').group_by(User).order_by(User.id).all()
    entries = [dict(company_name=row.company_name,email=row.email,
    description="",id=row.id,last_name=row.last_name, first_name=row.first_name,priority=row.priority) for row in cur]
    return jsonify(clients=entries)
    
@app.route('/new_client', methods=['POST'])
@roles_required('admin')
@login_required
def new_client():
    email = request.json['email']
    user = User.query.filter(User.email==email).first()
    if not user:
        user =  User(email=email, first_name=request.json['first_name'], last_name=request.json['last_name'],
                     password = app.user_manager.hash_password(request.json['password']), 
                     company_name=request.json['company_name'],  active=True,confirmed_at=datetime.utcnow())
                     
        role = Role.query.filter(Role.name == 'client').first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return jsonify({"email": request.json['email'], 
                    "first_name": request.json['first_name'],
                    "result": "OK",
                    "last_name": request.json['last_name'],
                    "company_name": request.json['company_name'],
                   })


    else:
        return jsonify({"result":"Error","msg":"email exist"})




# Product Route
@app.route('/products')
@roles_required('admin')
@login_required
def products():
           
    products = Product.query.all()
    return render_template('core/products.html',
                       products=products)

@app.route('/products_list')
def products_list():

    cur =  Product.query.all()
    entries = [dict(id=row.id,product_name=row.product_name, description=row.description) for row in cur]
    return jsonify(products=entries)
    
    
# User Route
@app.route('/users')
@roles_required('admin')
@login_required
def users():
           
    users = User.query.join(User.roles).filter(Role.name == 'user').group_by(User).all()
    return render_template('core/users.html',
                       users=users)


@app.route('/users_list')
@roles_required('admin')
@login_required
def users_list():

    cur =  User.query.join(User.roles).filter(Role.name == 'user').group_by(User).order_by(User.id).all()
    entries = [dict(email=row.email, id=row.id,last_name=row.last_name, first_name=row.first_name) for row in cur]
    return jsonify(users=entries)
    
@app.route('/new_user', methods=['POST'])
@roles_required('admin')
@login_required
def new_user():
    email = request.json['email']
    user = User.query.filter(User.email==email).first()
    if not user:
        user =  User(email=email, first_name=request.json['first_name'], last_name=request.json['last_name'],
                     password = app.user_manager.hash_password(request.json['password']), 
                     active=True,confirmed_at=datetime.utcnow())
                     
        role = Role.query.filter(Role.name == 'user').first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return jsonify({"email": request.json['email'], 
                    "first_name": request.json['first_name'],
                    "result": "OK",
                    "last_name": request.json['last_name'],
                    "id": user.id
                   })


    else:
        return jsonify({"result":"Error","msg":"email exist"})



  
