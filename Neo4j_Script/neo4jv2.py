import mysql.connector
from neo4j import GraphDatabase,Transaction,Session

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "pass",
    database = "sakila"
)

mycursor = mydb.cursor()

firstQuery = "SELECT f.title,f.release_year,f.description,c.name AS Category,a.first_name,a.last_name, language.name AS Foreign_language,extra.name AS Original_language,f.film_id,a.actor_id,c.category_id,f.language_id,f.original_language_id FROM film AS f LEFT JOIN film_category AS fc ON fc.film_id = f.film_id LEFT JOIN category AS c ON c.category_id = fc.category_id LEFT JOIN film_actor AS fa ON fa.film_id = f.film_id LEFT JOIN actor AS a ON a.actor_id = fa.actor_id LEFT JOIN language ON language.language_id = f.language_id LEFT JOIN ( SELECT f.film_id,l.name FROM film AS f LEFT JOIN language AS l ON l.language_id = f.original_language_id WHERE f.original_language_id is not null) extra ON f.film_id = extra.film_id"
secondQuery = "SELECT s.store_id, c.first_name AS Costumer_first_name, c.last_name AS Costumer_last_name, p.amount, p.payment_date, st.first_name AS Staff_first_name, st.last_name  AS Staff_last_name,s.manager_staff_id,st.staff_id,st.email,p.payment_id,c.customer_id,c.email FROM store AS s LEFT JOIN customer AS c ON s.store_id = s.store_id LEFT JOIN payment AS p ON c.customer_id = p.customer_id LEFT JOIN staff AS st ON p.staff_id = st.staff_id"
thirdQuery = "SELECT payment.payment_id,rental.rental_id,inventory.film_id From payment Inner JOIN rental ON payment.rental_id = rental.rental_id inner Join inventory ON rental.inventory_id = inventory.inventory_id"

# Fetch the results from the querys
mycursor.execute(firstQuery)
filmRecords = mycursor.fetchall()

myFilmIt = iter(filmRecords)
i1aux = None
categorys = []
actors = []

# Percorrer os filmes 
statmentCreateMovie = "CREATE (f:Filme {id:{id},title:{title},release_year:{release_year},description:{descrição}})"
statmentCreateActor = "CREATE (a:Ator {id:{id},name: {name}})"
statmentCreateActedIn = "MATCH (f:Filme),(a:Ator) WHERE f.id = {filme_id} and a.id = {ator_id} Create (a)-[r:Atuou_em]->(f) Return type(r)"
statmentCreateTemCategoria = "MATCH (c:Categoria),(f:Filme) WHERE f.id = {filme_id} and c.id = {categoria_id} Create (f)-[tc:Tem_Categoria]->(c) Return type(tc)"
statmentCreateCategory = "CREATE (c:Categoria {id:{id},name: {name}})"
statmentCreateLanguage = "CREATE (l:Idioma {id:{id},name:{name}})"
statmentCreateForeignLanguage = "Match (l:Idioma),(f:Filme) Where f.id = {filme_id} and l.id = {foreign_language_id} Create (f)-[le:Idioma_Estrangeiro]->(l) Return type(le)"
statmentCreateOriginalLanguage = "Match (l:Idioma),(f:Filme) Where f.id = {filme_id} and l.id = {original_language_id} Create (f)-[lo:Idioma_Original]->(l) Return type(lo)" 
statmentQueryCategory = "MATCH (c:Categoria) WHERE c.id = {id} Return c"
statmentQueryMovie = "MATCH (m:Filme) WHERE m.id = {id} RETURN m"
statmentQueryActor = "MATCH (m:Ator) WHERE m.id = {id} RETURN m"
statmentQueryActedIn = "MATCH (a:Ator) -[at:Atuou_em]- (f:Filme) Where a.id = {ator_id} and f.id = {filme_id} Return at"
statmentQueryTemCategoria = "MATCH (f:Filme) -[tc:Tem_Categoria]- (c:Categoria) where f.id = {filme_id} and c.id = {categoria_id} Return tc"
statmentQueryLanguage = "MATCH (l:Idioma) where l.id = {id} Return l"
statmentQueryForeignLanguage = "MATCH (l:Idioma) -[le : Idioma_Estrangeiro]- (f:Filme) Where l.id = {foreign_language_id} and f.id = {filme_id} Return le"
statmentQueryOriginalLanguage = "MATCH (l:Idioma) -[lo : Idioma_Original]- (f:Filme) Where l.id = {original_language_id} and f.id = {filme_id} Return lo"

