import mysql.connector
# import neo4j
import cx_Oracle

# Criacao da coneccao Oracle
con = cx_Oracle.connect("hr", "oracle", "127.0.0.1/orcl")
print(con.version)
print("Connected to oracle")


oracleCursor = con.cursor()

# Acesso db e collection MYSQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="267455A7E6",
    database="sakila"
)
mycursor = mydb.cursor()

# Oracle DataBase Creation


sqlDropCountry = "DROP TABLE COUNTRY"
sqlDropCategory = "DROP TABLE CATEGORY"
sqlDropLanguage = "DROP TABLE LANGUAGE"
sqlDropActor = "DROP TABLE ACTOR"
sqlDropCity = "DROP TABLE CITY"
sqlDropAddress = "DROP TABLE ADDRESS"
sqlDropStore = "DROP TABLE STORE"
sqlDropStaff = "DROP TABLE STAFF"
sqlDropCustomer = "DROP TABLE CUSTOMER"
sqlDropPayment = "DROP TABLE PAYMENT"
sqlDropRental = "DROP TABLE RENTAL"
sqlDropFilm = "DROP TABLE FILM"
sqlDropInventory = "DROP TABLE INVENTORY"
sqlDropFilmText = "DROP TABLE FILM_TEXT"
sqlDropFilmActor = "DROP TABLE FILM_ACTOR"
sqlDropFilmCategory = "DROP TABLE FILM_CATEGORY"


oracleCursor.execute(sqlDropPayment)
oracleCursor.execute(sqlDropRental)
oracleCursor.execute(sqlDropInventory)
oracleCursor.execute(sqlDropFilmText)
oracleCursor.execute(sqlDropFilmCategory)
oracleCursor.execute(sqlDropFilmActor)
oracleCursor.execute(sqlDropFilm)
oracleCursor.execute(sqlDropLanguage)
oracleCursor.execute(sqlDropCustomer)
oracleCursor.execute("ALTER TABLE STAFF DROP CONSTRAINT FK_STORE2")
oracleCursor.execute(sqlDropStore)
oracleCursor.execute(sqlDropStaff)
oracleCursor.execute(sqlDropCategory)
oracleCursor.execute(sqlDropAddress)
oracleCursor.execute(sqlDropCity)
oracleCursor.execute(sqlDropCountry)
oracleCursor.execute(sqlDropActor)
print("ORACLE DATABASE IS STARTING NOW:\n\n")

# ###################### ACTOR ########################### #

sqlActor = "CREATE TABLE ACTOR" \
           " (ACTOR_ID    NUMBER(10)   NOT NULL, " \
           "  FIRST_NAME  VARCHAR2(45) NOT NULL, " \
           "  LAST_NAME   VARCHAR2(45) NOT NULL, " \
           "  LAST_UPDATE TIMESTAMP    NOT NULL, " \
           "  CONSTRAINT PK_ACTOR PRIMARY KEY (ACTOR_ID))"
oracleCursor.execute(sqlActor)
con.commit()
print("Table ACTOR done!!")

# ###################### COUNTRY ########################### #

sqlCountry = "CREATE TABLE COUNTRY" \
             "(COUNTRY_ID   NUMBER(10)   NOT NULL , " \
             " COUNTRY      VARCHAR2(50) NOT NULL , " \
             " LAST_UPDATE  TIMESTAMP    NOT NULL , " \
             " CONSTRAINT PK_COUNTRY PRIMARY KEY (COUNTRY_ID))"
oracleCursor.execute(sqlCountry)
con.commit()
print("Table COUNTRY done!!")

# ###################### CITY ########################### #

sqlCity = "CREATE TABLE CITY" \
          "(CITY_ID      NUMBER(10)      NOT NULL   , " \
          " CITY         VARCHAR2(50)    NOT NULL   , " \
          " COUNTRY_ID   NUMBER(10)      NOT NULL   , " \
          " LAST_UPDATE  TIMESTAMP       NOT NULL   , " \
          " CONSTRAINT PK_CITY PRIMARY KEY (CITY_ID), " \
          " CONSTRAINT FK_COUNTRY" \
          "    FOREIGN KEY (COUNTRY_ID)" \
          "    REFERENCES COUNTRY(COUNTRY_ID))"
# Apaga tabela CITY
# Cria tabela CITY
oracleCursor.execute(sqlCity)
con.commit()
print("Table CITY done!!")

# ###################### ADDRESS ########################### #

