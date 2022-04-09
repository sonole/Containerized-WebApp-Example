<h1>DSMarkets</h1>
<p>Containerized Web App using Docker, Flask, MongoDB</p>
<br><hr><br>

<h3>Οδηγίες εκτέλεσης</h3>
Όπως ζητήθηκε έχει γίνει containerize το web service που καλούμαστε να υλοποιήσουμε,<br/>
το docker-compose είναι υπεύθυνο για την ταυτόχρονη λειτουργία των 2 container (MongoDB, Flask)<br/>
Ενώ το Docker image έχει base os Ubuntu 18.04, Python3, pip, data folder*, expose πόρτα 5000, entrypoint το "service.py"<br/>
1) Κάνουμε clone το repo<br/>
2) Αλλάζουμε dir στον "dsmarkets"<br/>
<pre>
	$ cd dsmarkets
	$ ls 
	docker-compose.yml  flask
</pre>
3) Από τον φάκελο που βρίσκονται τα δύο αρχεία docker-compose.yml και flask, τρέχουμε to docker με εντολή<br/>
<pre>
	$ docker-compose up -d
</pre>
4) Οταν τα 2 containers τρέχουν θα έχουμε το εξής μήνυμα:<br/>
![Containers Ready](https://raw.githubusercontent.com/sonole/sonole/main/assets/containers_ready.jpg)
5) Έπειτα αντιγράφουμε τα δύο collections στο container mongodb με την εξής εντολή:<br/>
<pre>
	$ docker cp flask/data/users.json mongodb:/users.json && docker cp flask/data/products.json mongodb:/products.json
</pre>
6) Τέλος κάνουμε import στην βάση InfoSys τα δύο αρχεία με την εξής εντολή:<br/>
<pre>
	$ docker exec -it mongodb mongoimport --db=InfoSys --collection=Users --file=users.json && docker exec -it mongodb mongoimport --db=InfoSys --collection=Products --file=products.json
</pre>
7) Επιβεβαιώνουμε οτι το flask service τρέχει χωρίς κάποιο πρόβλημα<br/>
<pre>
	$ docker logs flask