while(True):
    try:
        i1 = next(myFilmIt)
    except StopIteration:
        print("First collection done")
        break
    if i1aux == None:
        i1aux = i1
    # category and actors
    if i1aux[0] == i1[0]:
        actors.append({"name": i1[4] + " " + i1[5],"id": i1[9]})
        if i1[3] not in categorys:
            categorys.append({"name" :i1[3],"id" : i1[10]})
    else:
        with driver.session() as se:
            res = se.run(statmentQueryMovie,id=i1aux[8])    
            if res.single() == None:
                info = { "id": i1aux[8], "title" : i1aux[0], "release_year" : i1aux[1], "descrição" : i1aux[2]}
                se.run(statmentCreateMovie,info)
                print("New Filme")
            res =  se.run(statmentQueryLanguage,id=i1aux[11])
            if res.single() == None and not i1aux[6] == None:
                se.run(statmentCreateLanguage,id=i1aux[11],name=i1aux[6])
                print("New Language")
            res = se.run(statmentQueryForeignLanguage,filme_id=i1aux[8],foreign_language_id=i1aux[11])
            if res.single() == None and not i1aux[6] == None:
                se.run(statmentCreateForeignLanguage,filme_id=i1aux[8],foreign_language_id=i1aux[11])
                print("New Foreign Language Relathionship")
            res =  se.run(statmentQueryLanguage,id=i1aux[12])
            if res.single() == None and not i1aux[7] == None:
                se.run(statmentCreateLanguage,id=i1aux[12],name=i1aux[7])
                print("New Language")
            res = se.run(statmentQueryOriginalLanguage,filme_id=i1aux[8],original_language_id=i1aux[12])
            if res.single() == None and not i1aux[7] == None:
                se.run(statmentCreateOriginalLanguage,filme_id=i1aux[8],original_language_id=i1aux[12])
                print("New Original Language Relathionship")
            for actor in actors:
                res = se.run(statmentQueryActor,id=actor["id"])
                if res.single() == None:
                    se.run(statmentCreateActor,actor)
                    print("New Actor")
                res = se.run(statmentQueryActedIn,ator_id=actor["id"],filme_id=i1aux[8])
                if res.single() == None:
                    se.run(statmentCreateActedIn,ator_id=actor["id"],filme_id=i1aux[8])
                    print("New Actou em Relationship")                
            for category in categorys:
                res = se.run(statmentQueryCategory,id=category["id"])
                if res.single() == None:
                    se.run(statmentCreateCategory,category)
                    print("New Category")
                res = se.run(statmentQueryTemCategoria,categoria_id=category["id"],filme_id=i1aux[8])
                if res.single() == None:
                    se.run(statmentCreateTemCategoria,categoria_id=category["id"],filme_id=i1aux[8])
                    print("New Tem Categoria Relathionship")
                    se.sync()
        actors.clear()
        categorys.clear()
    i1aux = i1

# Adicionar o ultimo que pode nao ter sido incluido

