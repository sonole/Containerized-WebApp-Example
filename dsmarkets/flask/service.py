from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response, sessions, session
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import json, os, sys, uuid, time
sys.path.append('./data')

# Connect to our local MongoDB

mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

# Choose InfoSys database
db = client['InfoSys']
users = db['Users']
products = db['Products']

# Initiate Flask App
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
# The cart expires after 2 minutes (testing)
#app.permanent_session_lifetime = timedelta(minutes=2)
# The cart expires after 60 minutes
app.permanent_session_lifetime = timedelta(minutes=60)

users_sessions = {}
admins_sessions = {}

def create_session_simple(email):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (email, time.time())
    return user_uuid 


def create_session_admin(email):
    admin_uuid = str(uuid.uuid1())
    admins_sessions[admin_uuid] = (email, time.time())
    return admin_uuid  

def is_session_valid_simple(user_uuid):
    return user_uuid in users_sessions

def is_session_valid_admin(admin_uuid):
    return admin_uuid in admins_sessions


# 1: User Registration
@app.route('/userRegistration', methods=['POST'])
def user_registration():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # If user dosn't exists
    if users.find({"email":data["email"]}).count() == 0 :
        user = {
            "email": data['email'], 
            "password": data['password'],
            "category": "simple_user",
            "orderHistory": 0}
        # Add user to the 'users' collection
        users.insert_one(user)
        return Response(data['email']+" was added to the MongoDB", status=200, mimetype='application/json') 
    else:
        return Response("A user with the given email already exists", status=400, mimetype='application/json') 


# 2: Login
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # If credentials exists then create session 
    if users.find( { '$and': [ {'email':data["email"]}, {'password':data["password"]} ] }  ).count() ==1:
        # If user is administrator then create_session in admin list
        if users.find( { '$and': [ {'email':data["email"]}, {'password':data["password"]}, {'category':'administrator'} ] }  ).count() ==1:
            admin_uuid = create_session_admin(data['email'])
            res = {"uuid": admin_uuid, "email": data['email']}
        elif users.find( { '$and': [ {'email':data["email"]}, {'password':data["password"]}, {'category':'simple_user'} ] }  ).count() ==1:
            user_uuid = create_session_simple(data['email'])
            res = {"uuid": user_uuid, "email": data['email']}
            # we want cart only on simple user:
            session.permanent = True
        return Response(json.dumps(res), status=200, mimetype='application/json') 
    else:
        return Response("Wrong email or password.",status=400, mimetype='application/json')


