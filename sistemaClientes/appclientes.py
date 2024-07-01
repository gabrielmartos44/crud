#Se importan las librerias necesarias
from flask import Flask
from flaskext.mysql import MySQL
from flask import render_template, request, redirect

#se crea una applicacion con flask
app=Flask(__name__)


# Creamos la conexión con la base de datos:
mysql=MySQL()
# Creamos la referencia al host, para que se conecte a la base
# de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST']='localhost'
# Indicamos el usuario
app.config['MYSQL_DATABASE_USER']='root'
# Sin contraseña
app.config['MYSQL_DATABASE_PASSWORD']=''
# Nombre de nuestra BD
app.config['MYSQL_DATABASE_BD']='clientes'
mysql.init_app(app)


#se define una ruta raiz en la aplicacion flask y se cra la funcion clientes 
#se ejcuta un select para buscar todos los afiliados en la a base de datos para posteriormente mostralos en el html
#conecto,creo un cursor para ejecutar consultas sql, ejecuto la query y 
# guardo los registros buscados por la consulta en la variable db_afiliados
#renderizo clientes.html y paso la paso los datos guardados en db_afiliados como una variable en "afis"
@app.route('/')
def clientes():
    sql="SELECT * FROM `clientes`.`afiliados`"

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    db_afiliados=cursor.fetchall()

    
    return render_template("afiliados/clientes.html",afis=db_afiliados)

## creo la  ruta donde renderizo el documento html cada vez que se ingresa a la pagina
@app.route("/create.html")
def create():
    return render_template("afiliados/create.html")

#Se define  una ruta /store a una aplicacion flask la cual acepta solicitudes HTTP POST
#se define la funcion storage la cual ejecuta el codigo
#Se seleccionan los datos y se guardan en variable(estos se agrupan en una dupla llamada "datos")
#Se define un codigo sql para hacer el insert a la base de datos pasando todas las variables solitadas previamente por html
# conecto con la base de datos, ,creo un cursor para ejecutar consultas sql, ejecuto la query(pasando la dupla datos como parametro)  y confirmo la transaccion con el comit
# con el return me redirijo nuevamenta a la pagina principal
@app.route("/store",methods=["POST"])
def storage(): 
    _nombre=request.form["txtNombre"]
    _apellido=request.form["txtApellido"]
    _patologia=request.form["txtPatologia"]
    _informes=request.form["txtInformes"]
    _foto="null.jpg"

    datos=(_nombre,_apellido,_patologia,_informes,_foto)
    sql="INSERT INTO `clientes`.`afiliados` (`ID`, `NOMBRE`, `APELLIDO`, `PATOLOGIA`, `INFORMES`, `FOTOS`) VALUES (NULL,%s,%s,%s,%s,%s);"

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect("/")

#Se define una ruta destroy donde se pasara un entero(id) para que la funcion destroy o utilice como argumento
#Se define una consulta sql para eliminar de la tabla el el afiliado con el id seleccionado
#conecto con la base de datos, ,creo un cursor para ejecutar consultas sql, ejecuto la query(pasando el id como parametro) y confirmo la transaccion con el comit
#Se redireciona a la pagina principal
@app.route("/destroy/<int:id>")
def destroy(id):
    
    sql= "DELETE FROM `clientes`.`afiliados` WHERE `afiliados`.`ID` = %s;"

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,(id))
    conn.commit()
    
    return redirect("/")

#Se define una ruta edit donde se pasara un entero(id) para que la funcion edit o utilice como argumento
#Defino la consulta sql la cual selecciona todos los campos de la tabla afiliados donde el id consida con el pasado como parametro
#conecto con la base de datos, ,creo un cursor para ejecutar consultas sql, ejecuto la query(pasando el id como parametro) y confirmo la transaccion con el comit
#recupero los registros los cuales se guardan en la variable _afiliados
#renderizo edit.html y paso la paso los datos guardados en _afiliados como una variable en "afis"
@app.route("/edit/<int:id>")
def edit(id):

    sql="SELECT * FROM `clientes`.`afiliados` WHERE `afiliados`.`ID` = %s;"

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,(id))
    _afiliados=cursor.fetchall()
    conn.commit()

    return render_template("afiliados/edit.html", afis=_afiliados)
    
#Se define  una ruta /update a una aplicacion flask la cual acepta solicitudes HTTP POST
#se define la funcion update la cual ejecuta el codigo
#Se seleccionan los datos y se guardan en variable(estos se agrupan en una dupla llamada "datos")
#Se define un codigo sql para hacer el update a la base de datos pasando todas las variables solitadas previamente por html
#conecto con la base de datos, creo un cursor para ejecutar consultas sql, ejecuto la query(pasando la dupla datos como parametro)  y confirmo la transaccion con el comit
#con el return me redirijo nuevamenta a la pagina principal
@app.route("/update",methods=["POST"])
def update():
    _nombre=request.form["txtNombre"]
    _apellido=request.form["txtApellido"]
    _patologia=request.form["txtPatologia"]
    _informes=request.form["txtInformes"]
    _foto="null.jpg"
    id=request.form["txtID"]

    datos=(_nombre,_apellido,_patologia,_informes,_foto,id)

    sql="UPDATE `clientes`.`afiliados` SET `NOMBRE`= %s, `APELLIDO`= %s, `PATOLOGIA`= %s, `INFORMES`= %s, `FOTOS`= %s WHERE `afiliados`.`ID` = %s;"

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect("/")

#se asegura de que el servidor Flask se ejecute solo si el script se está ejecutando directamente
if __name__=="__main__":
    app.run(debug=True,port=8055)