with driver.session() as se:
            res = se.run(statmentQueryMovie,id=i1aux[8])    
            if res.single() == None:
                info = { "id": i1aux[8], "title" : i1aux[0], "release_year" : i1aux[1], "descrição" : i1aux[2]}
                se.run(statmentCreateMovie,info)
                print("New Filme")
            res =  se.run(statmentQueryLanguage,id=i1aux[11])
            if res.single() == None and not i1aux[6] == None:
                se.run(statmentCreateLanguage,id=i1aux[11],name=i1aux[6])
                print("New Language")
            res = se.run(statmentQueryForeignLanguage,filme_id=i1aux[8],foreign_language_id=i1aux[11])
            if res.single() == None and not i1aux[6] == None:
                se.run(statmentCreateForeignLanguage,filme_id=i1aux[8],foreign_language_id=i1aux[11])
                print("New Foreign Language Relathionship")
            res =  se.run(statmentQueryLanguage,id=i1aux[12])
            if res.single() == None and not i1aux[7] == None:
                se.run(statmentCreateLanguage,id=i1aux[12],name=i1aux[7])
                print("New Language")
            res = se.run(statmentQueryOriginalLanguage,filme_id=i1aux[8],original_language_id=i1aux[12])
            if res.single() == None and not i1aux[7] == None:
                se.run(statmentCreateOriginalLanguage,filme_id=i1aux[8],original_language_id=i1aux[12])
                print("New Original Language Relathionship")
            for actor in actors:
                res = se.run(statmentQueryActor,id=actor["id"])
                if res.single() == None:
                    se.run(statmentCreateActor,actor)
                    print("New Actor")
                res = se.run(statmentQueryActedIn,ator_id=actor["id"],filme_id=i1aux[8])
                if res.single() == None:
                    se.run(statmentCreateActedIn,ator_id=actor["id"],filme_id=i1aux[8])
                    print("New Actou em Relationship")                
            for category in categorys:
                res = se.run(statmentQueryCategory,id=category["id"])
                if res.single() == None:
                    se.run(statmentCreateCategory,category)
                    print("New Category")
                res = se.run(statmentQueryTemCategoria,categoria_id=category["id"],filme_id=i1aux[8])
                if res.single() == None:
                    se.run(statmentCreateTemCategoria,categoria_id=category["id"],filme_id=i1aux[8])
                    print("New Tem Categoria Relathionship")
                    se.sync()

# Percorrer a informaçao sobre as stores 

mycursor.execute(secondQuery)
storeRecords = mycursor.fetchall()
myStoreIt = iter(storeRecords)

# statments

statmentQueryStore = "Match (s:Loja) Where s.id = {store_id} Return s"
statmentCreateStore = "Create (s:Loja {id: {store_id},manager_id:{manager_id}})"
statmentQueryStaff = "Match (s:Staff) Where s.id = {staff_id} Return s"
statmentCreateStaff = "Create (s:Staff {id: {staff_id},name: {name},email : {email}})"
statmentQueryTrabalhaEm = "Match (s:Staff) -[r:Trabalha_Em]- (st:Loja) Where s.id = {staff_id} and st.id = {store_id} Return r"
statmentCreateTrabalhaEm = "Match (s:Staff),(st:Loja) Where s.id = {staff_id} and st.id = {store_id} Create (s)-[te:Trabalha_Em]->(st) Return type(te)"
statmentQueryCustomer = "Match (c:Cliente) Where c.id = {customer_id} Return c"
statmentCreateCustomer = "Create (c:Cliente {id: {customer_id},name: {name},email : {email}})"
statmentQueryPayment = "Match (p:Pagamento) Where p.id = {payment_id} Return p"
statmentCreatePayment = "Create (p:Pagamento {id: {payment_id},amount: {amount},date: {date}})"
statmentQueryPertence = "Match (s:Pagamento) -[r:Pertence]- (st:Cliente) Where s.id = {payment_id} and st.id = {customer_id} Return r"
statmentCreatePertence = "Match (s:Pagamento),(st:Cliente) Where s.id = {payment_id} and st.id = {customer_id} Create (s)-[te:Pertence]->(st) Return type(te)"
statmentQueryEmitidaEm = "Match (s:Pagamento) -[r:Emitida_Em]- (st:Loja) Where s.id = {payment_id} and st.id = {store_id} Return r"
statmentCreateEmitidaEm = "Match (s:Pagamento),(st:Loja) Where s.id = {payment_id} and st.id = {store_id} Create (s)-[te:Emitida_Em]->(st) Return type(te)"
statmentQueryEmitidaPor = "Match (s:Staff) -[r:Emitida_Por]- (st:Pagamento) Where s.id = {staff_id} and st.id = {payment_id} Return r"
statmentCreateEmitidaPor = "Match (s:Staff),(st:Pagamento) Where s.id = {staff_id} and st.id = {payment_id} Create (st)-[te:Emitida_Por]->(s) Return type(te)"