</pre>
![Flask Up And Running](https://raw.githubusercontent.com/sonole/sonole/main/assets/flask_ok.jpg)

<br/>
Σημείωση:
Μιας και στο συγκεκριμένο πληροφοριακό σύστημα οι χρήστες που μπορούν να κάνουν εγγραφη μέσο του web-service<br/>
έχουν δικαιώματα μόνο σαν απλός χρήστης και όχι σαν διαχειριστής, για να προσθέσουμε έναν administrator εκτελούμε:<br/>
<pre>
	$ docker exec -it mongodb mongo --port 27017
	$ db.Users.insertOne({"email":"admin@dsmarket.com","password":"admin","category":"administrator"})
</pre>
Στο collection "Users" που προσθέσαμε στο βήμα 5, ο παραπάνω διαχειριστής έχει προστεθεί ήδη.<br/>

<br/>
<hr>

### Παρακάτω βρίσκονται τα παραδείγματα εκτελέσεων requests και των απαντησεων που παίρνουμε σε κάθε entrypoint :
<pre>
###########################
### 1 User Registration ###
###########################
Request:
Type: POST
Url : http://0.0.0.0:5000//userRegistration
Body:
{
    "email": "alex@gmail.com", 
    "password": "passalex"
}

Response:
alex was added to the MongoDB (status=200)

Στην περίπτωση που το email υπάρχει ήδη
μας επιστρέφρει "A user with the given email already exists" (status=400)
</pre>
</br>
<pre>
##########################
####### 2 Login ##########
##########################
Request:
Type: POST
Url : http://0.0.0.0:5000/login
Body:
{
    "email": "alex@gmail.com", 
    "password": "passalex"
}

Response:
{
    "email": "alex@gmail.com",
    "uuid": "6726435c-b57b-11eb-8fab-000c29b50a20"
}


Στην περίπτωση που ο συνδιασμός email+pass δεν υπάρχει 
μας επιστρέφρει "Wrong email or password" (status=400)
</pre>
</br>
<pre>
############################
## 3 Product Registration ##
############################
Request:
Type: POST
Url : http://0.0.0.0:5000/productRegistration
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003
Body:
{
    "name": "Jose Cuervo Tequila Silver 700ML", 
    "category": "Alcohol Drinks",
    "stock": 15,
    "description": "Μια πραγματικά ασημένια τεκίλα, η Cuervo® Silver είναι η επιτομή της απαλότητας. 
    Οι κύριοι αποσταγματοποιητές στην La Rojeña δημιούργησαν αυτό το μοναδικό 			    
    και ισορροπημένο μείγμα για να αναδείξει τις αποχρώσεις της αγαύης, καραμέλας, 
    και φρέσκων μυρωδικών στο προφίλ της γεύσης της.",
    "price": 22.6
}

Response:
The product with name 'Jose Cuervo Tequila Silver 700ML' was added to the MongoDB

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν administrator και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
##########################
### 4 Product Deletion ###
##########################
Request:
Type: DELETE
Url : http://0.0.0.0:5000/productDeletion
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003
Body:
{ "_id":"60be81cf8db7ab143482ccf7" }

Response:
Product with id: 60be81cf8db7ab143482ccf7, was deleted.

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Στην περίπτωση που το _id δεν υπάρχει τότε μας εμφανίζεται:
Product with id: 60be81cf8db7ab143482ccf7, dosen't exists in DB.

Σημ: Προυποθέτει να έχουμε κάνει login σαν administrator και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
########################
### 5 Product Update ###
########################
Request:
Type: PUT
Url : http://0.0.0.0:5000/productUpdate?name=Αυγά%20Βιολογικά%20Medium%206%20Τεμ%20OFFER!!&price=3.80&stock=5
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body:
{ "_id":"60be81978db7ab143482ccf6" }

Response:
Product's info updated: {
    name": "Αυγά Βιολογικά Medium 6 Τεμ OFFER!!",
    "category": "Dairy Products",
    "stock": 5,
    "description": "Τα «Αυγά Βιολογικής Γεωργίας» από τα ΧΡΥΣΑ ΑΥΓΑ παράγονται 
    από κότες που ζουν ελεύθερες σε εύφορους αγρότοπους και τρέφονται αποκλειστικά 
    και μόνο με τις πιο αγνές, φυτικές τροφές Βιολογικής Γεωργίας.",
    "price": 3.8
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Στην περίπτωση που το _id δεν υπάρχει τότε μας εμφανίζεται:
  Product dosen't exists in DB.

Σημ: Προυποθέτει να έχουμε κάνει login σαν administrator και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
#####################
### 6 GET PRODUCT ###
#####################
Request:
Type: GET
Url : http://0.0.0.0:5000/getProduct
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body:
{"name" : "Avga Viologika Medium 6 Tem OFFER!!"}
or 
{ "category" : "Dairy Products" } 
or 
{ "_id" : "60be81978db7ab143482ccf6" }


Response:
Found 4 product(s) with  the category: Dairy Products [
    {
        "name": "Fresko Gala Elafry 1,5% Lipara 1 lt, OLYMPOS",
        "description": "Το 100% ελληνικό φρέσκο επιλεγμένο γάλα ΟΛΥΜΠΟΣ συλλέγεται καθημερινά 
	από επιλεγμένες μονάδες που βρίσκονται σε μικρές αποστάσεις από τις εγκαταστάσεις μας 
	και πληροί αυστηρότερα στάνταρ από αυτά που προβλέπει η ευρωπαϊκή νομοθεσία.",
        "price": 1.48,
        "category": "Dairy Products",
        "product ID": "60be81658db7ab143482ccf5"
    },
    {
        "name": "Avga Viologika Medium 6 Tem OFFER!!",
        "description": "Τα «Αυγά Βιολογικής Γεωργίας» από τα ΧΡΥΣΑ ΑΥΓΑ παράγονται από κότες 
	που ζουν ελεύθερες σε εύφορους αγρότοπους και τρέφονται αποκλειστικά και μόνο με τις 
	πιο αγνές, φυτικές τροφές Βιολογικής Γεωργίας.",
        "price": 3.5,
        "category": "Dairy Products",
        "product ID": "60bf71b0fe789a2bdd2da523"
    },
    {
        "name": "Avga Viologika Medium 6 Tem OFFER!!",
        "description": "Τα «Αυγά Βιολογικής Γεωργίας» από τα ΧΡΥΣΑ ΑΥΓΑ παράγονται από κότες 
	που ζουν ελεύθερες σε εύφορους αγρότοπους και τρέφονται αποκλειστικά και μόνο με τις 
	πιο αγνές, φυτικές τροφές Βιολογικής Γεωργίας.",
        "price": 3.8,
        "category": "Dairy Products",
        "product ID": "60be81978db7ab143482ccf6"
    },
    {
        "name": "Avga Viologika Medium 12 Tem OFFER!!",
        "description": "Τα «Αυγά Βιολογικής Γεωργίας» από τα ΧΡΥΣΑ ΑΥΓΑ παράγονται από κότες
	που ζουν ελεύθερες σε εύφορους αγρότοπους και τρέφονται αποκλειστικά και μόνο με τις 
	πιο αγνές, φυτικές τροφές Βιολογικής Γεωργίας.",
        "price": 6.4,
        "category": "Dairy Products",
        "product ID": "60bf710afe789a2bdd2da522"
    }
]

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Search by name => alphabetical sort
->Search by price => price sort
->Στην περίπτωση που το το search αποτυγχάνει πάντα εμφανίζεται κάποιο αντίστοιχο μήνυμα

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
#####################
### 7 ADD TO CART ###
#####################
Request:
Type: POST
Url : http://0.0.0.0:5000/addToCart
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body:
{
    "_id" : "60bf71b0fe789a2bdd2da523",
    "quantity": 2
}

Response:
Product Added to cart{
    "60bf71b0fe789a2bdd2da523": 2
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Στην περίπτωση που το id του προιοντος δεν υπάρχει ή αν το quantity δεν ειναι int,
  τότε έχουμε αντίστοιχα μηνύματα σφάλματος
->Αν ξαναστείλουμε το request τότε απλά για το ίδιο id το quantity αυξάνεται ανάλογα με το request.
->Πάντα ελέγχεται να μην υπερβαίνουμε το απόθεμα του προίοντος

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
####################
###### 8 CART ######
####################
Request:
Type: GET
Url : http://0.0.0.0:5000/cart
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20

Response:
Here is your cart
{
    "Jose Cuervo Tequila Silver 700ML": 2,
    "Fresko Gala Elafry 1,5% Lipara 1 lt, OLYMPOS": 2,
    "Avga Viologika Medium 6 Tem OFFER!!": 1
}
Total: 51.96

->Στην περίπτωση που δεν έχει μπει κανένα προιόν στο καλάθι τότε
  μας επιστρέφει "First you have to add products to cart." (status=200)
->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
########################
## 9 REMOVE FROM CART ##
########################
Request:
Type: DELETE
Url : http://0.0.0.0:5000/removeFromCart/60be81978db7ab143482ccf6
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20

Response:
Product has been removed from cart
Your new cart
{
    "Jose Cuervo Tequila Silver 700ML": 2,
    "Fresko Gala Elafry 1,5% Lipara 1 lt, OLYMPOS": 2
}
Total: 48.16

->Στην περίπτωση που το καλάθι μας είναι άδειο τότε δεν μπορεί να δαιγραφεί κάποιο προιον και άρα
  μας επιστρέφει "First you have to add products to cart." (status=500)
->Στην περίπτωση που το προιον δεν υπάρχει στο καλάθι
  μας επιστρέφει "Product has not been added to cart." (status=500)
->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
########################
## 10 PLACE AN ORDER ###
########################
Request:
Type: POST
Url : http://0.0.0.0:5000/order
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body:
{
    "card_no" : 1234567812345678
}

Response:
Here is your receipt

We are charging the amount of 77.26 and then we place the order
********DS MARKETS********
AFM: 099360626, DOY:PEIRAIA
Ilioupoleos 56,
17236, GR
**************************
{
    "Patron Silver Tequila 35cl": 2,
    "Avga Viologika Medium 12 Tem OFFER!!": 3
}
Value: 77.26
Thank you for choosing us!
***09/06/2021 09: 16: 55***



->Στην περίπτωση που δεν έχουμε δώσει int ή 16ψηφιο int σαν "card_no" τότε
  μας επιστρέφει "You have to enter a 16-digit number" (status=500)
->Στην περίπτωση που το καλάθι είναι άδειο
  μας επιστρέφει "Cart is empty." (status=500)
->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
########################
## 11 ORDERS HISTORY ###
########################
Request:
Type: GET
Url : http://0.0.0.0:5000/getOrders
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20

Response:
You have placed 2 orders.
Details: [
    {
        "Fresko Gala Elafry 1,5% Lipara 1 lt, OLYMPOS": 1,
        "Αυγά Βιολογικά Medium 6 Τεμ OFFER!!": 1
    },
    {
        "Patron Silver Tequila 35cl": 2,
        "Avga Viologika Medium 12 Tem OFFER!!": 3
    }
]

->Στην περίπτωση που δεν έχουμε κάνει καμία παραγγελία δηλ. orderHistory == 0
  μας επιστρέφει "You have to place an order first" (status=500)
->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
</br>
<pre>
########################
## 12 DELETE ACCOUNT ###
########################
Request:
Type: DELETE
Url : http://0.0.0.0:5000/deleteAccount	
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20

Response:
You are logged out.
And your account has been removed.

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key
</pre>