sqlAddress = "CREATE TABLE ADDRESS" \
             "( ADDRESS_ID  NUMBER(10)   NOT NULL , " \
             "  ADDRESS     VARCHAR2(50) NOT NULL , " \
             "  ADDRESS2    VARCHAR2(50) NULL , " \
             "  DISTRICT    VARCHAR2(50) NULL , " \
             "  CITY_ID     NUMBER(10)   NOT NULL , " \
             "  POSTAL_CODE VARCHAR2(10) NULL , " \
             "  PHONE       VARCHAR2(20) NULL , " \
             "  LAST_UPDATE TIMESTAMP    NOT NULL , " \
             "  CONSTRAINT PK_ADDRESS PRIMARY KEY (ADDRESS_ID), " \
             "  CONSTRAINT FK_CITY" \
             "     FOREIGN KEY (CITY_ID)" \
             "     REFERENCES CITY(CITY_ID))"
oracleCursor.execute(sqlAddress)
con.commit()
print("Table ADDRESS done!!")

# ###################### CATEGORY ########################### #

sqlCategory = "CREATE TABLE CATEGORY " \
              " (CATEGORY_ID NUMBER(10)   NOT NULL, " \
              "  NAME        VARCHAR2(25) NOT NULL, " \
              "  LAST_UPDATE TIMESTAMP    NOT NULL, " \
              "  CONSTRAINT PK_CATEGORY PRIMARY KEY (CATEGORY_ID))"
oracleCursor.execute(sqlCategory)
con.commit()
print("Table CATEGORY done!!")

# ###################### STAFF ########################### #

sqlStaff = "CREATE TABLE STAFF" \
           " (STAFF_ID    NUMBER(10)    NOT NULL, " \
           "  FIRST_NAME  VARCHAR2(50)  NOT NULL, " \
           "  LAST_NAME   VARCHAR2(50)  NOT NULL, " \
           "  ADDRESS_ID  NUMBER(10)    NOT NULL, " \
           "  PICTURE     BLOB          NULL, " \
           "  EMAIL       VARCHAR2(100) NULL, " \
           "  STORE_ID    NUMBER(10)    NOT NULL, " \
           "  ACTIVE      NUMBER(1,0)   NOT NULL, " \
           "  USERNAME    VARCHAR2(16)  NOT NULL, " \
           "  PASSWORD    VARCHAR2(50)  NULL, " \
           "  LAST_UPDATE TIMESTAMP     NOT NULL, " \
           "  CONSTRAINT PK_STAFF PRIMARY KEY (STAFF_ID), " \
           "  CONSTRAINT FK_ADDRESS2" \
           "     FOREIGN KEY (ADDRESS_ID)" \
           "     REFERENCES ADDRESS(ADDRESS_ID))"
oracleCursor.execute(sqlStaff)
con.commit()
print("Table STAFF done!!")

# ###################### STORE ########################### #

sqlStore = "CREATE TABLE STORE" \
           "(STORE_ID   NUMBER(10) NOT NULL," \
           " MANAGER_ID  NUMBER(10) NOT NULL," \
           " ADDRESS_ID  NUMBER(10) NOT NULL," \
           " LAST_UPDATE TIMESTAMP  NOT NULL," \
           "CONSTRAINT PK_STORE PRIMARY KEY (STORE_ID)," \
           "  CONSTRAINT FK_MANAGER" \
           "     FOREIGN KEY (MANAGER_ID)" \
           "     REFERENCES STAFF(STAFF_ID)," \
           "  CONSTRAINT FK_ADDRESS" \
           "     FOREIGN KEY (ADDRESS_ID)" \
           "     REFERENCES ADDRESS(ADDRESS_ID))"
oracleCursor.execute(sqlStore)
con.commit()
print("Table STORE done!!")

# ###################### CUSTOMER ########################### #

