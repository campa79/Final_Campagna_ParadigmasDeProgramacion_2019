from pprint import pprint
import sys
import csv

# Definición que uso para validar el codigo de 3 letras y 3 números
def validarCodigo(codigo):
    if len(codigo) != 6:
        return False

    primeraTerna = codigo[0:3]
    segundaTerna = codigo[3:7]

    if not primeraTerna.isalpha():
        return False

    if not segundaTerna.isdigit():
        return False

    return True

# Definición para cargar el archivo
def loadcsv(filename):
    try:
        fo=open(filename, "r")
    except:
        print("No se pudo abrir el archivo:", filename)
        return None

    linea1 = fo.readline()
    linea1 = linea1.strip()
    encabezados = linea1.split(",")

    ventas = [] #armo lista vacia
    for linea in fo.readlines():
        datos = linea.strip().split(",")

        if len(datos) != len(encabezados):
            print("El archivo contiene linea inválida.")
            print(linea)
            return None

        venta = {} #diccionario vacio
        for i in range(len(datos)): #iterar todo el archivo
            clave = encabezados[i]
            valor = datos[i]
            venta[clave] = valor

        if not venta["CODIGO"]:
            print("El archivo contiene una venta sin código.")
            print(linea)
            return None

        if not validarCodigo(venta["CODIGO"]):
            print("El archivo contiene un código no válido.")
            print(venta["CODIGO"])
            return None

        try:
            venta["CANTIDAD"] = int(venta["CANTIDAD"]) #lo paso a int
        except:
            #if not isinstance(venta["CANTIDAD"], int):
            print("El archivo contiene una cantidad no entera.")
            print(venta["CANTIDAD"])
            return None

        try:
            venta["PRECIO"] = float(venta["PRECIO"]) #lo paso a float
        except:
            print("El archivo contiene un precio no válido.")
            print(venta["PRECIO"])
            return None

        ventas.append(venta)
    return ventas

# Funcion para Productos por Cliente #################################################
def productosPorCliente(ventas, cliente):
    productos = [] #armo la lista vacia.
    for venta in ventas:
        if cliente.lower() in venta["CLIENTE"].lower():
            productos.append(venta) #Le paso toda la linea de la venta con los datos
    return productos

# Funcion para Clientes por Producto #################################################
def clientesPorProducto(ventas, producto):
    clientes = [] #armo la lista vacia.
    for venta in ventas:
        if producto.lower() in venta["PRODUCTO"].lower():
            clientes.append(venta)
    return clientes

# Funcion para Productos Mas Vendidos ################################################
def productosMasVendidos(f):

    ventas = list(csv.DictReader(f))
    tablanombres = [] #armo la lista vacia.
    resultado = {}

    for i in ventas:
        tablanombres.append(i["PRODUCTO"])
    tablanombres = list(set(tablanombres))
    print(tablanombres)

    for j in tablanombres:
        valor = 0
        for venta in ventas:
            if venta["PRODUCTO"] == j:
                valor = valor + int(venta["CANTIDAD"])
        resultado[j] = valor

    resultado = sorted(resultado.items(), key = lambda t:t[1], reverse=True)

    return resultado

# Funcion para Clientes por Gastos ###################################################
def clientesMasGastaron(f):

    ventas = list(csv.DictReader(f))
    tablanombres = [] #armo la lista vacia.
    resultado = {}

    for i in ventas:
        tablanombres.append(i["CLIENTE"])
    tablanombres = list(set(tablanombres))
    print(tablanombres)

    for j in tablanombres:
        valor = 0
        for venta in ventas:
            if venta["CLIENTE"] == j:
                valor = valor + float(venta["PRECIO"])*int(venta["CANTIDAD"])
        resultado[j] = valor

    resultado = sorted(resultado.items(), key = lambda t:t[1], reverse=True)

    return resultado

################################################ AGREGAR VENTA #######################################

#Defino el orden de la tabla para Agregar ventas / Agregado para el Final.
tablaordenada = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]

def nuevaventa(cod, prod, clien, prec, cant):
    readfile = open('datos.csv','r') #Leo el archivo datos.csv
    writefile = open('datos.csv','a', newline='') #agrego el salto de línea para escribirlo
    writefile = csv.writer(writefile)
    tablacsv = csv.DictReader(readfile)
    cod = cod.upper() #Pongo el código con mayúsculas
    prod = prod.title()
    clien = clien.title()

    ord = tablacsv.fieldnames
    dicc = {"CODIGO":cod,"PRODUCTO":prod,"CLIENTE":clien,"PRECIO":prec,"CANTIDAD":cant} #Armo el diccionario
    formulario = []
    for i in range(len(tablaordenada)):
        formulario.append(dicc[ord[i]])

    writefile.writerow(formulario)
    return
################################################ AGREGAR VENTA #######################################


###################### CHEQUEOS PARA AGREGAR VENTA ##################################################
def ventacheck(cod, prod, clien, prec, cant):
    lista = []
    dicc = {"Código":cod,"Producto":prod,"Cliente":clien,"Precio":prec,"Cantidad":cant}
    for i in dicc:
        if dicc[i] == "" or dicc[i].isspace():
            lista.append(f"Debes completar el campo {i}.")
    if len(lista) >= 1:
        return lista

    if len(prod) < 3:
        lista.append("El Producto tiene que tener mas de 3 caracteres. Ingresar nuevamente.")

    if len(clien) < 3:
        lista.append("El Cliente tiene que tener mas de 3 caracteres. Ingresar nuevamente.")

    if not (cod[0:3].isalpha()) or not (cod[3:6].isnumeric()) or len(cod)!=6:
        lista.append("El Código debe tener 3 letras y 3 números. Ingresar nuevamente.")

    #Salida del IF para cuando la venta ingresada cumple todos los requisitos
    #if (cod[0:3].isalpha()) and (cod[3:6].isnumeric()) and len(cod)!=6 and len(clien) < 3 and len(prod) < 3:
        #lista.append("Venta ingresada con éxito.")

    try:
        if not float(prec):
            lista.append("El Precio debe ser un número. Ingresar nuevamente.")
    except ValueError:
        lista.append("El precio no es un numero. Ingresar nuevamente.")

    try:
        if not float(cant).is_integer():
            lista.append("La Cantidad debe ser un número. Ingresar nuevamente.")
    except ValueError:
        lista.append("La Cantidad no es un numero. Ingresar nuevamente")
    return lista
###################### CHEQUEOS PARA AGREGAR VENTA ##################################################

#############################################################################
##################### Códigos de prueba para consola ########################
#############################################################################

if __name__ == '__main__': #codigo de prueba
    ventas = loadcsv("datos.csv")

    if ventas == None:
        print("El archivo CSV es incorrecto.")
        sys.exit()

    #pprint(ventas)
    #print(ventas[3]["CODIGO"])
    misProductos = productosPorCliente(ventas,"Alberto Campagna")
    print(misProductos)

    misClientes = clientesPorProducto(ventas,"BCD Mares")
    print(misClientes)
