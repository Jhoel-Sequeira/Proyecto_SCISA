
from asyncio.windows_events import NULL
from re import S
from flask import Flask, flash, redirect, render_template, request, url_for,session
from datetime import datetime
import cs50
from cs50 import SQL
from sqlalchemy import null
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')
db = cs50.SQL("sqlite:///base.db") 
app.secret_key = "super secret key"

@app.route('/')
def Index():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        ###SELECT U.User, U.Contraseña, ur.idRole as Rol FROM Usuario as U inner join UserRole as ur on U.User=ur.idUser Where U.User=:username
        # Query database for username
        if usuario == "" or contraseña == "":
            return render_template('login.html', hola = 1)
        else:
            rows = db.execute("SELECT * FROM credenciales Where Usuario=:username",
                          username=usuario)
            if len(rows) == 0 or not check_password_hash(rows[0]["Contraseña"], contraseña):
                return render_template('login.html', hola = 1)
            else:
                #Estas consultas son para mostrar la lista de personas y su asistencia
                hi = datetime.now()
                himes = hi.month
                db.execute('INSERT INTO Registro VALUES (:usuario,:fecha,:salida,:horae,:horas,:trab,:mes)',
                usuario= usuario, fecha = datetime.date(hi),salida = NULL, horae = datetime.time(hi),horas = NULL, trab =NULL, mes = himes )
                # Recordar el usuario y rol que se logeo
                session["user_id"] = rows[0]["Usuario"]
                session["userrole"]=rows[0]["Id_rol"]
                return redirect(url_for('home'))
    else:
        return render_template("index.html")

@app.route('/asistencia', methods=["GET", "POST"])
def asistencia():
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hi = datetime.now()
    himes = hi.month            
    prueba1 = db.execute('select Usuario, Fecha_entrada, Fecha_salida, Hora_entrada, Hora_salida,Horas_trabajadas from Registro where mes = :t ', t = himes)
    asistencia = db.execute('select Usuario, Fecha_entrada, Fecha_salida, Hora_entrada, Hora_salida,Horas_trabajadas from Registro GROUP BY Usuario')

    return render_template('Asistencia.html',mes = meses[himes], listas = prueba1, asist = asistencia,usuario = prueba1[0]["Usuario"])
        


@app.route('/mostratrasistencia', methods=["GET", "POST"])
def mostrarasistencia():
    if request.method == "POST":
        hi = datetime.now()
        himes = hi.month
        sele = request.form['seleccion']
        user = request.form['seleccion1']
        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        prueba1 = db.execute('select Usuario, Fecha_entrada from Registro where mes = :t AND Usuario = :us', t = int(sele),us = user)
        asistencia = db.execute('select Usuario, Fecha_entrada from Registro GROUP BY Usuario')
        return render_template('Asistencia.html',mes = meses[int(sele)], listas = prueba1, asist = asistencia)
        
    else:

        return redirect(url_for("index"))
@app.route('/deslog')
def deslog():
    hi = datetime.now()
    himes = hi.month
    db.execute('UPDATE  Registro SET Fecha_salida = :sal, Hora_salida = :horasal WHERE Fecha_entrada = :fe',
    sal= datetime.date(hi), horasal = datetime.time(hi),  fe = datetime.date(hi))
    hora_trabajadas = db.execute('SELECT (strftime("%s", Hora_salida) - strftime("%s", Hora_entrada))/3600 AS HorasTrab from Registro WHERE Fecha_entrada = :fe',
    fe = datetime.date(hi))
    db.execute('UPDATE  Registro SET Horas_trabajadas = :ht WHERE Fecha_entrada = :fe',
    ht= hora_trabajadas[0]["HorasTrab"],  fe = datetime.date(hi))
    session.clear()
    return render_template('login.html')        

