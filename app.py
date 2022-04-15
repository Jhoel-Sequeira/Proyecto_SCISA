
from asyncio.windows_events import NULL
from re import S
from flask import Flask, flash, redirect, render_template, request, url_for, session
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

db1 = cs50.SQL("sqlite:///SCISA_DB.db")

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
        # SELECT U.User, U.Contraseña, ur.idRole as Rol FROM Usuario as U inner join UserRole as ur on U.User=ur.idUser Where U.User=:username
        # Query database for username
        # HASHEAR USUARIOS db1.execute("Update Usuario set Contraseña = :userhash WHERE Usuario =:user",
        #             userhash=generate_password_hash("456"), user="Maria.Mendez")
        if usuario == "" or contraseña == "":
            return render_template('login.html', hola=1)
        else:
            rows = db1.execute("SELECT * FROM Usuario Where Usuario=:username",
                               username=usuario)
            if len(rows) == 0 or not check_password_hash(rows[0]["Contraseña"], contraseña):
                return render_template('login.html', hola=1)
            else:
                # Estas consultas son para mostrar la lista de personas y su asistencia
                hi = datetime.now()
                himes = hi.month
                # db.execute('INSERT INTO Registro VALUES (:usuario,:fecha,:salida,:horae,:horas,:trab,:mes)',
                #            usuario=usuario, fecha=datetime.date(hi), salida=NULL, horae=datetime.time(hi), horas=NULL, trab=NULL, mes=himes)
                db1.execute('INSERT INTO RegistroTrabajadores VALUES (:usuario,:fecha,:salida,:horae,:horas,:trab)',
                            usuario=rows[0]["Id_Usuario"], fecha=datetime.date(hi), salida=NULL, horae=datetime.time(hi), horas=NULL, trab=NULL)
                empleado = db1.execute(
                    "select substring(emp.Nombre,1,5) as nom from Empleado as emp INNER JOIN Usuario as u on emp.Id_Empleado = u.IdEmpleado WHERE u.Usuario =:u", u=usuario)
                print(empleado)
                # Recordar el usuario y rol que se logeo
                session["user"] = empleado[0]["nom"]
                session["user_Id"] = rows[0]["Id_Usuario"]
                session["userrole"] = rows[0]["Id_Rol"]
                return redirect(url_for('home'))
    else:
        return render_template("index.html")


@app.route('/asistencia', methods=["GET", "POST"])
def asistencia():
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hi = datetime.now()
    himes = hi.month
    prueba1 = db.execute(
        'select Usuario, Fecha_entrada, Fecha_salida, Hora_entrada, Hora_salida,Horas_trabajadas from Registro where mes = :t ', t=himes)
    asistencia = db.execute(
        'select Usuario, Fecha_entrada, Fecha_salida, Hora_entrada, Hora_salida,Horas_trabajadas from Registro GROUP BY Usuario')

    return render_template('Asistencia.html', mes=meses[himes], listas=prueba1, asist=asistencia, usuario=prueba1[0]["Usuario"])


@app.route('/mostratrasistencia', methods=["GET", "POST"])
def mostrarasistencia():
    if request.method == "POST":
        hi = datetime.now()
        himes = hi.month
        sele = request.form['seleccion']
        user = request.form['seleccion1']
        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        prueba1 = db.execute(
            'select Usuario, Fecha_entrada from Registro where mes = :t AND Usuario = :us', t=int(sele), us=user)
        asistencia = db.execute(
            'select Usuario, Fecha_entrada from Registro GROUP BY Usuario')
        return render_template('Asistencia.html', mes=meses[int(sele)], listas=prueba1, asist=asistencia)

    else:

        return redirect(url_for("index"))


