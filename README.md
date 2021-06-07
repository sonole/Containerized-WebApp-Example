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
    "description": "Μια πραγματικά ασημένια τεκίλα, η Cuervo® Silver είναι η επιτομή της απαλότητας. Οι κύριοι αποσταγματοποιητές στην La Rojeña δημιούργησαν αυτό το μοναδικό 			    και ισορροπημένο μείγμα για να αναδείξει τις αποχρώσεις της αγαύης, καραμέλας, και φρέσκων μυρωδικών στο προφίλ της γεύσης της.",
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
Url : http://0.0.0.0:5000/productUpdate?name=Avga Large 6 Temaxia&price=3.80&stock=5
Headers:
	key  : authorization
	value: 877e8546-c77e-11eb-8996-0242c0a83003
Body:
{ "_id":"60be81978db7ab143482ccf6" }

Response:
Product's info updated: {
    "name": "Avga Large 6 Temaxia",
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
  </pre>