sqlCustomer = "CREATE TABLE CUSTOMER" \
              "(CUSTOMER_ID NUMBER(10)    NOT NULL , " \
              " STORE_ID    NUMBER(10)    NOT NULL , " \
              " FIRST_NAME  VARCHAR2(50)  NOT NULL , " \
              " LAST_NAME   VARCHAR2(50)  NOT NULL , " \
              " EMAIL       VARCHAR2(100) NOT NULL , " \
              " ADDRESS_ID  NUMBER(10)    NOT NULL , " \
              " ACTIVE      NUMBER(1)     NOT NULL , " \
              " CREATE_DATA DATE          NOT NULL , " \
              " LAST_UPDATE TIMESTAMP     NOT NULL , " \
              " CONSTRAINT PK_CUSTOMER PRIMARY KEY (CUSTOMER_ID)," \
              " CONSTRAINT FK_STORE" \
              "    FOREIGN KEY (STORE_ID)" \
              "    REFERENCES STORE(STORE_ID)," \
              " CONSTRAINT FK_ADDRESS3" \
              "    FOREIGN KEY (ADDRESS_ID)" \
              "    REFERENCES ADDRESS(ADDRESS_ID))"
oracleCursor.execute(sqlCustomer)
con.commit()
print("Table CUSTOMER done!!")

# ###################### LANGUAGE ########################### #

sqlLanguage = "CREATE TABLE LANGUAGE " \
              " (LANGUAGE_ID NUMBER(10)   NOT NULL, " \
              "  NAME        VARCHAR2(20) NOT NULL, " \
              "  LAST_UPDATE TIMESTAMP    NOT NULL, " \
              "  CONSTRAINT PK_LANGUAGE PRIMARY KEY (LANGUAGE_ID))"
oracleCursor.execute(sqlLanguage)
con.commit()
print("Table LANGUAGE done!!")

# ###################### FILM ########################### #

sqlFilm = "CREATE TABLE FILM" \
          " (FILM_ID              NUMBER(10)    NOT NULL, " \
          "  TITLE                VARCHAR2(255) NOT NULL, " \
          "  DESCRIPTION          VARCHAR(255)  NULL, " \
          "  RELEASE_YEAR         NUMBER(10)    NULL, " \
          "  LANGUAGE_ID          NUMBER(10)    NOT NULL, " \
          "  ORIGINAL_LANGUAGE_ID NUMBER(10)    NULL, " \
          "  RENTAL_DURATION      NUMBER(10)    NOT NULL, " \
          "  RENTAL_DATE          NUMERIC(6, 2) NOT NULL, " \
          "  LENGTH               NUMBER(10)    NULL, " \
          "  REPLACEMENT_COST     NUMERIC(6, 2) NOT NULL, " \
          "  RATING               VARCHAR(15)   NULL, " \
          "  SPECIAL_FEATURES     VARCHAR2(255) NULL, " \
          "  LAST_UPDATE          TIMESTAMP     NOT NULL, " \
          "  CONSTRAINT PK_FILM PRIMARY KEY (FILM_ID)," \
          "  CONSTRAINT FK_LANGUAGE" \
          "     FOREIGN KEY (LANGUAGE_ID)" \
          "     REFERENCES LANGUAGE(LANGUAGE_ID)," \
          "  CONSTRAINT FK_LANGUAGE2" \
          "     FOREIGN KEY (ORIGINAL_LANGUAGE_ID)" \
          "     REFERENCES LANGUAGE(LANGUAGE_ID))"
oracleCursor.execute(sqlFilm)
con.commit()
print("Table FILM done!!")

# ###################### FILM_ACTOR ########################### #

sqlFilmActor = "CREATE TABLE FILM_ACTOR" \
               " (ACTOR_ID    NUMBER(10) NOT NULL, " \
               "  FILM_ID     NUMBER(10) NOT NULL, " \
               "  LAST_UPDATE TIMESTAMP  NOT NULL, " \
               "  CONSTRAINT PK_FILM_ACTOR PRIMARY KEY (ACTOR_ID,FILM_ID)," \
               "  CONSTRAINT FK_ACTOR" \
               "     FOREIGN KEY (ACTOR_ID)" \
               "     REFERENCES ACTOR(ACTOR_ID)," \
               "  CONSTRAINT FK_FILM" \
               "     FOREIGN KEY (FILM_ID)" \
               "     REFERENCES FILM(FILM_ID))"
oracleCursor.execute(sqlFilmActor)
con.commit()
print("Table FILM_ACTOR done!!")

# ###################### FILM_CATEGORY ########################### #

sqlFilmCategory = "CREATE TABLE FILM_CATEGORY" \
                  " ( FILM_ID    NUMBER(10) NOT NULL, " \
                  "  CATEGORY_ID NUMBER(10) NOT NULL, " \
                  "  LAST_UPDATE TIMESTAMP  NOT NULL, " \
                  "  CONSTRAINT PK_FILM_CATEGORY PRIMARY KEY (FILM_ID,CATEGORY_ID)," \
                  "  CONSTRAINT FK_FILM2" \
                  "     FOREIGN KEY (FILM_ID)" \
                  "     REFERENCES FILM(FILM_ID)," \
                  "  CONSTRAINT FK_CATEGORY" \
                  "     FOREIGN KEY (CATEGORY_ID)" \
                  "     REFERENCES CATEGORY(CATEGORY_ID))"
