def check_parada(cur,parada):
    cur.execute(f"SELECT autorizar FROM tabla_index WHERE nombre = '{parada}' ")
    check=cur.fetchall()
    for valor in check:
        if valor[0] == 'autorizada':
            return True
        else: 
            return False
    
def listado_paradas(cur):
    cur.execute("SELECT nombre FROM tabla_index")  
    db_paradas=cur.fetchall()     
    return db_paradas

def info_parada(cur,parada):
    cur.execute(f"SELECT codigo,nombre,direccion,municipio,provincia,zona,cuota,pago,banco,num_cuenta,federacion,geolocalizacion FROM  tabla_index  WHERE nombre='{parada}'" )
    infos=cur.fetchall()     
    return infos

def info_cabecera(cur,parada):          
    cur.execute(f'SELECT nombre FROM {parada}')
    seleccion=cur.fetchall()
    cant=len(seleccion)  
    presidente = []       
    cur.execute(f"SELECT nombre FROM {parada}  WHERE funcion = 'Presidente'")   
    press=cur.fetchone()
    if press != None:  
     for pres in press:   
        presidente=pres
    else:     
       presidente='No disponible'   
    veedor = []
    cur.execute(f"SELECT nombre FROM {parada}  WHERE funcion = 'Veedor'")   
    presd=cur.fetchone()
    if presd != None:
     for prex in presd:
       veedor=prex 
    else:
        veedor='No disponible'           
    return cant,presidente,veedor                
     
def lista_miembros(cur,parada):
    listas=[]
    cur.execute(f"SELECT id,nombre,cedula,telefono,funcion  FROM {parada}")
    miembros=cur.fetchall()
    for miembro in miembros:     
        listas+=miembro    
    lista=dividir_lista(listas,5)    
    return lista
    
def diario_general(cur,parada):
    prestamos=[]
    ingresos=[]
    gastos=[]
    aporte=[]
    pendiente=[]
    abonos=[]
    balance_bancario=[]
    cur.execute(f"SELECT  prestamos, ingresos, gastos, aporte, pendiente, abonos, balance_banco FROM tabla_index WHERE nombre='{parada}' " )  
    consult=cur.fetchall()
    for valor in consult:
      prestamos=valor[0]
      ingresos=valor[1]
      gastos=valor[2]
      aporte=valor[3]
      pendiente=valor[4]
      abonos=valor[5]
      balance_bancario=valor[6]
    balance=(aporte + ingresos + abonos )-(gastos+prestamos)
    data=(balance,prestamos,ingresos,gastos,aporte,pendiente,abonos,balance_bancario)   
    return data

def pendiente_aport(cur,parada):
    var1=[]
    var2=[]
    cur.execute(f"SHOW TABLES LIKE '{parada}_cuota'")
    vericar=cur.fetchall()
    if vericar !=[]:
      vgral=[]
      cur.execute(f"SELECT nombre FROM {parada}")
      list_nomb=cur.fetchall()
      for nombre in list_nomb:
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' and nombre='{nombre[0]}'") 
         var_x = cur.fetchall()
         for var_p in var_x:
              var1=var_p[0]
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' and nombre='{nombre[0]}'")
         var_z = cur.fetchall()
         for var_n in var_z:
              var2=var_n[0]   
         sub_t=var1+var2
         if sub_t != 0 :    
          avg=round((var1/sub_t)*100,2)
         else:
          avg = 0.00               
         vgral+=(nombre[0],var1,var2,sub_t,avg) 
      list_1=dividir_lista(vgral,5)                    
      return list_1
    else:
      return [] 




def dividir_lista(lista,lon) : 
    return [lista[n:n+lon] for n in range(0,len(lista),lon)]     


def aportacion(cur,parada):           
    cur.execute(f"SELECT codigo, nombre, cedula, telefono, funcion FROM {parada}")
    data=cur.fetchall()
    return data
  
def verif_p(cur,parada,cedula):
    cur.execute(f"SELECT * FROM {parada} WHERE  cedula = '{cedula}'")                                       
    accounts =cur.fetchall()
    if accounts != []:
         return True
    else:
         return False 
     
def nombres_miembro(cur,parada):
        listado=[]
        cur.execute(f"SELECT nombre FROM {parada} ")
        nombres=cur.fetchall()
        for nombre in nombres:
            listado += nombre
        return listado 
    
def info_personal(cur,parada,cedula):
    if parada !=[] and cedula !=[] :
      nombre = []
      cur.execute(f"SELECT nombre FROM {parada} WHERE cedula='{cedula}'")   
      nombres=cur.fetchall()
      for nombre in nombres: 
       return nombre[0]
    else:
      return []  

def verificar_prestamo(cur,parada,cedula):
    cur.execute(f"SHOW TABLES LIKE '{parada}_cuota'")
    vericar=cur.fetchall()
    if vericar !=[]:    
    
        prestado=[]    
        nombre=[]
        cur.execute(f"SELECT nombre FROM {parada} WHERE cedula = '{cedula}'") 
        nombres = cur.fetchall()
        for pers in nombres:
            nombre=pers[0]
        cur.execute(f"SELECT fecha,monto_prestamo FROM {parada}_prestamos WHERE prestamo_a ='{nombre}'") 
        prestamo=cur.fetchall()
        if prestamo !=[]:
           for prestado in prestamo:   
             return (f"usted tomo un prestamo en fecha {prestado[0]},por un monto de {prestado[1]}RD$") 
        else:
           return 'No tiene prestamo a este momento'
    else:
        return 'No hay registro de prestamo para usted en esta parada'


def verificar_abonos(cur,parada,cedula,prestamo):
    if (str(prestamo) != 'No tiene prestamo a este momento' ) or (str(prestamo) !='No hay registro de prestamo en esta parada'):
        
       return  'Tiene abonos pendientes de su deuda'
    else:
        return 'No teneno deuda registrada de usted en nuestros archivo'
    
    
def hist_pago(cur,parada,nombre,cedula): 
    var1=[] 
    var2=[] 
    cur.execute(f"SHOW TABLES LIKE '{parada}_cuota'")
    vericar=cur.fetchall()
    if vericar !=[]:
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' and nombre='{nombre}'") 
         var_x = cur.fetchall()
         for var_p in var_x:
              var1=var_p[0]
         cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' and nombre='{nombre}'")
         var_z = cur.fetchall()
         for var_n in var_z:
              var2=var_n[0]   
         sub_t=var1+var2
         if sub_t != 0 :    
          avg=round((var1/sub_t)*100,2)
         else:
            avg = 0.00                                           
         return (f" {sub_t} cuotas usted a pagado {var1} cuotas y tiene pendiente de pagar {var2} cuotas  por tanto su promedio de pago es de { avg}%",avg) 
    else:
      return ' de 0 cuotas no hay cuotas en atraso',0  
    
def visibilidad(pagos):
    if float(pagos) > 49 :
      return 'ver'   
    else:
        return 'no_ver'
    
def dat_miembros(cur,parada,miembro):
    cur.execute(f"SELECT nombre,cedula,telefono,funcion FROM {parada} WHERE nombre='{miembro}'")
    listado=cur.fetchall()
    return listado

def vef_cedula(cur,cedula):
  lista_paradas=[]  
  cur.execute("SELECT nombre FROM tabla_index")  
  db_paradas=cur.fetchall()    
  for parada in db_paradas:
      lista_paradas+=parada   
  for parada in lista_paradas:
      cur.execute(f"SELECT nombre FROM {parada} WHERE cedula='{cedula}'")
      nombre=cur.fetchall()
      if nombre !=[]:            
        print(parada)
        return parada
              
  return []    