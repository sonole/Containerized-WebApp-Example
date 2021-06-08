2η Εργασία στο μάθημα (ΨΣ-512) - Πληροφοριακά Συστήματα<br/>
<hr>
Όνομα: Αλέξανδρος Παληάμπελος<br/>
ΑΜ   : Ε16099<br/>
email: alexpap18@gmail.com<br/>
<hr>
Διδάσκοντες εργαστηρίου:<br/>
* Χρυσόστομος Συμβουλίδης, simvoul@unipi.gr<br/>
* Jean-Didier Totow, totow@unipi.gr<br/>
<hr>
Στο αρχείο app.py υλοιποιούνται όλα τα ζητούμενα entrypoints. <br/>
Ενώ το αρχείο prepare_app.py κάνει όλες τις απαραίτητες ενέργειες<br>
ώστε να τρέξει το app.py χωρίς κάποιο πρόβλημα.<br/>
Σημ: θα πρέπει στον ίδιο φάκελο να είναι και το students.json που θα γίνει import απο το prepare_app.py
<hr>

Παρακάτω βρίσκονται τα παραδείγματα εκτελέσεων requests και των απαντησεων που παίρνουμε σε κάθε entrypoint :
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


--------------------------------


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


--------------------------------


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


--------------------------------


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


--------------------------------


########################
### 5 Product Update ###
########################
Request:
Type: PATCH
Url : http://0.0.0.0:5000/productUpdate?name=Αυγά%20Βιολογικά%20Medium%206%20Τεμ%20OFFER!!&price=3.80&stock=5
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003
Body:
{ "_id":"60be81978db7ab143482ccf6" }

Response:
Product's info updated: {
    name": "Αυγά Βιολογικά Medium 6 Τεμ OFFER!!",
    "category": "Dairy Products",
    "stock": 5,
    "description": "Τα «Αυγά Βιολογικής Γεωργίας» από τα ΧΡΥΣΑ ΑΥΓΑ παράγονται από κότες που ζουν ελεύθερες 
    σε εύφορους αγρότοπους και τρέφονται αποκλειστικά και μόνο με τις πιο αγνές, φυτικές τροφές Βιολογικής Γεωργίας.",
    "price": 3.8
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Στην περίπτωση που το _id δεν υπάρχει τότε μας εμφανίζεται:
  Product dosen't exists in DB.

Σημ: Προυποθέτει να έχουμε κάνει login σαν administrator και να έχουμε πάρει το αντίστοιχο auth key


--------------------------------


#####################
### 6 GET PRODUCT ###
#####################
Request:
Type: GET
Url : http://0.0.0.0:5000/getProduct
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003
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


--------------------------------


#####################
### 7 ADD TO CART ###
#####################
Request:
Type: POST
Url : http://0.0.0.0:5000/addToCart
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003
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


--------------------------------


####################
###### 8 CART ######
####################
Request:
Type: GET
Url : http://0.0.0.0:5000/cart
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003

Response:
Here is your cart
{
    "Jose Cuervo Tequila Silver 700ML": 2,
    "Fresko Gala Elafry 1,5% Lipara 1 lt, OLYMPOS": 1,
    "Avga Viologika Medium 6 Tem OFFER!!": 2
}
Total: 54.28

->Στην περίπτωση που δεν έχει μπει κανένα προιόν στο καλάθι τότε
  μας επιστρέφει "First you have to add products to cart." (status=200)
->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key


--------------------------------


########################
## 8 REMOVE FROM CART ##
########################
Request:
Type: DELETE
Url : http://0.0.0.0:5000/removeFromCart/60be81978db7ab143482ccf6
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003

Response:


->
->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)

Σημ: Προυποθέτει να έχουμε κάνει login σαν απλός χρήστης και να έχουμε πάρει το αντίστοιχο auth key

  </pre>
