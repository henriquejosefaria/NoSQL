from pymongo import MongoClient
import mysql.connector
#import neo4j
import cx_Oracle

#Criacao da coneccao Oracle
con = cx_Oracle.connect("hr", "oracle", "127.0.0.1/orcl")
print(con.version)
print("Connected to oracle")

oracleCursor = con.cursor()

#Criacao db e collection MONGO
cliente = MongoClient('mongodb://localhost:27017/')

dados = cliente['SakilaDatabase']

filmsList = dados.films
paymentList = dados.payments

#Criacao db e collection NEO4J

# neoClient = neo4j.Connector('http://localhost:7474',('neo4j','neo4j'))

#Acesso db e collection MYSQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "267455A7E6",
    database = "sakila"
)
mycursor = mydb.cursor()

#Oracle DataBase Creation

oracle_city_sql = "SELECT * FROM city"
oracle_city = mycursor.execute(oracle_city_sql)
sql_city = "CREATE TABLE city ( city_id number(10) NOT NULL, city varchar2(50) NOT NULL, country_id number(10), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_city)
for row in oracle_city.fetchall():
    sql = 'insert into city(city_id, city, country_id, last_update)' + 'values(:' +row[city_id]+',:'+row[city]+',:'+row[country_id]+',:'+row[last_update]+'));'
    mycursor.execute(sql)

oracle_customer_sql = "SELECT * FROM customer"
oracle_customer = mycursor.execute(oracle_customer_sql)
sql_costumer = "CREATE TABLE costumer ( customer_id number(10) NOT NULL, store_id number(10) NOT NULL,first_name varchar2(50) NOT NULL,last_name varchar2(50) NOT NULL,email varchar2(100) NOT NULL,address_id number(10) NOT NULL,active BOOLEAN,create_date DATETIME,last_update TIMESTAMP(3));"
oracleCursor.execute(sql_costumer)
for row in oracle_costumer.fetchall():
    sql = 'insert into costumer(customer_id, store_id, first_name, last_name, email,address_id,active,create_date,last_update)' + 'values(:' + row[customer_id]+',:' + row[store_id]+',:'+ row[first_name]+',:' +row[last_name]+',:' +row[email]+',:'+row[address_id]+',:'+row[active]+',:'+row[create_date]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_country_sql = "SELECT * FROM country"
oracle_country = mycursor.execute(oracle_country_sql)
sql_country = "CREATE TABLE country ( country_id number(10) NOT NULL, country varchar2(50) NOT NULL,last_update TIMESTAMP(3));"
oracleCursor.execute(sql_country)
for row in oracle_country.fetchall():
    sql = 'insert into country(country_id, country, last_update)' + 'values(:' +row[country_id]+',:'+row[country]+',:'+row[last_update]+'));'
    mycursor.execute(sql)

oracle_address_sql = "SELECT * FROM address"
oracle_address = mycursor.execute(oracle_address_sql)
sql_address = "CREATE TABLE address ( address_id number(10) NOT NULL, address varchar2(50) NOT NULL, address2 varchar2(50) NOT NULL, district varchar2(50) NOT NULL,city_id number(10) NOT NULL, postal_code varchar2(10),phone varchar2(20), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_address)
for row in oracle_address.fetchall():
    sql = 'insert into address(address_id, address, address2, district,city_id,postal_code,phone,last_update)' + 'values(:' +row[address_id]+',:'+ row[address]+',:'+ row[address2]+',:'+ row[district]+',:'+row[city_id]+',:'+row[postal_code]+',:'+row[phone]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_store_sql = "SELECT * FROM store"
oracle_store = mycursor.execute(oracle_store_sql)
sql_store = "CREATE TABLE store ( store_id number(10) NOT NULL, manager_id number(10) NOT NULL, address_id number(10) NOT NULL, last_update TIMESTAMP(3));"
oracleCursor.execute(sql_store)
for row in oracle_store.fetchall():
    sql = 'insert into store(city_id, city, country_id, last_update)' + 'values(:' +row[city_id]+',:'+row[city]+',:'+row[country_id]+',:'+row[last_update]+'));'
    mycursor.execute(sql)

