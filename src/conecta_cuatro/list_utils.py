from typing import Any
from settings import VICTORY_STREAK
def find_streak(haystack, needle, VICTORY_STREAK):
    are_consecutive = False

    if VICTORY_STREAK <= 0:
        are_consecutive = False
        
    contador = 0
    for element in haystack:
        if element == needle:
            are_consecutive = True
            contador += 1
            if contador == VICTORY_STREAK:
                break
        else:
            #este es opcional se puede quitar ya que es implicito, si no es igual a la
            #aguja se queda en falso y contador se resetea a 0
            are_consecutive = False
            contador = 0
    return contador == VICTORY_STREAK


def get_nths(matrix: list[list[str | None]] , n):
    """
    Recibe un matriz y devuelve una lista con el elemento en la posición n de cada sublista
    Si la sublista no tiene indice n coloca None
    """
    result = []  

    # recorremos cada sublista dentro de la matriz
    for sublist in matrix:

        
        if n < len(sublist):
            value = sublist[n]   # sí existe cogemos el valor
        else:
            value = None         # si no ponemos None

        result.append(value)     

    return result


def transpose(matrix: list[list[str | None]]) -> list[list[str | None]]:
    """
    Devuelve la matriz transpuesta usando get_nths.
    Convierte columnas en filas.
    """
    transposed = []
    # Compruebo si existe y no esta vacia
    if matrix and matrix[0]:
        # Repito tantas veces como elementos tiene la primera fila (o columna) de la matriz  
        for element in range(len(matrix[0])): 
            # Añado  
            transposed.append(get_nths(matrix, element))

    return transposed

def add_prefix(elements: list, number: int, filler: Any)-> Any:
    """
    Recibe una lista y devuelve una nueva lista con number rellenos
    al principio (un prefijo)
    Por ej: add_prefix([1,2],2, None) -> [None, None, 1, 2]
    """
    return ([filler]* number) + elements

def add_suffix(elements: list, number: int, filler: Any)-> Any:
    """
    Recibe una lista y devuelve una nueva lista con number rellenos
    al final (un sufijo)
    Por ej: add_suffix([1,2],2, None) -> [1, 2, None, None]
    """
    return elements + ([filler] * number)

def displace_list(elements: list, distance: int, total_size: int, filler: Any)-> list:
    """
    Crea una nueva lista de tamaño total_size, con la original, desplazada
    hacia el final distance posiciones.
    Los espacios nuevos se rellenan con filler.
    Ej: displace_list([1,2,3], 1, 7, None)-> [None, 1, 2, 3, None, None, None]
    Esto quiere decir que la lista tendrá una longitud total de 7 
    y la original la movemos 1 posicion
    """
    #debemos desplazar la lista original distance posiciones hacia la -> derecha
    #rellenar el resto de espacios (que falten hasta 7) con un filler
    #cuantos fillers necesito antes y cuantos despues de elements?

    prefix_needed = distance #los que van antes de elements serán iguales a la distance que desplazamos

    #para suffix necesitamos el tamaño final (7), el desplazamiento y el tamaño de la lista original
    suffix_needed = total_size - distance - len(elements)

    prefix_list = add_prefix(elements, prefix_needed, filler)
    final_list = add_suffix(prefix_list, suffix_needed, filler)

    return final_list

# add_prefix(elements, prefix_needed, filler) + add_suffix(elements, suffix_needed, filler)
#no sirve porque duplica a elements

def displace_lol(lol: list[list], total_size: int, filler: Any):
    displaced_lol = []
    for i, sublist in enumerate(lol):
        displaced_lol.append(displace_list(sublist, i, total_size, filler))
    return displaced_lol

def reversed_list(l: list):
    """
    Utilizamos REVERSED y no reverse, ya que la segunda modifica la lista 
    original y la primera devuelve un iterador de reversed por lo que debemos indicar
    que queremos que nos devuelva una lista nueva, revertida.
    """
    return list(reversed(l)) #poniendole list delante obtenemos la lista

def reversed_matrix(lol: list[list]):
    changed = []
    for ls in lol:
        changed.append(reversed_list(ls))
    return changed
    
