import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
clients_ref = db.collection('clients')

def search_and_confirm():
    id_query = input('Introduce el DNI del registro que necesites: ')
    result = clients_ref.document(id_query).get()
    if result.exists:
        print(f'¿Este es el cliente que busca?: {result.to_dict()}')
        confirmation = input('Pulsa s para confirmar: ') == 's'
        if confirmation:
            return id_query
        else: 
            print('Operación cancelada')
            return False
    else:
        print('No se ha encontrado ningún cliente')

def doct_menu():
    print('''¿Qué quieres hacer?
    1 - Actualizar un registro || 2 - Añadir información básica a un registro || 3 - Borrar un registro || 4 - Consultar un registro || 5 - Consultar todos los registros || 6 - Salir''')
    doct_option = input ('selecciona una opción: ')
    switch_options(doct_option)

def add_info(option, id):

    if option == '1':
        wise_tooth = input('¿Paciente está operado de muelas del juicio? Seleccione si (s) o no (n): ')
        if wise_tooth == 's':
            clients_ref.document(id).update({'wise_tooth' : True})
        elif wise_tooth == 'n':
            clients_ref.document(id).update({'wise_tooth' : False})
        else:
            print('Operación cancelada')

    elif option == '2': 
        teeth = input('Introduce el número de dientes: ')
        clients_ref.document(id).update({'teeth_number' : teeth}) 

    elif option == '3':   
       tooth_caries = input('Introduce el diente que tenga caries: ') 
       clients_ref.document(id).update({'caries' : firestore.ArrayUnion([tooth_caries])})

    elif option == '4':
        treatment = input('Introduce el nombre del tratamiento: ') 
        start_date = input('Fecha de inicio del tratamiento: ')
        finish_date = input('Fecha de fin del tratamiento: ')
        clients_ref.document(id).update({'treatment' : firestore.ArrayUnion([{'name': treatment, 'start': start_date, 'finish': finish_date}])}) 

def switch_options(doct_option):
    if doct_option == '1':       
        id_query = search_and_confirm()
        if id_query:
            key_update = input('¿Qué campo quieres actualizar?: ')
            value_update = input('¿Cuál es el nuevo valor?: ' )
            clients_ref.document(id_query).update({key_update : value_update})
            print(f'Nuevo valor para {key_update}: {value_update}') 

    elif doct_option == '2':   
        id_query = search_and_confirm()
        if id_query:
            print('''¿Qué información quiere añadir?
            Pulse 1 para añadir información sobre las muelas del juicio
            Pulse 2 para añadir información sobre número de dientes
            Pulse 3 para añadir información sobre caries
            Pulse 4 para añadir información sobre tratamientos''')
            option = input('Opción: ')
            add_info(option, id_query)          

    elif doct_option == '3':
        id_query = search_and_confirm()
        if id_query:
            second_confirm = input('¿Seguro qué quiere borrar este registro? Pulse s de nuevo para confirmar: ') == 's'
            if second_confirm:
                clients_ref.document(id_query).delete()
                print('Registro borrado')    

    elif doct_option == '4':
        id_query = input('Introduce el DNI del registro que necesites consultar: ')
        result = clients_ref.document(id_query).get()
        print(f'{result.id}=> {result.to_dict()}')  

    elif doct_option == '5':
        results = clients_ref.stream()
        for result in results:
            print(f'{result.id}=> {result.to_dict()}')            

    elif doct_option == '6':  
        print('Adiós')
        exit()          

    else:
        print('Selecciona una opción del 1 al 4')      

print("Bienvenido/a a la Clínica Baudental")

main_rol = input("¿Eres cliente o dentista? Pulsa 1 para cliente o 2 para dentista: ")

if main_rol=='1':
    name = input ("Introduce tu nombre: ")
    last_name = input("Introduce tu apellido: ")
    id = input("Introduce tu DNI: ")
    phone = input("Introduce tu teléfono: ")
    email = input("Introduce tu email: ")
    clients_ref.document(str(id)).set({'dni': id, 'name':name, 'last_name':last_name, 'phone':phone, 'email':email})
    print('registro creado')

elif main_rol=='2':    
    while True:    
        doct_menu()    
else: 
    print('Cerrando') 