oracle_staff_sql = "SELECT * FROM staff"
oracle_staff = mycursor.execute(oracle_staff_sql)
sql_staff = "CREATE TABLE staff ( staff_id number(10) NOT NULL, first_name varchar2(50) NOT NULL, last_name varchar2(50) NOT NULL, address_id number(10) NOT NULL, picture BLOB, email varchar2(100), store_id number(10) NOT NULL, active BOOLEAN, username varchar2(16) NOT NULL, password VARBINARY (40), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_staff)
for row in oracle_staff.fetchall():
    sql = 'insert into staff(staff_id, first_name, last_name, address_id, picture,email,store_id,active,username,password,last_update)' + 'values(:' +row[staff_id]+',:' +row[first_name]+',:' +row[last_name]+',:' +row[address_id]+',:' +row[picture]+',:'+row[email]+',:'+row[store_id]+',:'+row[active]+',:'+row[username]+',:'+row[password]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_payment_sql = "SELECT * FROM payment"
oracle_payment = mycursor.execute(oracle_payment_sql)
sql_payment = "CREATE TABLE payment ( payment_id number(10) NOT NULL, customer_id number(10) NOT NULL, staff_id number(10) NOT NULL, rental_id number(10) NOT NULL, amount FLOAT(2), payment_date DATE, last_update TIMESTAMP(3));"
oracleCursor.execute(sql_payment)
for row in oracle_payment.fetchall():
    sql = 'insert into payment(payment_id, customer_id, staff_id,rental_id,amount,payment_date,last_update)' + 'values(:' +row[payment_id]+',:' +row[customer_id]+',:' +row[staff_id]+',:'+row[rental_id]+',:'+row[amount]+',:'+row[payment_date]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_rental_sql = "SELECT * FROM rental"
oracle_rental = mycursor.execute(oracle_rental_sql)
sql_rental = "CREATE TABLE rental ( rental_id number(10) NOT NULL, rental_date DATE, inventory_id number(10) NOT NULL, customer_id number(10) NOT NULL, return_date DATE, staff_id number(10) NOT NULL, last_update TIMESTAMP(3));"
oracleCursor.execute(sql_rental)
for row in oracle_rental.fetchall():
    sql = 'insert into rental(rental_id, rental_date, inventory_id,customer_id,return_date,staff_id, last_update)' + 'values(:' +row[rental_id]+',:' +row[rental_date]+',:' +row[inventory_id]+',:'+row[customer_id]+',:'+row[return_date]+',:'+row[staff_id]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_film_sql = "SELECT * FROM film"
oracle_film = mycursor.execute(oracle_film_sql)
sql_film = "CREATE TABLE film ( film_id number(10) NOT NULL, title varchar2(255), description NCLOB, release_year number(5), language_id number(10) NOT NULL, original_language_id number(10), rental_duration number(10) NOT NULL, rental_rate FLOAT(2), length number(10), replacement_cost FLOAT(2), rating varchar2(10), special_features varchar2(100), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_film)
for row in oracle_film.fetchall():
    sql = 'insert into film(film_id, title, description,release_year,language_id, original_language_id,rental_duration,rental_date,length, replacement_cost,rating,special_features,last_update)' + 'values(:' +row[film_id]+',:'+ row[title]+',:'+ row[description]+',:'+row[release_year]+',:'+row[language_id]+',:'+ row[original_language_id]+',:'+row[rental_duration]+',:'+row[rental_date]+',:'+row[length]+',:'+ row[replacement_cost]+',:'+row[rating]+',:'+row[special_features]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_category_sql = "SELECT * FROM category"
oracle_category = mycursor.execute(oracle_category_sql)
sql_category = "CREATE TABLE category ( category_id number(10) NOT NULL, name varchar2(25), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_category)
for row in oracle_category.fetchall():
    sql = 'insert into category(category_id, name, last_update)' + 'values(:' +row[category_id]+',:'+row[name]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_language_sql = "SELECT * FROM language"
oracle_language = mycursor.execute(oracle_language_sql)
sql_language = "CREATE TABLE language ( language_id number(10) NOT NULL, name varchar(20), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_language)
for row in oracle_language.fetchall():
    sql = 'insert into language(language_id, name, last_update)' + 'values(:' +row[language_id]+',:'+ row[name]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_actor_sql = "SELECT * FROM actor"
oracle_actor = mycursor.execute(oracle_actor_sql)
sql_actor = "CREATE TABLE actor ( actor_id number(10) NOT NULL, first_name varchar2(45), last_name varchar2(45), last_update TIMESTAMP(3));"
oracleCursor.execute(sql_actor)
for row in oracle_actor.fetchall():
    sql = 'insert into actor(actor_id, first_name, last_name, last_update)' + 'values(:' +row[actor_id]+',:' +row[first_name]+',:' +row[last_name]+',:'+row[last_update]+');'
    mycursor.execute(sql)


