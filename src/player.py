
class Player:
    """
    Representa a un jugador, con un nombre y un caracter, con 
    el que juega, en un tablero con la recomendación del oráculo.
    """

    def __init__(self, name: str, char = None, opponent = None, oracle = None)-> None:
        #refactorizo player para que solo necesite como parametro name, Match se encarga de char de ahora en más
        #importo dentro de la función debido a que me generaba un circular import
        if oracle is None:
            from oracle import SmartOracle
            oracle = SmartOracle()
        self._name = name
        self._char = char
        self._oracle = oracle
        self._opponent = opponent
    
    @property
    def name(self):
        return self._name
    
    @property
    def opponent(self):
        """
        Propiedad por la cual podemos acceder
        al oponente de cada player
        """
        return self._opponent
    
    @opponent.setter #para asignar un valor
    def opponent(self, other):
        if other is not None: #Ya que le hemos asignado como valor pred. None hay que especificar q no sea None
            self._opponent = other
            other._opponent = self
    
    def play(self, board: list[list]):
        """
        Elige de entre todas las columnas disponibles, la que contenga
        la mejor jugada (recomendada por el oráculo)
        """
        
        #Obtengo las recomendaciones (utilizo tupla, evito crear una clase para 2 valores)
        (best, _) = self._ask_oracle(board)
        #Metemos ficha en la mejor opción (jugamos)
        self._play_on(board, best.index)
    
    def _play_on(self, board: list[list], position: int):
        """
        Jugamos en la posición dada (position)
        """
        board.add(self._char, position) #metemos el player_char en la posición
    
    def _ask_oracle(self, board):
        """
        Pregunta al oráculo y devuelve la mejor opción
        """
        recommendations = self._oracle.get_recommendation(board, self)
        best = self._choose(recommendations)
        return (best, recommendations) #refactorizado, mucho más sencillo
    
    def _choose(self, recommendations):
        """
        Se encarga de seleccionar la mejor jugada según 
        las recomendaciones
        """
        from oracle import ColumnClassification
        # Delegar en SmartOracle si tiene _choose_best
        if hasattr(self._oracle, '_choose_best'):
            valid = [r for r in recommendations if r.classification != ColumnClassification.FULL]
            return self._oracle._choose_best(valid)
        valid = list(filter(lambda x: x.classification != ColumnClassification.FULL, recommendations))
        return valid[0]
    
class HumanPlayer(Player):
    
    def __init__(self, name: str, char: str = None): #solo le va a pasar su nombre, Match se encarga de asignar char
        
        super().__init__(name, char) #es su especie de "oraculo"

    def _ask_oracle(self, board):
        """
        Mediante un bucle infinito le preguntamos al humano qué
        jugada quiere realizar. En el bucle se valida su decisión,
        si está dentro de lo aceptado, sale del bucle SINO
        el bucle se repite hasta que de una respuesta valida.
        """
        from oracle import ColumnRecommendation
        while True: #inicializamos el bucle infinito
            answer = input(f"  [{self._name}] Elige columna (0-{len(board)-1}): ")
            if _is_int(answer) and _is_in_column_range(board, int(answer)) and _not_full_column(board, int(answer)): 
                #si pasa los and, entonces tomamos su respuesta como una posición
                position = int(answer)
                return (ColumnRecommendation(position, None), None) #None ya que el humano elije x si mismo
            print("  ⚠  Columna inválida, intenta de nuevo.")
        


#Funciones de validacion de índice de columna
def _not_full_column(board, num):
    """
    Nos ayuda a validar jugadas humanas. Identifica que 
    la columna seleccionada NO esté llena y avala la jugada.
    """
    #obtengo la columna especifica (num) y utilizamos is_full() para determinar si está llena o no
    return not board.is_full(num)
    
def _is_in_column_range(board, num):
    """
    Nos ayuda a validar jugadas humanas. Identifica que 
    la columna seleccionada esté dentro del rango de board.
    """
    return 0 <= num < len(board)

def _is_int(string)-> bool:
    """
    Nos ayuda a validar jugadas humanas. Identifica que 
    el string insertado represente un entero únicamente.
    """
    try:
        int(string)# convierte en un int "puro"
        return True
    except:
        return False #era cualquier otra cosa (otro string, un float, una función) y no la puede convertir a int