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
        #if venta["CLIENTE"] == cliente:
            #productos.append(venta["PRODUCTO"]) #Solo le paso el producto vendido
            productos.append(venta) #Le paso toda la linea de la venta con los datos
    return productos

# Funcion para Clientes por Producto #################################################
def clientesPorProducto(ventas, producto):
    clientes = [] #armo la lista vacia.
    for venta in ventas:
        if producto.lower() in venta["PRODUCTO"].lower():
        #if venta["PRODUCTO"] == producto:
            clientes.append(venta["CLIENTE"])
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
                valor = valor + int(venta["PRECIO"])*int(venta["CANTIDAD"])
        resultado[j] = valor

    resultado = sorted(resultado.items(), key = lambda t:t[1], reverse=True)

    return resultado

### AGREGAR VENTA ####################################################################
def agregarventa(cod, prod, clien, prec, cant):
    archivoleer = open('datos.csv','r')
    archivoesc = open('datos.csv','a', newline='')
    archivoesc = csv.writer(archivoesc)
    tablacsv = csv.DictReader(archivoleer)
    cod = cod.upper()
    prod = prod.title()
    clien = clien.title()

    ord = tablacsv.fieldnames
    dicc = {"CODIGO":cod,"PRODUCTO":prod,"CLIENTE":clien,"PRECIO":prec,"CANTIDAD":cant}
    formulario = []
    for i in range(len(tablaorden)):
        formulario.append(dicc[ord[i]])

    archivoesc.writerow(formulario)
    return
### AGREGAR VENTA ####################################################################




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
