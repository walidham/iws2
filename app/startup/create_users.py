from datetime import datetime
from app import app, db
from app.core.models import User, Role, Product, FeatureRequest


def create_users():
    """ Create users when app starts """
    from app.core.models import User, Role

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    user_role = find_or_create_role('user', u'User')
    client_role = find_or_create_role('client', u'Client')

    # Add users
    admin = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(u'User', u'Example', u'user@example.com', 'Password1',user_role)
    client = find_or_create_user(u'Client', u'Example', u'client@example.com', 'Password1',client_role)

    #Add Product
    prod1 = find_or_create_product('Policies','This is IWS product examlpe')
    prod2 = find_or_create_product('Biling','This is IWS product examlpe')

    # Add features Requests
    fr = find_or_create_feature('Feature Request user 1','This is Feature Request added by User IWS',
                                 datetime.utcnow(),'http://www.britecore.com',user,prod1);

    fr = find_or_create_feature('Feature Request clien 2','This is Feature Request added by Client',
                                 datetime.utcnow(),'http://www.britecore.com',client,prod2);
    fr = find_or_create_feature('Feature Request client 3','This is Feature Request added by Client',
                                 datetime.utcnow(),'http://www.britecore.com',client,prod1);
    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

def find_or_create_product(product_name, description):
    """ Find existing product or create new product """
    prod = Product.query.filter(Product.product_name == product_name).first()
    if not prod:
        prod = Product(product_name=product_name,
                    description=description)
        
        db.session.add(prod)
    return prod

def find_or_create_feature(title, description, target_date, ticket_url, user, prod):
    
    fr = FeatureRequest(title=title, description=description, target_date=target_date, ticket_url=ticket_url, user_id=user.id, product_id=prod.id)
   
    db.session.add(fr)
    return fr