# 3: Product Registration
@app.route('/productRegistration', methods=['POST'])
def product_registration():
    # Request headers
    uuid = request.headers.get('authorization')
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "category" in data or not "stock" in data or not "description" in data or not "price" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # Check if headers are empty
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else: 
        # Check if admin is logged in
        if not is_session_valid_admin(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            product = {
                "name": data['name'], 
                "category": data['category'],
                "stock": data['stock'],
                "description": data['description'],
                "price": data['price']
            }
            products.insert_one(product)
            return Response("The product with name '"+data['name']+"' was added to the MongoDB", status=200, mimetype='application/json') 


# 4: Product Deletion
@app.route('/productDeletion', methods=['DELETE'])
def product_deletion():
    # Request headers
    uuid = request.headers.get('authorization')
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "_id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # Check if headers are empty
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        # Check if admin is logged in
        if not is_session_valid_admin(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            if products.find({"_id":ObjectId(data["_id"])}).count() ==1:
                products.delete_one({"_id":ObjectId(data["_id"])})
                msg = "Product with id: "+data['_id']+", was deleted."
                return Response(msg, status=200, mimetype='application/json')
            else:
                msg = "Product with id: "+data['_id']+", dosen\'t exists in DB."
                return Response(msg,status=500,mimetype='application/json')


# 5: Product Update
@app.route('/productUpdate', methods=['PUT'])
def product_update():
    # Request headers
    uuid = request.headers.get('authorization')
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "_id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    # Request Arguments
    name = request.args.get('name')
    category = request.args.get('category')
    stock = request.args.get('stock')
    description = request.args.get('description')
    price = request.args.get('price')
    if name==None and category==None and stock==None and description==None and price==None:
        return Response("Bad request (no arguments).", status=500, mimetype='application/json')

    # Check if headers are empty
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        # Check if admin is logged in
        if not is_session_valid_admin(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Check if product exists
            if products.find({"_id":ObjectId(data["_id"])}).count() ==1:
                # Create a list to irritate
                attributes = [name, category, stock, description, price]
                i = 0
                for attribute in attributes:
                    if i == 0:
                        field = 'name'
                    elif i == 1:
                        field = 'category'
                    elif i == 2:
                        field = 'stock'
                    elif i == 3:
                        field = 'description'
                    elif i == 4:
                        field = 'price'
                    if attribute != None:
                        # Conver from string to int or float for mongodb insert
                        if i == 2:
                            attribute = int(stock)
                        if i == 4:
                            attribute = float(price)
                        # Update Product
                        products.update( 
                            { '_id': ObjectId(data["_id"]) },
                            { '$set': { 
                                field: attribute } })
                    i = i + 1
                # Display Product
                product = products.find_one({"_id":ObjectId(data["_id"])})
                product = {'name':product["name"], 'category':product['category'], 'stock':product["stock"], 
                            'description':product["description"], 'price':product["price"]}
                return Response("Product's info updated: "+json.dumps(product), status=200, mimetype='application/json')
            else:
                return Response("Product dosen\'t exist in DB",status=500,mimetype='application/json')


# 6: Get Product
@app.route('/getProduct', methods=['GET'])
def get_product():
    # Request headers
    uuid = request.headers.get('authorization')
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data and not "category" in data and not "_id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    if len(data) > 1:
        return Response("Too many fields. Only 1 is allowed",status=500,mimetype="application/json")
    # Check if headers are empty
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        # Check if admin is logged in
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            if "name" in data:
                # Count the products with the same name
                counter = products.find( { 'name' : data['name'] } ).count()
                if counter >0:
                    prods = products.find( { 'name' : data['name'] } ).sort('name')
                    output = []
                    for prod in prods:
                        prod = { 'name': prod['name'], 'description': prod['description'],
                                'price':prod['price'], 'category': prod['category'], 'product ID': str(prod['_id'])}
                        output.append(prod)
                    msg = 'Found '+str(counter)+' product(s) with  the name: '+data['name']+' '
                    return Response(msg+json.dumps(output), status=200, mimetype='application/json')
                else:
                    return Response("The product name: "+data['name']+", wasnt found in DB",status=500,mimetype='application/json')
            elif "category" in data:
                # Alternative way to search for products
                # counter = products.find({ '$text': { '$search': data['category'] } }).count()
                # Count the products with the same category
                counter = products.find( { 'category': data['category'] } ).count()
                if counter >0:
                    prods = products.find( { 'category': data['category'] } ).sort('price')
                    output = []
                    for prod in prods:
                        prod = { 'name': prod['name'], 'description': prod['description'],
                                'price':prod['price'], 'category': prod['category'], 'product ID': str(prod['_id'])}
                        output.append(prod)
                    msg = 'Found '+str(counter)+' product(s) with  the category: '+data['category']+' '
                    return Response(msg+json.dumps(output), status=200, mimetype='application/json')
                else:
                    return Response("The product category: "+data['category']+", wasnt found in DB",status=500,mimetype='application/json')
            elif "_id" in data:
                # Check if _id exists
                if products.find({"_id":ObjectId(data['_id'])}).count() ==1:
                    # Display Product
                    prod = products.find_one({"_id":ObjectId(data['_id'])})
                    prod = { 'name': prod['name'], 'description': prod['description'],
                                    'price':prod['price'], 'category': prod['category'], 'product ID': str(prod['_id'])}
                    return Response("Here is the requested product: "+json.dumps(prod), status=200, mimetype='application/json')
                else:
                    return Response("Product with _id: "+data['_id']+", dosen\'t exist in DB",status=500,mimetype='application/json')
    

# 7: Add To Cart
@app.route('/addToCart', methods=['POST'])
def add_to_cart():
    # Request headers
    uuid = request.headers.get('authorization')
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "_id" in data or not "quantity" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        # Check if simple user is logged in
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Check if product exist
            if products.find({"_id":ObjectId(data['_id'])}).count()==1:
                # Make sure given quantity is int
                if isinstance(data['quantity'], int):
                    product = products.find_one({"_id":ObjectId(data['_id'])})
                    product = { 'stock': product['stock'], 
                        'price':product['price'],'_id': str(product['_id'])}
                    # Kill if product out of stock
                    if data['quantity'] > product['stock']:
                        return Response("Max quantity for this product is "+str(product['stock']),status=500,mimetype='application/json')
                    
        
                    # Unique cart for user
                    cart = str(uuid)+'cart'

                    # If cart already set
                    if cart in session:
                        # If product already exists in cart
                        if data['_id'] in session[cart]:
                            # Save in x the quantity of the product on cart
                            x = session[cart].get(data['_id'])
                            y = x + data['quantity']
                            # Kill if product out of stock
                            if y > product['stock']:
                                return Response("Max quantity for this product is "+str(product['stock']),status=500,mimetype='application/json')
                            #session[cart] = [{data['_id']: y}]
                            session[cart].update({data['_id']: y})
                        # Else new product, append to cart
                        else:
                            session[cart].update({data['_id']: data['quantity']})
                    else:
                        # Create cart and add product
                        session[cart] = ({data['_id']: data['quantity']})
                    return Response("Product Added to cart"+json.dumps(session[cart]),status=200,mimetype='application/json')

                else:
                    return Response("Quantity must be an int",status=500,mimetype='application/json')
            else:
                return Response("Product with _id: "+data['_id']+", dosen\'t exist in DB",status=500,mimetype='application/json')

# 8: Cart
@app.route('/cart', methods=['GET'])
def cart():
    # Request headers
    uuid = request.headers.get('authorization')

    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        # Check if simple user is logged in
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Unique cart for user
            cart = str(uuid)+'cart'
            if cart in session:
                # Create new list to print the cart with product names
                output = {}
                # Total cart value
                cart_value = 0
                for id, quantity in session[cart].items():
                    product = products.find_one({"_id":ObjectId(id)}) 
                    cart_value += quantity * product['price']
                    output.update({product['name']:quantity})
                # Round total value
                cart_value = round(cart_value, 2)
                msg = "Here is your cart\n"+json.dumps(output)+"\nTotal: "+str(cart_value)
                return Response(msg,status=200,mimetype='application/json')
            else:
                return Response("First you have to add products to cart.",status=200,mimetype='application/json') 


# 9: Remove From Cart
@app.route('/removeFromCart/<string:pID>', methods=['DELETE'])
def remove_from_cart(pID):
    # Request headers
    uuid = request.headers.get('authorization')
    if pID == None:
        return Response("you have to provide id after url",status=500,mimetype='application/json')
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Unique cart for user
            cart = str(uuid)+'cart'
            if cart in session:
                flag = False
                for id, quantity in session[cart].items():
                    if id == pID:
                        session[cart].pop(pID)
                        flag = True
                        # Create new list to print the cart with product names
                        output = {}
                        # Total cart value
                        cart_value = 0
                        for id, quantity in session[cart].items():
                            product = products.find_one({"_id":ObjectId(id)}) 
                            cart_value += quantity * product['price']
                            output.update({product['name']:quantity})
                        # Round total value
                        cart_value = round(cart_value, 2)
                        msg = "Product has been removed from cart\nYour new cart\n"+json.dumps(output)+"\nTotal: "+str(cart_value)
                        return Response(msg,status=200,mimetype='application/json')

                if flag == False:
                    return Response("Product has not been added to cart",status=500,mimetype='application/json')
            else:
                return Response("First you have to add products to cart.",status=500,mimetype='application/json') 


# 10: Place an Order
@app.route('/order', methods=['POST'])
def order():
    # Request headers
    uuid = request.headers.get('authorization')
     # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "card_no" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    else:
        # Validate given data
        if not isinstance(data['card_no'], int) or len(str(data['card_no'])) != 16:
            return Response("You have to enter a 16-digit number",status=500,mimetype="application/json")
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Fetch cart
            # Unique cart for user
            cart = str(uuid)+'cart'
            if cart in session:
                # Create new list to print the cart with product names
                output = {}
                # Total cart value
                cart_value = 0
                for id, quantity in session[cart].items():
                    product = products.find_one({"_id":ObjectId(id)}) 
                    # Check again for stock
                    if quantity>product['stock']:
                        flag = True
                        return Response("Sorry someone was quicker than you.\nProduct out of stock.\nPlease remove product from cart and then continue.",status=500,mimetype='application/json')
                    else:
                        cart_value += quantity * product['price']
                        output.update({product['name']:quantity})
                        new_stock = product['stock'] - quantity
                        # Update Product on DB
                        products.update( 
                            { '_id': ObjectId(id) },
                            { '$set': { 
                                'stock': new_stock } })
                        flag = False
                
                # Empty the cart
                session[cart] = {}

                # Print Receipt
                if flag == False:
                    # Update user orderHistory field
                    # Find the loged in email
                    email = users_sessions[uuid][0]
                    users.update( 
                            { 'email': email },
                            { '$inc': { 
                                'orderHistory': 1 } })
                    users.update( 
                            { 'email': email },
                            { '$push': { 
                                'orderDetails': output } })            
                    # Get time
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    # Round total value
                    cart_value = round(cart_value, 2)
                    msg = "Here is your receipt\n"
                    msg += "\nWe are charging the amount of "+str(cart_value)+" and then we place the order"
                    msg += "\n********DS MARKETS********"
                    msg += "\nAFM:099360626, DOY:PEIRAIA"
                    msg += "\nIlioupoleos 56, 17236, GR"
                    msg += "\n**************************"
                    msg += "\n"+json.dumps(output)
                    msg += "\nValue:\t\t"+str(cart_value)
                    msg += "\nThank you for choosing us!"
                    msg += "\n***"+dt_string+"***"
                    return Response(msg,status=200,mimetype='application/json') 
                else:
                    return Response("Somothing went wrong.",status=404,mimetype='application/json')
            else:
                return Response("Cart is empty..",status=500,mimetype='application/json')

# 11: Orders History
@app.route('/getOrders', methods=['GET'])
def get_orders():
    # Request headers
    uuid = request.headers.get('authorization')
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Find the loged in email
            email = users_sessions[uuid][0]
            # Fetch orders
            user = users.find_one({'email':email})
            if user['orderHistory'] == 0:
                msg = "You have to place an order first."
                return Response(msg,status=500,mimetype='application/json')
            if user['orderHistory'] == 1:
                msg = "You have placed "+str(user['orderHistory'])+" order.\n"
                msg += "Details:\n"
                msg += json.dumps(user['orderDetails'])     
            else: 
                msg = "You have placed "+str(user['orderHistory'])+" orders.\n"
                msg += "Details:\n"
                msg += json.dumps(user['orderDetails'])
            return Response(msg,status=200,mimetype='application/json')
            
            
# 12: User Deletion
@app.route('/deleteAccount', methods=['DELETE'])
def delete_account():
    # Request headers
    uuid = request.headers.get('authorization')
    if not uuid:
        return Response("bad header request",status=500,mimetype='application/json')
    else:
        if not is_session_valid_simple(uuid):
            return Response("You don't have authorization, get out!",status=401,mimetype='application/json')
        else:
            # Find the loged in email
            email = users_sessions[uuid][0]
            msg = "You are logged out.\n"
            # Delete user
            users.delete_one({'email':email})
            msg += "And your account has been removed."
            # Log out
            users_sessions.pop(uuid)
            return Response(msg, status=200,mimetype='application/json')


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