oracle_inventory_sql = "SELECT * FROM inventory"
oracle_inventory = mycursor.execute(oracle_inventory_sql)
sql_inventory = "CREATE TABLE inventory ( inventory_id number(10) NOT NULL, film_id number(10) NOT NULL, store_id number(10) NOT NULL, last_update TIMESTAMP(3));"
oracleCursor.execute(sql_inventory)
for row in oracle_inventory.fetchall():
    sql = 'insert into inventory(inventory_id, film_id, store_id, last_update)' + 'values(:' +row[inventory_id]+',:'+row[film_id]+',:'+row[store_id]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_film_text_sql = "SELECT * FROM film_text"
oracle_film_text = mycursor.execute(oracle_film_text_sql)
sql_film_text = "CREATE TABLE film_text ( film_id number(10) NOT NULL,title varchar(255),description NCLOB);"
oracleCursor.execute(sql_film_text)
for row in oracle_film_text.fetchall():
    sql = 'insert into film_text(film_id, title, description)' + 'values(:' +row[film_id]+',:' +row[title]+',:' +row[description]+');'
    mycursor.execute(sql)

oracle_film_actor_sql = "SELECT * FROM film_actor"
oracle_film_actor = mycursor.execute(oracle_film_actor_sql)
sql_film_actor = "CREATE TABLE film_actor ( actor_id number(10) NOT NULL, film_id number(10) NOT NULL, last_update TIMESTAMP(3));"
oracleCursor.execute(sql_film_actor)
for row in oracle_film_actor.fetchall():
    sql = 'insert into film_actor(actor_id, film_id, last_update)' + 'values(:' +row[actor_id]+',:'+row[film_id]+',:'+row[last_update]+');'
    mycursor.execute(sql)

oracle_film_category_sql = "SELECT * FROM film_category"
oracle_film_category = mycursor.execute(oracle_film_category_sql)
sql_film_category = "CREATE TABLE film_category ( film_id number(10) NOT NULL, category_id number(10) NOT NULL, last_update TIMESTAMP(3));"
oracleCursor.execute(sql_film_category)
for row in oracle_film_category.fetchall():
    sql = 'insert into film_category(film_id, category_id, last_update)' + 'values(:' +row[film_id]+',:'+row[category_id]+',:'+row[last_update]+');'
    mycursor.execute(sql)




#leitura DB
firstQuery = "SELECT f.title,f.release_year,f.description,c.name AS Category,a.first_name,a.last_name, language.name AS Foreign_language,extra.name AS Original_language,f.film_id FROM film AS f LEFT JOIN film_category AS fc ON fc.film_id = f.film_id LEFT JOIN category AS c ON c.category_id = fc.category_id LEFT JOIN film_actor AS fa ON fa.film_id = f.film_id LEFT JOIN actor AS a ON a.actor_id = fa.actor_id LEFT JOIN language ON language.language_id = f.language_id LEFT JOIN ( SELECT f.film_id,l.name FROM film AS f LEFT JOIN language AS l ON l.language_id = f.original_language_id WHERE f.original_language_id is not null) extra ON f.film_id = extra.film_id"
secondQuery = "SELECT s.store_id, c.first_name AS Costumer_first_name, c.last_name AS Costumer_last_name, p.amount, p.payment_date, st.first_name AS Staff_first_name, st.last_name  AS Staff_last_name FROM store AS s LEFT JOIN customer AS c ON s.store_id = s.store_id LEFT JOIN payment AS p ON c.customer_id = p.customer_id LEFT JOIN staff AS st ON p.staff_id = st.staff_id"
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
while(True):
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
        info = { "id": i1aux[8], "title" : i1aux[0], "release_year" : i1aux[1], "descrição" : i1aux[2], "original_language" : i1aux[7], "foreign_language" : i1aux[6], "categorys" :  categorys, "actors" : actors}
        filmsList.insert_one(info)
        actors.clear()
        categorys.clear()
    i1aux = i1

info = {"id": i1aux[8], "title": i1aux[0], "release_year": i1aux[1], "descrição": i1aux[2], "original_language": i1aux[7],"foreign_language": i1aux[6], "categorys": categorys, "actors": actors}
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
while(True):
    query1Mongo = filmsList.find({}, {"title": 1, "original_language": 1, "foreign_language": 1, "_id": 0})
    [print(queryMongo) for queryMongo in query1Mongo]
    break





