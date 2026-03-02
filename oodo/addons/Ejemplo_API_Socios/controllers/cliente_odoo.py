import xmlrpc.client

# Configuracion
url = "http://localhost:8069"
db = "izan"
username = "izanbelcam@icloud.com"
password = "1607" 

try:
    # Autenticacion mediante servicio common
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    if uid:
        print(f"Conexion exitosa. UID: {uid}")
        
        # Bucle de ejecucion continua hasta escribir sortir
        while True:
            entrada = input("Ordre > ").strip()
            
            if entrada.lower() == "sortir":
                break
            
            try:
                # Procesamiento de la cadena de entrada
                partes = entrada.split(",")
                comando = partes[0].strip()
                
                # Operacion: Crear
                if comando == "Crear":
                    # Extraer nombre y num_socio limpiando comillas y espacios
                    nombre = entrada.split('nombre=')[1].split(',')[0].replace('"', '').replace("'", "").strip()
                    ref_socio = entrada.split('num_socio=')[1].split(',')[0].replace('"', '').replace("'", "").strip()
                    
                    nuevo_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
                        'name': nombre,
                        'ref': ref_socio  # Mapeo de num_socio a ref
                    }])
                    print(f"Resposta: Soci creat amb exit en Odoo (ID: {nuevo_id}).")

                # Operacion: Consultar
                elif comando == "Consultar":
                    ref_buscada = entrada.split('num_socio=')[1].replace('"', '').replace("'", "").strip()
                    socios = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                        [[['ref', '=', ref_buscada]]], {'fields': ['name', 'ref']})
                    
                    if socios:
                        s = socios[0]
                        print(f"Resposta: Dades d'Odoo -> Nom: {s['name']} | Referencia: {s['ref']}")
                    else:
                        print("Resposta: No se ha encontrado el socio.")

                # Operacion: Borrar
                elif comando == "Borrar":
                    ref_buscada = entrada.split('num_socio=')[1].replace('"', '').replace("'", "").strip()
                    ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['ref', '=', ref_buscada]]])
                    
                    if ids:
                        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [ids])
                        print(f"Resposta: Soci amb referencia {ref_buscada} eliminat.")
                    else:
                        print("Resposta: Error, el soci no existeix.")

                else:
                    print("Resposta: Orden no soportada.")

            except Exception:
                # Si el formato de los parametros es incorrecto
                print("Resposta: Orden no soportada.")

    else:
        print("Error: Credenciales incorrectas.")

except Exception as e:
    print(f"Error de conexion: {e}")