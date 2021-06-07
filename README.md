1η Εργασία στο μάθημα (ΨΣ-512) - Πληροφοριακά Συστήματα<br/>
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
#########################
###### 1 REGISTER #######
#########################
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
####### 2 LOGIN ##########
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


##########################
##### 3 GET STUDENT ######
##########################
Request:
Type: GET
Url : http://0.0.0.0:5000/getstudent
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body:
{"email":"danasilva@ontagene.com"}

Response:
Student found: {
    "_id": "5e99cffd7a781a4aac69daaa",
    "yearOfBirth": 1999,
    "name": "Dana Silva",
    "email": "danasilva@ontagene.com"
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν το email δεν υπάρχει τότε
  "No student found with the email given" (status=500)


--------------------------------


##########################################
# 4 RETURN STUDENTS WHO ARE 30 YEARS OLD #
##########################################
Request:
Type: GET
Url : http://0.0.0.0:5000/getstudents/thirties
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20

Response:
Found 2 students with age 30 : [
    {
        "_id": null,
        "yearOfBirth": 1991,
        "name": "Browning Rasmussen",
        "address": [
            {
                "city": "Cuylerville",
                "street": "Doone Court",
                "postcode": 17331
            }
        ],
        "email": "browningrasmussen@ontagene.com"
    },
    {
        "gender": "male",
        "_id": null,
        "yearOfBirth": 1991,
        "name": "Bennett Baker",
        "email": "bennettbaker@ontagene.com"
    }
]


->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν δεν βρεθουν φοιτητες τότε
  "No students found with age 30" (status=500)



--------------------------------


###################################################
# 5 RETURN STUDENTS WHO ARE AT LEAST 30 YEARS OLD #
###################################################
Request:
Type: GET
Url : http://0.0.0.0:5000/getstudents/oldies
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20

Response:
Found 44 students with age at least 30 : [......]

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν δεν βρεθουν φοιτητες τότε
  "No students found with age at least 30" (status=500)


--------------------------------


#####################################
# 6 RETURN STUDENT ADDRESS BY EMAIL #
#####################################
Request:
Type: GET
Url : http://0.0.0.0:5000/getstudentaddress
Headers:
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body: 
{ "email":"danasilva@ontagene.com" }

Response:
Here is the student's address: {
    "street": "Lafayette Avenue",
    "name": "Dana Silva",
    "postcode": 11573
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν υπαρχει email αλλά όχι address τότε:
  "The student has not an address" (status=500)
->Αν δεν υπαρχει το email τότε
  "Email dosent exists in DB" (status=500)


--------------------------------


#############################
###### 7 DELETE STUDENT #####
#############################
Request:
Type: DELETE
Url : http://0.0.0.0:5000/deletestudent
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body: 
{ "email":"spencercannon@ontagene.com" }

Response:
Student with name: Spencer Cannon, was deleted.

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν δεν υπαρχει το email τότε
  "Student with email: spencercannon@ontagene.com, dosen't exists in DB." (status=500)


--------------------------------


######################################
##### 8 INSERT STUDENT'S COURSES #####
######################################
Request:
Type: PATCH
Url : http://0.0.0.0:5000/addcourse
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body: 
{
    "email": "gillharmon@ontagene.com",
    "courses": [
        {"InfoSys":"10"}, 
        {"Analisi 1":"0"}, 
        {"Analisi 2":"0"}
    ]
} 

Response:
Student's courses updated: {
    "courses": [
        {
            "InfoSys": "10"
        },
        {
            "Analisi 1": "5"
        },
        {
            "Analisi 2": "0"
        }
    ],
    "name": "Gill Harmon",
    "email": "gillharmon@ontagene.com"
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν δεν υπαρχει το email τότε
  "Email dosen't exists in DB" (status=500)


--------------------------------


################################
##### 9 GET PASSED COURSES #####
################################
Request:
Type: GET
Url : http://0.0.0.0:5000/getpassedcourses
	key  : authorization
	value: 6726435c-b57b-11eb-8fab-000c29b50a20
Body: 
{ "email": "gillharmon@ontagene.com" } 

Response:
Gill Harmon has passed 2 courses. Here are the courses: {
    "InfoSys": 10,
    "Analisi 1": 5
}

->Στην περίπτωση που κάποιο απο τo uuid δεν υπάρχει στην λίστα τότε
  μας επιστρέφρει "You don't have authorization, get out!" (status=401)
->Αν δεν υπαρχει το email ή δεν έχει courses τότε
  "Email dosen't exists in DB or student hasnt any courses registered" (status=500)
  </pre>
