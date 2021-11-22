from re import I
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
from Service import *
app = Flask(__name__)

#Conexion a base de datos NYSQL
app.config["MYSQL_HOST"] = "208.91.198.197"
app.config["MYSQL_USER"] = "nueva_era"
app.config["MYSQL_PASSWORD"] = "NuevaEra843*"
app.config["MYSQL_DB"] = "construcciones_db"
mysql = MySQL(app)
print("Conexión establecida exitosamente!")

#Configuracion
app.secret_key = "mysecretkey"

@app.route("/")
def home():
	return render_template("login.html")

@app.route("/dashboard")
def dashboard():
	data = ("Dashboard | Nueva Era","Dashboard")
	return render_template("dashboard.html", datos = data)

@app.route("/perfil")
def perfil():
	data = ("Mi Perfil | Nueva Era","Mi Perfil")
	return render_template("perfil.html", datos = data)

@app.route("/usuarios")
def usuarios():
	data = ("Usuarios | Nueva Era","Usuarios")
	return render_template("usuarios.html", datos = data)

@app.route("/roles")
def roles():
	data = ("Roles | Nueva Era","Roles")
	return render_template("roles.html", datos = data)

@app.route("/roles/permisos")
def permisos():
	data = ("Permisos | Nueva Era","Permisos")
	return render_template("permisos.html", datos = data)

@app.route("/actualizar")
def actualizar():
	data = ("Actualizar Info | Nueva Era","Actualizar información")
	return render_template("actualizar.html", datos = data)


#Construcciones privadas
@app.route("/construcciones_privadas")
def construc_priv():
	data = ("Construcciones Privadas | Nueva Era","Construcciones Privadas","functions_constructora.js")
	return render_template("construc_priv.html", datos = data)

@app.route("/list_construc_priv")
def list_construc_priv():
	data = Service.get_usuarios()
	data = [list(i) for i in data]
	for i in range(len(data)):
		if data[i][6] != None:
			data[i][6] = datetime.strftime(data[i][6],"%d-%m-%Y")
		else:
			data[i][6] = "No existe"

		if data[i][8] == "Activa":
			data[i][8] = '<span class="badge bg-info">Activa</span>'
		elif data[i][8] == "Vencida":
			data[i][8] = '<span class="badge bg-danger">Vencida</span>'
		else:
			data[i][8] = '<span class="badge bg-secondary">Duda</span>'

		data[i].append('<div class="text-center">'+
				'<button class="btn btn-warning btn-sm btn-ver-construc" rl="'+data[i][0]+'" title="Ver"><i class="fas fa-eye"></i></button> '+
				'<button class="btn btn-primary btn-sm btn-edit-construc" rl="'+data[i][0]+'" title="Comentar"><i class="fas fa-pencil-alt"></i></button> '+
				'<button class="btn btn-danger btn-sm btn-eli-construc" rl="'+data[i][0]+'" title="Eliminar"><i class="fas fa-trash-alt"></i></button> '+
				'</div>')
	return jsonify(data)