while(True):
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
    staffInfo = {"staff_id" : staff_id, "name": staff, "email" : staff_email}
    paymentInfo = {"payment_id": payment_id,"amount" : amount,"date": date}
    customerInfo = {"customer_id": costumer_id,"name": costumer,"email": costumer_email}
    print(storeInfo)
    print(staffInfo)
    print(paymentInfo)
    print(customerInfo)
    with driver.session() as se:
        res = se.run(statmentQueryStore,store_id=storeInfo["store_id"])
        if res.single() == None:
            se.run(statmentCreateStore,storeInfo)
            se.sync()
            print("New Store")
        res = se.run(statmentQueryStaff,staff_id=staffInfo["staff_id"])
        if res.single() == None:
            se.run(statmentCreateStaff,staffInfo)
            se.sync()
            print("New Staff")
        res = se.run(statmentQueryTrabalhaEm,staff_id=staffInfo["staff_id"],store_id=storeInfo["store_id"])
        if res.single() == None:
            se.run(statmentCreateTrabalhaEm,staff_id=staffInfo["staff_id"],store_id=storeInfo["store_id"])
            se.sync()
            print("New Trabalha_Em Relathionship")
        res = se.run(statmentQueryCustomer,customer_id=customerInfo["customer_id"])
        if res.single() == None:
            se.run(statmentCreateCustomer,customerInfo)
            se.sync()
            print("New Customer")
        res = se.run(statmentQueryPayment,payment_id=paymentInfo["payment_id"])
        if res.single() == None:
            se.run(statmentCreatePayment,paymentInfo)
            se.sync()
            print("New Payment")
        res = se.run(statmentQueryPertence,payment_id=paymentInfo["payment_id"],customer_id=customerInfo["customer_id"])
        if res.single() == None:
            se.run(statmentCreatePertence,payment_id=paymentInfo["payment_id"],customer_id=customerInfo["customer_id"])
            se.sync()
            print("New Pertence Relathionship")
        res = se.run(statmentQueryEmitidaEm,payment_id=paymentInfo["payment_id"],store_id=storeInfo["store_id"])
        if res.single() == None:
            se.run(statmentCreateEmitidaEm,payment_id=paymentInfo["payment_id"],store_id=storeInfo["store_id"])
            se.sync()
            print("New Emitida_Em Relathionship")
        res = se.run(statmentQueryEmitidaPor,staff_id=staffInfo["staff_id"],payment_id=paymentInfo["payment_id"])
        if res.single() == None:
            se.run(statmentCreateEmitidaPor,staff_id=staffInfo["staff_id"],payment_id=paymentInfo["payment_id"])
            se.sync()
            print("New Emitida_Por Relathionship")
        
    # inserir aqui

mycursor.execute(thirdQuery)
connectionsRecord = mycursor.fetchall()
connectionsIter = iter(connectionsRecord)
statmentQueryPaymentFilm = "Match (p:Pagamento)-[r:Corresponde]-(f:Filme) Where p.id = {payment_id} and f.id = {film_id} Return r"
statmentCreatePaymentFilm = "Match (p:Pagamento),(f:Filme) Where p.id = {payment_id} and f.id = {film_id} Create (p)-[r:Corresponde]->(f) Return type(r)"

while(True):
	try:
		i2 = next(connectionsIter)
	except StopIteration:
		print("Third collection done")
		break
	connectionInfo = {"payment_id": i2[0],"film_id": i2[2]}
	with driver.session() as se:
		res = se.run(statmentQueryMovie,id=i2[2])
		if res.single() != None:
			res = se.run(statmentQueryPayment,payment_id=i2[0])  	
			if res.single() != None:
				res = se.run(statmentQueryPaymentFilm,payment_id=i2[0],film_id=i2[2])
				if res.single() == None:
					se.run(statmentCreatePaymentFilm,payment_id=i2[0],film_id=i2[2])
					print("New Corresponde Relationship")

















