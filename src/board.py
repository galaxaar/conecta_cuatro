from settings import BOARD_COLUMNS, BOARD_ROWS, VICTORY_STREAK
type MatrixColumn = list[list[str|None]]
from copy import deepcopy
from list_utils import find_streak, transpose, displace_lol, reversed_list, reversed_matrix

class Board:
    """
    Representa un tablero con las dimensiones de settings. 
    Detecta una victoria
    Jugador A = representado por x
    Jugador B = representado por o
    Espacio vacío = sin jugada alguna, representado por None
    """   
    # metodos de clase
    @classmethod
    def from_list(cls, list_repr: MatrixColumn):
        board = cls()
        board._columns = deepcopy(list_repr)
        return board
    
    #dunders __x__
    def __init__(self):
        """
        Crea un tablero con las dimensiones adecuadas -OK
        El tablero es una "matriz" de carecteres de jugador 
        y None representa una posición vacía
        Cada lista es una columna y el fondo es el principio
        """
        #cada elemento de self._columns es una columna
        
        self._columns : MatrixColumn = [] #lista vacía

        for col_num in range(BOARD_COLUMNS): # 1er bucle: cada iteración (las 4) genera = [[], [], [], []]
            self._columns.append([])
            for row_num in range(BOARD_ROWS): #2do bucle: acá metemos 4 veces (board_rows) el elemento None
                self._columns[col_num].append(None) #[col_num] representa cada lista vacia creada
                # esto seria = [[None, None, None, None], [None, None, None, None] x cada vez que se meta en col_num]
    # self._columns = lista de columnas
    # self._columns[col_num] = es la columna actual 

    def __eq__(self, value: object)-> bool:
        """
        Se ejecuta cuando haces a == b
        siendo a `self`y b `value`
        """
        result = True
        if not isinstance(value, self.__class__):
            result = False
        else:
            #son de la misma clase: comparo sus propiedades
            #en este caso, _columns
            result = (self._columns == value._columns)
        return result
    
    def __hash__(self)-> int:
        return hash(self._columns)
        
    def __repr__(self)-> str:
        """
        Devuelve representacion textual del objeto: las columnas
        """
        #return f"{self.__class__}: {self._columns}" PROBAR MAS TARDE!!!!!!!!!!!!!!!
        return f"< Board:/n{(self._columns)}>"
    
    def __len__(self):
        """
        Método "mágico" para devolver la longitud de un objeto
        sin tener que depender de importar BOARD_LENGHT
        """
        return len(self._columns)
        
    # Interfaz pública
    def print_board(self, matrix_init: MatrixColumn)->str:
        """ 
        Devuelve un board visual en la terminal transformando
        los elementos de las columnas en strings.
        Para los espacios vacíos (sin jugadas) None, se 
        representa con " - "
        """
        matrix = transpose(matrix_init)
        new_matrix = ""
        characters = ""
        for sublist in matrix[::-1]:
            for element in sublist:
                if element == None:
                    characters += " - "
                else:
                    characters += " " + element + " "
            new_matrix += f"{characters}\n"
            characters = ""
        return new_matrix
    
    def add(self, player_char: str, col_number: int)-> None: 
        """
        Método impuro solo lleva a cabo efecto secundarios
        (cambia el tablero)
        Si col_number no es válido, debe de lanzar una excepción
        ValueError si la columna está llena o si el indice 
        es de una columna inexistente
        """
        try:
            #selecciona la columna ESPECIFICA
            column = self._columns[col_number]
            if not self.is_full(col_number): #si no está llena
                for index, item in enumerate(column):
                    if item == None: #y hay un slot vacío
                        column[index] = player_char #juego aqui("cae la ficha")
                        break
            
        except IndexError:
            raise ValueError(f"{col_number} no es válido") #si me pasan una columna inexistente
    
    def is_full(self, index):
        """
        Predicado que devuelve,a partir de un indice, si X columna
        de sself._columns está llena o no. 
        Si el último elemento de la columna es diferente
        a None, entonces está lleno (es decir True).
        """
        return self._columns[index][-1] != None
    
    #Interfaz privada
    def is_victory(self, player_char: str)-> bool:
        """
        Determina si hay una victoria para el jugador
        representado por un caracter
        """
        return (self._has_vertical_victory(player_char, self._columns) or
                self._has_horizontal_victory(player_char, self._columns) or
                self._has_ascending_victory(player_char, self._columns) or
                self._has_descending_victory(player_char, self._columns))
    
    def _has_vertical_victory(self, player_char: str, matrix: MatrixColumn) -> bool: 
        result = False 
        for column in matrix:
            result = find_streak(column, player_char, VICTORY_STREAK)
            if result:
                break
        return result
    
    def _has_horizontal_victory(self, player_char: str, matrix: MatrixColumn)-> bool:
        """
        Transforma y vencerás!
        Transforma la matriz del tablero para cambiar una victoria horizontal 
        en una vertical y entonces llama a has_vertical_victory
        """
        inverted_matrix = transpose(matrix)
        
        return self._has_vertical_victory(player_char, inverted_matrix)
    
    def _has_ascending_victory(self, player_char: str, matrix: MatrixColumn)-> bool:
        #lo convierto en columnas
        rows = transpose(matrix)
        #lo convierto en una victorial horizontal
        extended = displace_lol(rows, 7, None)
        #devuelvo la victoria horizontal
        return self._has_horizontal_victory(player_char, extended)
        

    def _has_descending_victory(self, player_char: str, matrix: MatrixColumn)-> bool:
        #lo transfromo en columnas
        rows = transpose(matrix)
        #lo convierto en una victoria ascendente ("damos vuelta" el tablero)
        up_side_down_matrix = reversed_matrix(rows)
        return self._has_ascending_victory(player_char, up_side_down_matrix)