@app.route("/regis_contruc_priv")
def regis_construc_priv():
	if request.method == "POST":
		cur = mysql.connection.cursor()
		cur.execute("select max(id_const)+1 from construccion")
		codigo = cur.fetchall()
		nombre = request.form["nom_const"]
		apellidos = request.form["ape_emple"]
		dni = request.form["dni_emple"]
		fecha = request.form["fech_emple"]
		mail = request.form["mail_emple"]
		telefono = request.form["telef_emple"]
		distrito = request.form["distr_emple"]
		estado = request.form["estado"]
		cur.execute("insert into construccion values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(codigo,nombre,apellidos,dni,fecha,'',mail,telefono,distrito,estado))
		mysql.connection.commit()
		response = {"status":"True", "msj": "Construccion registrada correctamente!"}
		return jsonify(response)

@app.route("/buscar_construc_priv/<id_construc>", methods=["GET"])
def buscar_construc_priv(id_construc):
	cur = mysql.connection.cursor()
	cur.execute("call sp_buscar_const_priv(%s)", [id_construc])
	data = cur.fetchall()
	data = [list(i) for i in data]
	if data[0][6] != None:
		data[0][6] = datetime.strftime(data[0][6],"%Y-%m-%d")
	else:
		data[0][6] = "No existe"
	return jsonify(data[0])

@app.route("/actividad_construc_priv")
def actividad_construc_priv():
	data = ("Registrar Actividad | Nueva Era","Registrar Actividad",)
	return render_template("registrar_actividad_privada.html", datos = data)

#Construcciones publicas
@app.route("/construcciones_publicas")
def construc_pub():
	data = ("Construcciones Públicas | Nueva Era","Construcciones Públicas","functions_constructora.js")
	return render_template("construc_pub.html", datos = data)

@app.route("/list_construc_pub")
def list_construc_pub():
	cur = mysql.connection.cursor()
	cur.execute("call sp_listar_const_pub")
	data = cur.fetchall()
	data = [list(i) for i in data]
	for i in range(len(data)):
		if(data[i][6] == "Activa"):
			data[i][6] = '<span class="badge bg-info">Activa</span>'
		else:
			data[i][6] = '<span class="badge bg-danger">Inactiva</span>'

		data[i].append('<div class="text-center">'+
				'<button class="btn btn-warning btn-sm btn-ver-construc" rl="'+data[i][0]+'" title="Ver"><i class="fas fa-eye"></i></button> '+
				'<button class="btn btn-primary btn-sm btn-edit-construc" rl="'+data[i][0]+'" title="Comentar"><i class="fas fa-pencil-alt"></i></button> '+
				'<button class="btn btn-danger btn-sm btn-eli-construc" rl="'+data[i][0]+'" title="Eliminar"><i class="fas fa-trash-alt"></i></button> '+
				'</div>')
	return jsonify(data)
	cur.connection.close();

@app.route("/regis_contruc_pub")
def regis_construc_pub():
	if request.method == "POST":
		cur = mysql.connection.cursor()
		cur.execute("select max(id_const)+1 from construccion")
		codigo = cur.fetchall()
		nombre = request.form["nom_const"]
		apellidos = request.form["ape_emple"]
		dni = request.form["dni_emple"]
		fecha = request.form["fech_emple"]
		mail = request.form["mail_emple"]
		telefono = request.form["telef_emple"]
		distrito = request.form["distr_emple"]
		estado = request.form["estado"]
		cur.execute("insert into construccion values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(codigo,nombre,apellidos,dni,fecha,'',mail,telefono,distrito,estado))
		mysql.connection.commit()
		response = {"status":"True", "msj": "Construccion registrada correctamente!"}
		return jsonify(response)
		cur.connection.close();

@app.route("/buscar_construc_pub/<id_construc>", methods=["GET"])
def buscar_construc_pub(id_construc):
	cur = mysql.connection.cursor()
	cur.execute("call sp_buscar_const_pub(%s)", [id_construc])
	data = cur.fetchall()
	return jsonify(data[0])
	cur.connection.close();

@app.route("/actividad_construc_pub")
def actividad_construc_pub():
	data = ("Registrar Actividad | Nueva Era","Registrar Actividad",)
	return render_template("registrar_actividad_publica.html", datos = data)

# ! REGISTRAR COMENTARIO ------------------------------------!!!
@app.route("/regis_comen", methods=["POST"])
def regis_comen():
	if request.method == "POST":
		cur = mysql.connection.cursor()
		'''id = request.form["id_emple"]
		if id != "0":
			codigo = id
		else:
			cur.execute("select max(id_usuario)+1 from usuario")
			codigo = cur.fetchall()'''
		#TODO id_usuario =
		id_usuario = "null"
		#TODO id_construccion = 
		id_construccion = "null"
		comentario = request.form["comentario"]
		nombre = request.form["name_c"]
		telefono = request.form["num_c"]
		#TODO tipo = request.form["tipo"]
		tipo = "1"
		cur.execute("call sp_registrar_comentario(%s,%s,%s,%s,%s,%s)",(id_usuario,id_construccion,nombre,telefono,tipo,comentario))
		mysql.connection.commit()
		response = {"status":True, "msj":"Comentario registrado correctamente!"}
		return jsonify(response)
		cur.connection.close();


#Empleados
@app.route("/empleados")
def empleados():
	data = ("Empleados | Nueva Era","Empleados","functions_empleado.js")
	return render_template("empleados.html", datos = data)

@app.route("/list_emple")
def list_emple():
	cur = mysql.connection.cursor()
	cur.execute("call sp_listar_empleados")
	data = cur.fetchall()
	data = [list(i) for i in data]
	for i in range(len(data)):
		data[i][4] = datetime.strftime(data[i][4],"%d-%m-%Y")
		if data[i][5] == "ACTIVO":
			data[i][5] = '<span class="badge bg-info">Activo</span>'
		else:
			data[i][5] = '<span class="badge bg-danger">Culminado</span>'
		for j in range(7,9):
			if data[i][j] == None:
				data[i][j] = "No Registrado"
		
		data[i].append('<div class="text-center">'+
				'<button class="btn btn-warning btn-sm btn-ver-emple" rl="'+data[i][0]+'" title="Ver"><i class="fas fa-eye"></i></button> '+
				'<button class="btn btn-primary btn-sm btn-edit-emple" rl="'+data[i][0]+'" title="Editar"><i class="fas fa-pencil-alt"></i></button> '+
				'<button class="btn btn-danger btn-sm btn-eli-emple" rl="'+data[i][0]+'" title="Eliminar"><i class="fas fa-trash-alt"></i></button> '+
				'</div>')
	return jsonify(data)
	cur.connection.close();

@app.route("/list_usuarios")
def list_usuarios():
	cur = mysql.connection.cursor()
	cur.execute("call sp_listar_usuarios")
	data = cur.fetchall()
	print("Capto datos")
	data = [list(i) for i in data]
	for i in range(len(data)):
		if data[i][5] == "1":
			data[i][5] = '<span class="badge bg-info">Activo</span>'
		else:
			data[i][5] = '<span class="badge bg-danger">Inactivo</span>'
		data[i].append('<div class="text-center">'+
				'<button class="btn btn-primary btn-sm btn-edit-usu" rl="'+data[i][0]+'" title="Editar"><i class="fas fa-pencil-alt"></i></button>'+
				'<a class="btn btn-danger btn-sm " href="elim_usuario?a='+data[i][0]+'&b='+data[i][1]+'&c='+data[i][2]+'&d='+data[i][4]+'" role="button" title="Eliminar"><i class="fas fa-trash-alt"></i></a>'+
				'</div>')
		data[i][4] = '<span class="badge bg-success">'+data[i][4]+'</span>'
	return jsonify(data)
	cur.connection.close();

@app.route("/regis_emple", methods=["POST"])
def regis_emple():
	if request.method == "POST":
		cur = mysql.connection.cursor()
		party_id = request.form["id_emple"]
		id_party_generado = ""
		id_mec_cont_generado = ""
		if party_id == "0":
			 party_id = "flag"
			 cur.execute("select f_autogenerar_id_party()")
			 id_party_generado = cur.fetchall()
			 cur.execute("select f_generar_id_m_contc()")
			 id_mec_cont_generado = cur.fetchall()

		print(party_id)
		nombre = request.form["nom_emple"]
		apellidos = request.form["ape_emple"]
		dni = request.form["dni_emple"]
		fecha = request.form["fech_emple"] 

		mail = request.form["mail_emple"] 
		sexo = request.form["sexo"]
		telefono = request.form["telef_emple"]
		distrito = request.form["distr_emple"]
		estado = request.form["estado"]
		
		if estado == "Activo":
			estado = "1"
		else: estado = "0"	
		id_usuario = "USU-100000"

		print(nombre)
		print(apellidos)
		print(dni)
		print(fecha)
		print(mail)
		print(sexo)
		print(telefono)
		print(distrito)
		print(estado)
		print(id_usuario)
		print(id_party_generado)
		print(id_mec_cont_generado)


		cur.execute("call sp_crear_actualizar_usuario(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
		 	(party_id,nombre,apellidos,dni,sexo,fecha,mail,telefono,distrito,estado,id_usuario,id_party_generado,id_mec_cont_generado))
		mysql.connection.commit()
		response = {"status":True, "msj":"Empleado registrado correctamente!"}
		return jsonify(response)
		cur.connection.close();

#! AQUI SE DEBE AGREGAR SEXO  

@app.route("/buscar_empleado/<id_emple>", methods=["GET"])
def buscar_emple(id_emple):
	cur = mysql.connection.cursor()
	cur.execute("call sp_buscar_empleado(%s)",[id_emple])
	data = cur.fetchall()
	data = [list(i) for i in data]
	data[0][4] = datetime.strftime(data[0][4],"%Y-%m-%d")
	data[0][6] = datetime.strftime(data[0][6],"%Y-%m-%d")
	for i in range(7,10):
		if data[0][i] == None:
			data[0][i] = "No Registrado"
	return jsonify(data[0])
	
	
#! ACTUALIZAR EMPLEADO

@app.route("/edi_emple/<id_emple>", methods=["GET"])
def edi_emple(id_emple):
	cur = mysql.connection.cursor()
	cur.execute("call sp_buscar_empleado(%s)",[id_emple])
	data = cur.fetchall()
	data = [list(i) for i in data]
	data[0][4] = datetime.strftime(data[0][4],"%Y-%m-%d")
	data[0][6] = datetime.strftime(data[0][6],"%Y-%m-%d")
	for i in range(7,10):
		if data[0][i] == None:
			data[0][i] = "No Registrado"
	return jsonify(data[0])


@app.route("/elim_emple/<id_emple>", methods=["POST"])
def elim_emple(id_emple):
	cur = mysql.connection.cursor()
	cur.execute("delete from usuario where id_usuario=%s", [id_emple])
	mysql.connection.commit()
	response = {"status":"True", "msj":"Registro de empleado elminado!"}
	return jsonify(response)
	cur.connection.close();

@app.route("/elim_usuario/")
def elim_usuario():
	a = request.args.get('a', None) 
	b = request.args.get('b', None)
	c = request.args.get('c', None)
	d = request.args.get('d', None)
	data = ("Eliminar Usuario | Nueva Era","Eliminar Usuario",a,b,c,d)
	return render_template("usuario_delete.html", datos = data)

@app.route("/get_permiso/<id_usuario>",methods=["GET"])
def get_permiso(id_usuario):
	cur=mysql.connection.cursor()
	print("Funca la funcion")
	cur.execute("call sp_buscar_permiso(%s)",[id_usuario])
	permiso=cur.fetchall()
	print(permiso)
	return jsonify(permiso)
	cur.connection.close();

@app.route("/elim_usuario_perma/<id_usuario>", methods=["POST"])
def elim_usuario_perma(id_usuario):
	cur = mysql.connection.cursor()
	cur.execute("call sp_eliminar_usuario_perma(%s)",[id_usuario])
	mysql.connection.commit()
	response = {"status":"True", "msj":"Usuario eliminado permanentemente!"}
	return jsonify(response)
	cur.connection.close();

@app.route("/elim_usuario_tempo/<id_usuario>", methods=["POST"])
def elim_usuario_tempo(id_usuario):
	cur=mysql.connection.cursor()
	cur.execute("update usuario set id_privilegio='PRI-100001' where id_usuario=%s",[id_usuario])
	mysql.connection.commit()
	response = {"status":"True", "msj":"Usuario eliminado temporalmente!"}
	return jsonify(response)
	cur.connection.close();

@app.route("/regis_usuario/", methods=["POST"])
def regis_usuario():
	

@app.route("/editar_usuario/", methods=["POST"])

@app.route("/actividad/<id_emple>", methods=["GET"])
def actividad(id_emple):
	data = ("Actividad | Nueva Era","Actividad de vendedor","functions_empleado.js")
	return render_template("actividad.html", datos = data)

#Vista PB
@app.route("/vista_pbi")
def vista_pbi():
	data = ("Vista PBI | Nueva Era","Vista Power BI","function_reporte.js")
	return render_template("vista_pbi.html", datos = data)

#Reportes
@app.route("/reportes")
def reportes():
	data = ("Reportes | Nueva Era","Reportes","function_reporte.js")
	return render_template("reportes.html", datos = data)

if __name__ == "__main__":
	app.run(debug=True)