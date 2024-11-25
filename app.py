from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app=Flask(__name__)


# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#initialize the database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
 
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
 
# Routes

@app.route('/', methods=['GET'])
def start():
    # return jsonify({'message': 'hello'})
    return render_template('index.html')



@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        data = request.json
        user = User(name=data['username'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created!', 'user': {'id': user.id, 'name': user.username}})
    
    users = User.query.all()
    return render_template('users.html', users=users) 


@app.route('/products', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'POST':
        data = request.json
        product = Product(name=data['name'], price=data['price'])
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created!', 'product': {'id': product.id, 'name': product.name, 'price': product.price}})
    
    products = Product.query.all()
    return render_template('products.html', products=products)
 
@app.route('/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'POST':
        data = request.json
        order = Order(user_id=data['user_id'], product_id=data['product_id'])
        db.session.add(order)
        db.session.commit()
        return jsonify({'message': 'Order created!', 'order': {'id': order.id, 'user_id': order.user_id, 'product_id': order.product_id}})
    
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)
 
# Initialize the database
# def create_tables():
#     with app.app_context():
#         db.create_all()

@app.before_request
def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()
 
if __name__ == '__main__':
    # Create tables before starting the application
    # create_tables()
    app.run(debug=True)