oracleCursor.execute(sqlFilmCategory)
con.commit()
print("Table FILM_CATEGORY done!!")

# ###################### FILM_TEXT ########################### #

sqlFilmText = "CREATE TABLE FILM_TEXT" \
              " (FILM_ID     NUMBER(10)   NOT NULL, " \
              "  TITLE       VARCHAR(255) NOT NULL, " \
              "  DESCRIPTION NCLOB        NOT NULL, " \
              "  CONSTRAINT PK_FILM_TEXT PRIMARY KEY (FILM_ID))"
oracleCursor.execute(sqlFilmText)
con.commit()
print("Table FILM_TEXT done!!")

# ###################### INVENTORY ########################### #

sqlInventory = "CREATE TABLE INVENTORY" \
               " (INVENTORY_ID NUMBER(10) NOT NULL, " \
               "  FILM_ID      NUMBER(10) NOT NULL, " \
               "  STORE_ID     NUMBER(10) NOT NULL, " \
               "  LAST_UPDATE  TIMESTAMP  NOT NULL, " \
               "  CONSTRAINT PK_INVENTORY PRIMARY KEY (INVENTORY_ID)," \
               "  CONSTRAINT FK_FILM3" \
               "     FOREIGN KEY (FILM_ID)" \
               "     REFERENCES FILM(FILM_ID)," \
               "  CONSTRAINT FK_STORE3" \
               "     FOREIGN KEY (STORE_ID)" \
               "     REFERENCES STORE(STORE_ID))"
oracleCursor.execute(sqlInventory)
con.commit()
print("Table INVENTORY done!!")

# ###################### RENTAL ########################### #

sqlRental = "CREATE TABLE RENTAL" \
            " (RENTAL_ID    NUMBER(10) NOT NULL, " \
            "  RENTAL_DATE  DATE       NOT NULL, " \
            "  INVENTORY_ID NUMBER(10) NOT NULL, " \
            "  CUSTOMER_ID  NUMBER(10) NOT NULL, " \
            "  RETURN_DATE  DATE       NULL, " \
            "  STAFF_ID     NUMBER(10) NOT NULL, " \
            "  LAST_UPDATE  TIMESTAMP  NOT NULL, " \
            "  CONSTRAINT PK_RENTAL PRIMARY KEY (RENTAL_ID)," \
            "  CONSTRAINT FK_CUSTOMER" \
            "     FOREIGN KEY (CUSTOMER_ID)" \
            "     REFERENCES CUSTOMER(CUSTOMER_ID)," \
            "  CONSTRAINT FK_STAFF" \
            "     FOREIGN KEY (STAFF_ID)" \
            "     REFERENCES STAFF(STAFF_ID)," \
            "  CONSTRAINT FK_INVENTORY" \
            "     FOREIGN KEY (INVENTORY_ID)" \
            "     REFERENCES INVENTORY(INVENTORY_ID))"
oracleCursor.execute(sqlRental)
con.commit()
print("Table RENTAL done!!")

# ###################### PAYMENT ########################### #

sqlPayment = "CREATE TABLE PAYMENT" \
             " (PAYMENT_ID   NUMBER(10) NOT NULL, " \
             "  CUSTOMER_ID  NUMBER(10) NOT NULL, " \
             "  STAFF_ID     NUMBER(10) NOT NULL, " \
             "  RENTAL_ID    NUMBER(10) NULL, " \
             "  AMOUNT       FLOAT(2)   NOT NULL, " \
             "  PAYMENT_DATE DATE       NOT NULL, " \
             "  LAST_UPDATE  TIMESTAMP  NOT NULL, " \
             "  CONSTRAINT PK_PAYMENT PRIMARY KEY (PAYMENT_ID)," \
             "  CONSTRAINT FK_CUSTOMER2" \
             "     FOREIGN KEY (CUSTOMER_ID)" \
             "     REFERENCES CUSTOMER(CUSTOMER_ID)," \
             "  CONSTRAINT FK_STAFF2" \
             "     FOREIGN KEY (STAFF_ID)" \
             "     REFERENCES STAFF(STAFF_ID)," \
             "  CONSTRAINT FK_RENTAL" \
             "     FOREIGN KEY (RENTAL_ID)" \
             "     REFERENCES RENTAL(RENTAL_ID))"