@app.route('/Cotizacion')
def cotizacion():
    
     return render_template('cotizacion.html')

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        sele = request.form['selec-mes']
        if sele:
            if sele == 'todo':
                print("todo")
                proyectos = db.execute("SELECT * FROM Proyectos")
                proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = session["user_id"])
                solicitudes = db.execute("SELECT * FROM Solicitudes")
                #contar los proyectos aprobados, incompletos y en progreso
                completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Completado")
                Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Incompleto")
                Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Progreso")
                imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
                total = db.execute("SELECT COUNT(*) FROM Proyectos")
                cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Completado",to = total[0]['COUNT(*)'])
                cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Progreso",to = total[0]['COUNT(*)'])
                cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Incompleto",to = total[0]['COUNT(*)'])
                return render_template('home.html',var1 = "",completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'],
                incompleto = cuentaInc[0]['calc'], pro = proyectos, proUser = proyectos_user, soli = solicitudes,
                comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],prog = Progreso[0]["COUNT(Estado)"], img = imagen,
                indice = "todo")  
    
            else:    
                print("meses")
                proyectos_especificos = db.execute("SELECT * FROM Proyectos WHERE strftime('%m', FechaInicio) = :mes",mes = sele)
                proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user ",user = session["user_id"])
                solicitudes = db.execute("SELECT * FROM Solicitudes")
                #contar los proyectos aprobados, incompletos y en progreso
                completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado AND strftime('%m', FechaInicio)=:mes",estado = "Completado", mes = sele)
                Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado AND strftime('%m', FechaInicio)=:mes",estado = "Incompleto", mes = sele)
                Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado AND strftime('%m', FechaInicio)=:mes",estado = "Progreso", mes = sele)
                imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
                total = db.execute("SELECT COUNT(*) FROM Proyectos WHERE strftime('%m', FechaInicio) = :mes",mes = sele)
                cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est AND strftime('%m', FechaInicio) = :mes",est = "Completado",to = total[0]['COUNT(*)'],mes = sele)
                cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est AND strftime('%m', FechaInicio) = :mes",est = "Progreso",to = total[0]['COUNT(*)'],mes = sele)
                cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est AND strftime('%m', FechaInicio) = :mes",est = "Incompleto",to = total[0]['COUNT(*)'],mes = sele)
                indice = "mes"
                print(indice)
                return render_template('home.html',var1 = "",completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'], incompleto = cuentaInc[0]['calc'], pro = 0, proUser = proyectos_user, soli = solicitudes,comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],prog = Progreso[0]["COUNT(Estado)"],
                img = imagen, pro_espe = proyectos_especificos,indice = "mes")  
        else:
            print("afuera del if de todo")
            proyectos = db.execute("SELECT * FROM Proyectos")
            proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = session["user_id"])
            solicitudes = db.execute("SELECT * FROM Solicitudes")
            #contar los proyectos aprobados, incompletos y en progreso
            completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Completado")
            Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Incompleto")
            Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Progreso")
            imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
            total = db.execute("SELECT COUNT(*) FROM Proyectos")
            cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Completado",to = total[0]['COUNT(*)'])
            cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Progreso",to = total[0]['COUNT(*)'])
            cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Incompleto",to = total[0]['COUNT(*)'])
            return render_template('home.html',var1 = "",completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'], 
            incompleto = cuentaInc[0]['calc'], pro = proyectos, proUser = proyectos_user, 
            soli = solicitudes,comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],
            prog = Progreso[0]["COUNT(Estado)"], img = imagen,indice = "todo")  
    else:
        print("carga")
        
        proyectos = db.execute("SELECT * FROM Proyectos")
        proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = session["user_id"])
        solicitudes = db.execute("SELECT * FROM Solicitudes")
        #contar los proyectos aprobados, incompletos y en progreso
        completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Completado")
        Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Incompleto")
        Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Progreso")
        imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
        total = db.execute("SELECT COUNT(*) FROM Proyectos")
        cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Completado",to = total[0]['COUNT(*)'])
        cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Progreso",to = total[0]['COUNT(*)'])
        cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Incompleto",to = total[0]['COUNT(*)'])
        return render_template('home.html',var1 = "",completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'], incompleto = cuentaInc[0]['calc'], pro = proyectos, proUser = proyectos_user, soli = solicitudes,comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],prog = Progreso[0]["COUNT(Estado)"], img = imagen)  

 
# mostrar los modals segun su seleccion
@app.route('/modal')
def modal():
    proyectos = db.execute("SELECT * FROM Proyectos")
    permisos = db.execute("SELECT * FROM Solicitudes")
    return render_template('modal.html', pro = proyectos, permiso = permisos)
        

@app.route('/reporte', methods=["GET", "POST"])
def reporte():
    if request.method == "POST":
        tarea = request.form['tarea']
        porcentaje = request.form['porcentaje']
        descripcion = request.form['descripcion']
        imagen = request.form['imagen']
        print(imagen)
        db.execute("INSERT INTO Reportes VALUES(NULL,:nom,:porcen,:desc,:img)",nom = tarea, porcen = porcentaje, desc = descripcion, img = imagen)
        return redirect(url_for('home')) 
    else:
        return redirect(url_for("index"))    

@app.route('/solicitud', methods=["GET", "POST"])
def solicitud():
    if request.method == "POST":
       hi = datetime.now()
       nombre = request.form['nombre']
       titulo = request.form['titulo']
       justificacion = request.form['justificacion']
       db.execute('INSERT INTO solicitudes VALUES (NULL,:nom,:jus,:fech,:titu,:estado,:vi)',nom = nombre, jus = justificacion,fech = datetime.date(hi),titu =titulo
       ,estado = "Pendiente",vi = 1 )
       return redirect(url_for('home'))  
    else:

        return redirect(url_for("index"))
@app.route('/AceptarSoli', methods=["GET", "POST"])
def AceptarSoli():
     if request.method == "POST":
        id = request.form['resp'] 
        solicitudes = db.execute("SELECT * FROM Solicitudes")
        db.execute('UPDATE  Solicitudes SET Estado = :est,Vigente = :vi WHERE Id_Solicitud = :Id',
        est = "Aprobado",vi = 0, Id = id)
        return redirect(url_for('home'))
     
     else:

        return redirect(url_for("index"))         

@app.route('/home1/<string:info>')
def home1(info):
    if request.method == "POST":
        sele = request.form['selec-mes']
        if sele:
            if sele == 'todo':
                print("todo")
                proyectos = db.execute("SELECT * FROM Proyectos")
                proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = session["user_id"])
                solicitudes = db.execute("SELECT * FROM Solicitudes")
                #contar los proyectos aprobados, incompletos y en progreso
                completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Completado")
                Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Incompleto")
                Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Progreso")
                imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
                total = db.execute("SELECT COUNT(*) FROM Proyectos")
                cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Completado",to = total[0]['COUNT(*)'])
                cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Progreso",to = total[0]['COUNT(*)'])
                cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Incompleto",to = total[0]['COUNT(*)'])
                variable = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = info)
                return render_template('home.html',var1 = variable,completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'],
                incompleto = cuentaInc[0]['calc'], pro = proyectos, proUser = proyectos_user, soli = solicitudes,
                comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],prog = Progreso[0]["COUNT(Estado)"], img = imagen,
                indice = "todo")  
    
            else:    
                print("meses")
                proyectos_especificos = db.execute("SELECT * FROM Proyectos WHERE strftime('%m', FechaInicio) = :mes",mes = sele)
                proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user ",user = session["user_id"])
                solicitudes = db.execute("SELECT * FROM Solicitudes")
                #contar los proyectos aprobados, incompletos y en progreso
                completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado AND strftime('%m', FechaInicio)=:mes",estado = "Completado", mes = sele)
                Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado AND strftime('%m', FechaInicio)=:mes",estado = "Incompleto", mes = sele)
                Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado AND strftime('%m', FechaInicio)=:mes",estado = "Progreso", mes = sele)
                imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
                total = db.execute("SELECT COUNT(*) FROM Proyectos WHERE strftime('%m', FechaInicio) = :mes",mes = sele)
                cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est AND strftime('%m', FechaInicio) = :mes",est = "Completado",to = total[0]['COUNT(*)'],mes = sele)
                cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est AND strftime('%m', FechaInicio) = :mes",est = "Progreso",to = total[0]['COUNT(*)'],mes = sele)
                cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est AND strftime('%m', FechaInicio) = :mes",est = "Incompleto",to = total[0]['COUNT(*)'],mes = sele)
                indice = "mes"
                print(indice)
                variable = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = info)
                print(variable)
                return render_template('home.html',var1 = variable,completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'], incompleto = cuentaInc[0]['calc'], pro = 0, proUser = proyectos_user, soli = solicitudes,comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],prog = Progreso[0]["COUNT(Estado)"],
                img = imagen, pro_espe = proyectos_especificos,indice = "mes")  
        else:
            print("afuera del if de todo")
            proyectos = db.execute("SELECT * FROM Proyectos")
            proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = session["user_id"])
            solicitudes = db.execute("SELECT * FROM Solicitudes")
            #contar los proyectos aprobados, incompletos y en progreso
            completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Completado")
            Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Incompleto")
            Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Progreso")
            imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
            total = db.execute("SELECT COUNT(*) FROM Proyectos")
            cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Completado",to = total[0]['COUNT(*)'])
            cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Progreso",to = total[0]['COUNT(*)'])
            cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Incompleto",to = total[0]['COUNT(*)'])
            variable = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = info)
            print(variable)
            return render_template('home.html',var1 = variable,completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'], 
            incompleto = cuentaInc[0]['calc'], pro = proyectos, proUser = proyectos_user, 
            soli = solicitudes,comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],
            prog = Progreso[0]["COUNT(Estado)"], img = imagen,indice = "todo")  
    else:
        print("carga")
        
        proyectos = db.execute("SELECT * FROM Proyectos")
        proyectos_user = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = session["user_id"])
        solicitudes = db.execute("SELECT * FROM Solicitudes")
        #contar los proyectos aprobados, incompletos y en progreso
        completado = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Completado")
        Incompleto = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Incompleto")
        Progreso = db.execute("SELECT COUNT(Estado)From Proyectos WHERE Estado = :estado",estado = "Progreso")
        imagen = db.execute("SELECT Imagen From Reportes WHERE Id_reporte = :estado",estado = 1)
        total = db.execute("SELECT COUNT(*) FROM Proyectos")
        cuentaComp = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Completado",to = total[0]['COUNT(*)'])
        cuentaPro = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Progreso",to = total[0]['COUNT(*)'])
        cuentaInc = db.execute("SELECT count(*)*100 / :to AS calc From Proyectos WHERE Estado = :est",est = "Incompleto",to = total[0]['COUNT(*)'])
        print(info)
        variable = db.execute("SELECT * FROM Proyectos WHERE Empleado = :user",user = info)
        print(variable)
        return render_template('home.html',var1 = variable,completo = cuentaComp[0]['calc'], progreso = cuentaPro[0]['calc'], incompleto = cuentaInc[0]['calc'], pro = proyectos, proUser = proyectos_user, soli = solicitudes,comp = completado[0]["COUNT(Estado)"],inco = Incompleto[0]["COUNT(Estado)"],prog = Progreso[0]["COUNT(Estado)"], img = imagen)  


@app.route('/facturacion')
def facturacion():
    
     return render_template('facturacion.html')     

@app.route('/RRHH')
def rrhh():
    
     return render_template('RRHH.html') 

@app.route('/planificacion')
def planificacion():
    
     return render_template('planificacion.html')     

@app.route('/ejecucion')
def ejecucion():
    
     return render_template('ejecucion.html')     

@app.route('/ayuda')
def ayuda():
    
     return render_template('ayuda.html')     

if __name__ == '__main__':
 app.run(port = 3000, debug = True)
