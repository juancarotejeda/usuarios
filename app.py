import mysql.connector,funciones,os
from flask import Flask, render_template,flash, request,  redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key=os.getenv("APP_KEY")
DB_HOST =os.getenv('DB_HOST')
DB_USERNAME =os.getenv("DB_USERNAME")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_NAME =os.getenv("DB_NAME")

# Connect to the database
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME,
    autocommit=True
)

@app.route("/")
def login():   
    cur = connection.cursor() 
    resultado=funciones.listado_paradas(cur)
    paradas=[]
    for paradax in resultado:
       paradas+=paradax  
    cur.close()                   
    return render_template('login.html',paradas=paradas)

@app.route("/verificador", methods=["GUET","POST"])
def verificador(): 
   msg = ''   
   if request.method == 'POST':        
    cedula = request.form['cedula']  
    cur = connection.cursor() 
    parada=funciones.vef_cedula(cur,cedula)   
    print(parada)
    if parada!= []:                                                                             
            fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H")            
            informacion = funciones.info_parada(cur,parada) 
            cabecera = funciones.info_cabecera(cur,parada) 
            nombre =  funciones.info_personal(cur,parada,cedula)
            prestamo = funciones.verificar_prestamo(cur,parada,cedula)
            miembros = funciones.lista_miembros(cur,parada)                
            diario = funciones.diario_general(cur,parada) 
            cuotas_hist = funciones.pendiente_aport(cur,parada)
            #abonos = funciones.verificar_abonos(cur,parada,cedula,prestamo)
            pagos = funciones.hist_pago(cur,parada,nombre,cedula)
            mostrar = funciones.visibilidad(pagos[1])
            cur.close()
            return render_template('index.html',informacion=informacion,cabecera=cabecera,fecha=fecha,miembros=miembros,diario=diario,cuotas_hist=cuotas_hist,nombre=nombre,prestamo=prestamo,pagos=pagos,mostrar=mostrar)                 
    else:
        msg = 'cedula no esta registrada!'        
        flash(msg)           
        return redirect(url_for('login'))    
            
@app.route("/canal")
def canal():
    return render_template('canal_motoben.html')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