oracleCursor.execute(sqlPayment)
con.commit()
print("Table PAYMENT done!!\n")


# ########################################################## #

# ###################### FILLING ########################### #

# ########################################################## #



# ###################### ACTOR ########################### #

oracle_actor_sql = "SELECT * FROM actor"
mycursor.execute(oracle_actor_sql)
actorRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(actorRows)
oracleCursor.executemany('insert into ACTOR(ACTOR_ID, FIRST_NAME, LAST_NAME,LAST_UPDATE) values(:1,:2,:3,:4)',
                         actorRows)
con.commit()
print("Table ACTOR filled!!")


# ###################### COUNTRY ########################### #
oracle_country_sql = "SELECT * FROM country"
mycursor.execute(oracle_country_sql)
countryRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(countryRows)
oracleCursor.executemany('insert into COUNTRY(COUNTRY_ID, COUNTRY, LAST_UPDATE) values ( :1, :2, :3)', countryRows)
con.commit()
print("Table COUNTRY filled!!")

# ###################### CITY ########################### #
oracle_city_sql = "SELECT * FROM city"
mycursor.execute(oracle_city_sql)
cityRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(cityRows)
oracleCursor.executemany('insert into CITY(CITY_ID, CITY, COUNTRY_ID, LAST_UPDATE) values ( :1, :2, :3, :4)', cityRows)
con.commit()
print("Table CITY filled!!")

# ###################### ADDRESS ########################### #

oracle_address_sql = "SELECT * FROM address"
mycursor.execute(oracle_address_sql)
addressRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(addressRows)
oracleCursor.executemany(
    'insert into ADDRESS(ADDRESS_ID, ADDRESS, ADDRESS2, DISTRICT,CITY_ID,POSTAL_CODE,PHONE,LAST_UPDATE) values(:1,:2,:3,:4,:5,:6,:7,:8)',
    addressRows)
con.commit()
print("Table ADDRESS filled!!")

# ###################### CATEGORY ########################### #
oracle_category_sql = "SELECT * FROM category"
mycursor.execute(oracle_category_sql)
categoryRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(categoryRows)
oracleCursor.executemany('insert into CATEGORY(CATEGORY_ID, NAME,LAST_UPDATE) values(:1,:2,:3)', categoryRows)
con.commit()
print("Table CATEGORY filled!!")


# ###################### STAFF ########################### #

# NOTA: BLOAD NÃO PODE SER CARREGAD PORQUE O PYTHON NÃO AGUENTA #

oracle_staff_sql = "SELECT staff_id,first_name,last_name,address_id,email,store_id,active,username,password,last_update FROM staff"
mycursor.execute(oracle_staff_sql)
staffRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(staffRows)
oracleCursor.executemany('insert into STAFF(STAFF_ID, FIRST_NAME, LAST_NAME, ADDRESS_ID, PICTURE,EMAIL,STORE_ID,ACTIVE,USERNAME,PASSWORD,LAST_UPDATE) values(:1,:2,:3,:4,NULL,:5,:6,:7,:8,:9,:10)', staffRows)
con.commit()
print("Table STAFF filled!!")


# ###################### STORE ########################### #
oracle_store_sql = "SELECT * FROM store"
mycursor.execute(oracle_store_sql)
storeRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(storeRows)
oracleCursor.executemany('insert into STORE(STORE_ID, MANAGER_ID, ADDRESS_ID, LAST_UPDATE) values(:1,:2,:3,:4)',
                         storeRows)
con.commit()
print("Table STORE filled!!")

sqlStaffAlteration = "ALTER TABLE STAFF " \
                     "ADD  CONSTRAINT FK_STORE2" \
                     "     FOREIGN KEY (STORE_ID)" \
                     "     REFERENCES STORE(STORE_ID)"
oracleCursor.execute(sqlStaffAlteration)
con.commit()
print("Table STAFF altered successfully!!")

# ###################### CUSTOMER ########################### #
oracle_customer_sql = "SELECT * FROM customer"
mycursor.execute("SELECT * FROM customer")
customerRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(customerRows)
oracleCursor.executemany(
    'insert into CUSTOMER(CUSTOMER_ID, STORE_ID, FIRST_NAME, LAST_NAME, EMAIL, ADDRESS_ID, ACTIVE, CREATE_DATA, LAST_UPDATE) values ( :1, :2, :3, :4, :5, :6, :7, :8, :9)',
    customerRows)
