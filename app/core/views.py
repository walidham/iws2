# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint, jsonify
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted, roles_required
from app import app, db
from app.core.models import UserProfileForm, FeatureRequest, User, Product, UsersRoles, Role
from flask_wtf import csrf

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
def clients_list():

    cur =  User.query.join(User.roles).filter(Role.name == 'client').group_by(User).order_by(User.id).all()
    entries = [dict(company_name=row.company_name,email=row.email,
    description="",id=row.id,last_name=row.last_name, first_name=row.first_name,priority=row.priority) for row in cur]
    return jsonify(clients=entries)
    
    
# Product Route
@app.route('/products')
@roles_required('admin')
@login_required
def products():
           
    products = Product.query.all()
    return render_template('core/products.html',
                       products=products)
  
# User Route
@app.route('/users')
@roles_required('admin')
@login_required
def users():
           
    users = User.query.join(User.roles).filter(Role.name == 'user').group_by(User).all()
    return render_template('core/users.html',
                       users=users)
  
