from pymongo import MongoClient
import mysql.connector

# Criacao db e collection MONGO
cliente = MongoClient('mongodb://localhost:27017/')

dados = cliente['SakilaDatabase']

filmsList = dados.films
paymentList = dados.payments

# Acesso db e collection MYSQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pass",
    database="sakila"
)
mycursor = mydb.cursor()



# leitura DB
firstQuery = "SELECT f.title,f.release_year,f.description,c.name AS Category,a.first_name,a.last_name, language.name AS Foreign_language,extra.name AS Original_language,f.film_id FROM film AS f LEFT JOIN film_category AS fc ON fc.film_id = f.film_id LEFT JOIN category AS c ON c.category_id = fc.category_id LEFT JOIN film_actor AS fa ON fa.film_id = f.film_id LEFT JOIN actor AS a ON a.actor_id = fa.actor_id LEFT JOIN language ON language.language_id = f.language_id LEFT JOIN ( SELECT f.film_id,l.name FROM film AS f LEFT JOIN language AS l ON l.language_id = f.original_language_id WHERE f.original_language_id is not null) extra ON f.film_id = extra.film_id"

secondQuery = "SELECT s.store_id, c.first_name AS Costumer_first_name, c.last_name AS Costumer_last_name, p.amount, p.payment_date, st.first_name AS Staff_first_name, st.last_name  AS Staff_last_name,s.manager_staff_id,st.staff_id,st.email,p.payment_id,c.customer_id,c.email FROM store AS s LEFT JOIN customer AS c ON s.store_id = s.store_id LEFT JOIN payment AS p ON c.customer_id = p.customer_id LEFT JOIN staff AS st ON p.staff_id = st.staff_id"
mycursor.execute(firstQuery)
filmRecords = mycursor.fetchall()
mycursor.execute(secondQuery)
storeRecords = mycursor.fetchall()
myFilmIt = iter(filmRecords)
i1aux = None
categorys = []
actors = []
filmsList.drop()
paymentList.drop()
while (True):
    try:
        i1 = next(myFilmIt)
    except StopIteration:
        print("first collection done")
        break
    if i1aux == None:
        i1aux = i1
    # category and actors
    if i1aux[0] == i1[0]:
        actors.append(i1[4] + " " + i1[5])
        if i1[3] not in categorys:
            categorys.append(i1[3])
    else:
        info = {"id": i1aux[8], "title": i1aux[0], "release_year": i1aux[1], "descrição": i1aux[2],
                "original_language": i1aux[7], "foreign_language": i1aux[6], "categorys": categorys, "actors": actors}
        filmsList.insert_one(info)
        actors.clear()
        categorys.clear()
    i1aux = i1

info = {"id": i1aux[8], "title": i1aux[0], "release_year": i1aux[1], "descrição": i1aux[2],
        "original_language": i1aux[7], "foreign_language": i1aux[6], "categorys": categorys, "actors": actors}
filmsList.insert_one(info)

myStoreIt = iter(storeRecords)
while (True):
    try:
        i2 = next(myStoreIt)
    except StopIteration:
        print("second collection done")
        break
    
    costumer = i2[1] + " " + i2[2]
    costumer_id = i2[11]
    costumer_email = i2[12]
    manager_staff_id = i2[7]
    staff = i2[5] + " " + i2[6]
    staff_id = i2[8]
    staff_email = i2[9]
    date = i2[4]
    amount = float(i2[3])
    payment_id = i2[10]
    store = i2[0]
    
    storeInfo = {"store_id" : store, "manager_id" : manager_staff_id}
    paymentStaffInfo = {"staff_id" : staff_id, "name": staff, "email" : staff_email,"payment_id": payment_id,"amount" : amount,"date": date}
    customerInfo = {"customer_id": costumer_id,"name": costumer,"email": costumer_email}
    res = paymentList.find_one({"store_id": store})
    
    if res == None:
        paymentList.insert_one(storeInfo)
    res = paymentList.find_one({"paymentsByCostumer.customer_id": costumer_id,"store_id": store})
    if res == None:
        paymentList.update({"store_id": store},{ "$push": { "paymentsByCostumer" : customerInfo}})
    res = paymentList.find_one({"store_id": store,"paymentsByCostumer.customer_id": costumer_id,"paymentsByCostumer.payments.payment_id": payment_id,"paymentsByCostumer.payments.staff_id": staff_id})
    if res == None:
        res = paymentList.aggregate([{"$match":{"store_id": store,"paymentsByCostumer.customer_id": costumer_id}},{ "$project" : { "index" : { "$indexOfArray": ["$paymentsByCostumer.customer_id",costumer_id]}}}])
        ress = list(res)   
        query = "paymentsByCostumer."+ str(ress[0]["index"]) +".payments"
        paymentList.update({"store_id": store,"paymentsByCostumer.customer_id": costumer_id},{ "$push": {query : paymentStaffInfo }})
        