con.commit()
print("Table CUSTOMER filled!!")


# ###################### LANGUAGE ########################### #

oracle_language_sql = "SELECT * FROM language"
mycursor.execute(oracle_language_sql)
languageRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(languageRows)
oracleCursor.executemany('insert into LANGUAGE(LANGUAGE_ID, NAME,LAST_UPDATE) values(:1,:2,:3)', languageRows)
con.commit()
print("Table LANGUAGE filled!!")


# ###################### FILM ########################### #
oracle_film_sql = "SELECT * FROM film"
mycursor.execute(oracle_film_sql)
filmRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(filmRows)
newfilmRows = []
for row in filmRows:
    string = ' '.join(row[11])
    newRow = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],string,row[12]]
    newfilmRows.append(newRow)
oracleCursor.executemany('insert into FILM(FILM_ID, TITLE, DESCRIPTION, RELEASE_YEAR,LANGUAGE_ID, ORIGINAL_LANGUAGE_ID,RENTAL_DURATION,RENTAL_DATE,LENGTH, REPLACEMENT_COST,RATING,SPECIAL_FEATURES,LAST_UPDATE) values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)',newfilmRows)
con.commit()
print("Table FILM filled!!")

# ###################### FILM_ACTOR ########################### #
oracle_film_actor_sql = "SELECT * FROM film_actor"
mycursor.execute(oracle_film_actor_sql)
filmActorRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(filmActorRows)
oracleCursor.executemany('insert into FILM_ACTOR(ACTOR_ID, FILM_ID,LAST_UPDATE) values(:1,:2,:3)', filmActorRows)
con.commit()
print("Table FILM_ACTOR filled!!")

# ###################### FILM_CATEGORY ########################### #
oracle_film_category_sql = "SELECT * FROM film_category"
mycursor.execute(oracle_film_category_sql)
filmCategoryRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(filmCategoryRows)
oracleCursor.executemany('insert into FILM_CATEGORY(FILM_ID,CATEGORY_ID,LAST_UPDATE) values(:1,:2,:3)',
                         filmCategoryRows)
con.commit()
print("Table FILM_CATEGORY filled!!")

# ###################### INVENTORY ########################### #
oracle_inventory_sql = "SELECT * FROM inventory"
mycursor.execute(oracle_inventory_sql)
inventoryRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(inventoryRows)
oracleCursor.executemany('insert into INVENTORY(INVENTORY_ID, FILM_ID, STORE_ID ,LAST_UPDATE) values(:1,:2,:3,:4)',
                         inventoryRows)
con.commit()
print("Table INVENTORY filled!!")


# ###################### RENTAL ########################### #
oracle_rental_sql = "SELECT * FROM rental"
mycursor.execute(oracle_rental_sql)
rentalRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(rentalRows)
oracleCursor.executemany(
    'insert into RENTAL(RENTAL_ID, RENTAL_DATE, INVENTORY_ID,CUSTOMER_ID,RETURN_DATE,STAFF_ID, LAST_UPDATE) values(:1,:2,:3,:4,:5,:6,:7)',
    rentalRows)
con.commit()
print("Table RENTAL filled!!")

# ###################### PAYMENT ########################### #
oracle_payment_sql = "SELECT * FROM payment"
mycursor.execute(oracle_payment_sql)
paymentRows = mycursor.fetchall()
oracleCursor.bindarraysize = len(paymentRows)
oracleCursor.executemany('insert into PAYMENT(PAYMENT_ID, CUSTOMER_ID, STAFF_ID, RENTAL_ID, AMOUNT,PAYMENT_DATE,LAST_UPDATE) values(:1,:2,:3,:4,:5,:6,:7)',
    paymentRows)
con.commit()
print("Table PAYMENT filled!!")

# ###################### QUERYS ########################### #

res = oracleCursor.execute("SELECT * FROM FILM WHERE FILM_ID <= 3").fetchall()
print("res =",res)

res2 = oracleCursor.execute("SELECT FILM.TITLE, LANGUAGE.NAME FROM FILM, LANGUAGE WHERE FILM.LANGUAGE_ID = LANGUAGE.LANGUAGE_ID").fetchall()
print("res2 =",res2)
