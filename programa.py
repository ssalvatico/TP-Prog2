import sys

def openFile(nombre, carpeta, type):
    ruta = f"./{carpeta}/{nombre}.txt"
    try:
        archivo = open(ruta,type) #Abre el archivo sin errores
        return archivo
    
    except FileNotFoundError:
        print(f"El archivo {ruta} no fue encontrado.") #Error de que no encuentra el archivo
        return None
    
    except Exception as error:
        print(f"Error al abrir el archivo {ruta}: {error}") #Cualquier otro error que no me permita abrir el archivo
        return None

def mayorFrecuencia(lista):
    conteo = {}

    for elemento in lista:
        if elemento in conteo:
            conteo[elemento] += 1
        else:
            conteo[elemento] = 1

    elemento_mas_comun = max(conteo, key=conteo.get)

    return elemento_mas_comun

def verificaMatch(lista1, lista2):
    for i in lista1:
        for j in lista2:
            if i == j:
                return i
    return 0

def ultimoRecurso(valores):
    listaPlana = []
    for elem in valores:
        for subelem in elem:
            listaPlana.append(subelem)
    return mayorFrecuencia(listaPlana)

def actualizadorDict(dicc, valor, clave):
    valores = list(dicc.get(clave, []))
    valores.append(valor)
    dicc[clave] = valores
    return dicc

def almacenadorTexto(nombre):

    archivo = openFile(nombre,"Entradas", "r")
    lineas = archivo.readlines()    

    anterior = {}
    siguiente = {}

    for linea in lineas:
        linea = linea.split()
        length = len(linea)
        
        for i in range(length):
            palabra = linea[i]
            if palabra == '':
                continue
            if i == 0:
                if len(linea) == 1:
                    continue
                else:
                    actualizadorDict(siguiente,linea[i + 1], palabra)
            
            if i > 0 and i < length-1:
                actualizadorDict(anterior, linea[i - 1], palabra)
                actualizadorDict(siguiente, linea[i + 1], palabra)
            
            if i == length-1:
                actualizadorDict(anterior, linea[i-1], palabra)
    
    archivo.close()
    return (anterior, siguiente)

def buscadorDeFrase(nombre):
    anterior, siguiente = almacenadorTexto(nombre)
    entrada = openFile(nombre, "Frases", "r")
    lineas = entrada.readlines()
    salida = openFile(nombre, "Salidas", "w")

    for linea in lineas:
        linea = linea.split()
        length = len(linea)
        
        for i in range(length):
            palabra = linea[i]

            if palabra != "_":
                if i < len(linea)-1:
                    palabra += " "
                elif i == len(linea)-1:
                    palabra += '\n'
                
            if palabra == "_":
                if i == 0:
                    if linea[i+1] in anterior:
                        palabra = mayorFrecuencia(anterior[linea[i + 1]]) + ' '
                    else:
                        palabra = ultimoRecurso(anterior.values()) + ' '

                elif i > 0 and i < length-1:
                    if linea[i+1] in anterior and linea[i-1] in siguiente:
                            comparacion = verificaMatch(anterior[linea[i + 1]],siguiente[linea[i - 1]])
                            if comparacion:
                                palabra = comparacion + ' '
                    
                    if linea[i+1] in anterior:
                        palabra = mayorFrecuencia(anterior[linea[i + 1]]) + ' '
                    
                    if linea[i - 1] in siguiente:
                        palabra = mayorFrecuencia(siguiente[linea[i - 1]]) + ' '
                    
                    else:
                        palabra = ultimoRecurso(anterior.values()) + ' '

                elif i == length-1:
                    if linea[i - 1] in siguiente:
                        palabra = mayorFrecuencia(siguiente[linea[i - 1]]) + '\n'
                    else:
                        palabra = ultimoRecurso(siguiente.values()) + '\n'

            salida.write(palabra)

    entrada.close()
    salida.close()
    return 0



def main():
    if len(sys.argv) != 2:
        print("Numero de argumentos incorrecto")
    else:
        buscadorDeFrase(sys.argv[1])

if __name__ == "__main__":
    main()