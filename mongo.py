from pymongo import MongoClient
import mysql.connector
import neo4j

#Criação db e collection MONGO
cliente = MongoClient('mongodb://localhost:27017/')

dados = cliente['SakilaDatabase']

filmsList = dados.films
paymentList = dados.payments

#Criação db e collection NEO4J

# neoClient = neo4j.Connector('http://localhost:7474',('neo4j','neo4j'))

#Acesso db e collection MYSQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "267455A7E6",
    database = "sakila"
)
mycursor = mydb.cursor()
#leitura DB
firstQuery = "SELECT f.title,f.release_year,f.description,c.name AS Category,a.first_name,a.last_name, language.name AS Foreign_language,extra.name AS Original_language FROM film AS f INNER JOIN film_category AS fc ON fc.film_id = f.film_id INNER JOIN category AS c ON c.category_id = fc.category_id INNER JOIN film_actor AS fa ON fa.film_id = f.film_id INNER JOIN actor AS a ON a.actor_id = fa.actor_id INNER JOIN language ON language.language_id = f.language_id LEFT JOIN ( SELECT f.film_id,l.name FROM film AS f INNER JOIN language AS l ON l.language_id = f.original_language_id WHERE f.original_language_id is not null) extra ON f.film_id = extra.film_id"
secondQuery = "SELECT s.store_id, c.first_name AS Costumer_first_name, c.last_name AS Costumer_last_name, p.amount, p.payment_date, st.first_name AS Staff_first_name, st.last_name  AS Staff_last_name FROM store AS s INNER JOIN customer AS c ON s.store_id = s.store_id INNER JOIN payment AS p ON c.customer_id = p.customer_id INNER JOIN staff AS st ON p.staff_id = st.staff_id"
mycursor.execute(firstQuery)
filmRecords = mycursor.fetchall()
mycursor.execute(secondQuery)
storeRecords = mycursor.fetchall()
print(len(filmRecords))
print(len(storeRecords))
myFilmIt = iter(filmRecords)
titleaux = ""
categorys = []
actors = []
while(True):
    try:
        i1 = next(myFilmIt)
    except StopIteration:
        print("first collection done")
        break
    title = i1[0]
    if titleaux == "":
        titleaux = title
    year  = i1[1]
    desc = i1[2]
    language = i1[6]
    orig_language = i1[7]
    # category and actors
    if titleaux == title:
        if i1[3] not in categorys :
            categorys.append(i1[3])
        actors.append(i1[4] + " " + i1[5])
    else:
        info = { "title" : title, "release_year" : year, "descrição" : desc, "original_language" : orig_language, "foreign_language" : language, "categorys" :  categorys, "actors" : actors}
        filmsList.insert_one(info)
myStoreIt = iter(storeRecords)
while(True):
    try:
        i2 = next(myStoreIt)
    except StopIteration:
        print("second collection done")
        break
    costumer = i2[1] + " " + i2[2]
    staff = i2[5] + " " + i2[6]
    date = i2[4]
    amount = float(i2[3])
    store = i2[0]
    storeinfo = {"store_id" : store, "customer" : costumer, "date" : date, "amount" : amount, "staff" : staff}
    paymentList.insert_one(storeinfo)





