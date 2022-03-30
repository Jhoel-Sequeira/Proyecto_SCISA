
from asyncio.windows_events import NULL
from flask import Flask, flash, redirect, render_template, request, url_for,session
from datetime import datetime
import cs50
from cs50 import SQL
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

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
                consult_user = db.execute('SELECT Id_rol FROM credenciales WHERE Usuario = :u', u = usuario)
                session["user_id"] = rows[0]["Id_Usuario"]
                return render_template('home.html',rol = int(consult_user[0]["Id_rol"]),nombre = rows[0]["Usuario"])
        
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

@app.route('/home')
def home():
    
     return render_template('home.html')     

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