@app.route('/deslog')
def deslog():
    hi = datetime.now()
    himes = hi.month
    db1.execute('UPDATE  RegistroTrabajadores SET FechaSalida = :sal, HoraSalida = :horasal WHERE FechaEntrada = :fe',
                sal=datetime.date(hi), horasal=datetime.time(hi),  fe=datetime.date(hi))
    hora_trabajadas = db1.execute('SELECT (strftime("%s", HoraSalida) - strftime("%s", HoraEntrada))/3600 AS HorasTrab from RegistroTrabajadores WHERE FechaEntrada = :fe',

                                  fe=datetime.date(hi))
    db1.execute('UPDATE  RegistroTrabajadores SET HorasTrabajadas = :ht WHERE FechaEntrada = :fe',
                ht=hora_trabajadas[0]["HorasTrab"],  fe=datetime.date(hi))
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
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")
                imagen = db.execute(
                    "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                return render_template('home.html', var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img=imagen,
                    indice="todo")

            else:
                print("meses")
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT * FROM Solicitudes")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
                imagen = db.execute(
                    "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                print(indice)
                return render_template('home.html', var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=0, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                       img=imagen, pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
            imagen = db.execute(
                "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            return render_template('home.html', var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img=imagen, indice="todo")
    else:
        print("carga")

        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
        imagen = db.execute(
            "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        return render_template('home.html', var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img=imagen)


# mostrar los modals segun su seleccion
@app.route('/modal')
def modal():
    proyectos = db.execute("SELECT * FROM Proyectos")
    permisos = db.execute("SELECT * FROM Solicitudes")
    return render_template('modal.html', pro=proyectos, permiso=permisos)


@app.route('/reporte', methods=["GET", "POST"])
def reporte():
    if request.method == "POST":
        tarea = request.form['tarea']
        porcentaje = request.form['porcentaje']
        descripcion = request.form['descripcion']
        imagen = request.form['imagen']
        print(imagen)
        db.execute("INSERT INTO Reportes VALUES(NULL,:nom,:porcen,:desc,:img)",
                   nom=tarea, porcen=porcentaje, desc=descripcion, img=imagen)
        return redirect(url_for('home'))
    else:
        return redirect(url_for("index"))


@app.route('/solicitud', methods=["GET", "POST"])
def solicitud():
    if request.method == "POST":
        hi = datetime.now()
        titulo = request.form['titulo']
        justificacion = request.form['justificacion']
        db1.execute('INSERT INTO Solicitudes VALUES(null, :nom, :jus, :fech, :titu, :estado, :vi)',
                    nom=session["user_Id"], jus=justificacion, fech=datetime.date(hi), titu=titulo, estado=6, vi=1)
        return redirect(url_for('home'))
    else:

        return redirect(url_for("index"))


@ app.route('/AceptarSoli', methods=["GET", "POST"])
def AceptarSoli():
    if request.method == "POST":
        id = request.form['resp']
        db.execute('UPDATE  Solicitudes SET Estado = :est,Vigente = :vi WHERE Id_Solicitud = :Id',
                   est="Aprobado", vi=0, Id=id)
        db1.execute('UPDATE Solicitudes SET IdEstado = :est,Vigencia = :vi WHERE Id_Solicitud = :Id',
                    est=4, vi=0, Id=id)
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
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")
                imagen = db.execute(
                    "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                variable = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
                # LLAMAR las tareas de cada Proyecto
                print(variable)
                return render_template('home.html', var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img=imagen,
                    indice="todo")

            else:
                print("meses")
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT * FROM Solicitudes")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
                imagen = db.execute(
                    "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                print(indice)
                variable = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
                return render_template('home.html', var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=0, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                       img=imagen, pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
            imagen = db.execute(
                "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            variable = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
            return render_template('home.html', var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img=imagen, indice="todo")
    else:
        print("carga")

        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
        imagen = db.execute(
            "SELECT Imagen From Reportes WHERE Id_reporte = :estado", estado=1)
        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        variable = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
        print(variable)
        return render_template('home.html', var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img=imagen)


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
    proyectos = db.execute("SELECT * FROM Proyectos")

    return render_template('ejecucion.html', pro=proyectos)


@app.route('/ayuda')
def ayuda():

    return render_template('ayuda.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
