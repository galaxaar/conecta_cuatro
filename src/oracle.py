from enum import Enum
from copy import deepcopy
from board import Board
from player import Player
from settings import BOARD_COLUMNS, BOARD_ROWS
import random

# Clases de columna
class ColumnClassification(Enum):
    FULL = -1 #imposible
    LOSE = 1 #derrota inminente
    BAD = 5 #Muy indeseable
    MAYBE = 10 #Indeseable
    WIN = 100 #Victoria inmediata 


# Recomendación de una columna: indice + clase
class ColumnRecommendation:
    """ 
    Clase que representa la recomendación del oráculo para
    una columna. Se compone del índice de dicha columna en
    el tablero y un valor de ColumnClassification.
    """

    def __init__(self, index: int, classification: ColumnClassification)-> None:
        self._index = index
        self._classification = classification
    
    #tuve que implementar las propertys para poder mantener los atributos privados 
    #y evitar problemas en el futuro
    @property
    def index(self):
        return self._index
    
    @property
    def classification(self):
        return self._classification
    
    def __eq__(self, other):
        """
        Sirve para comprobar si dos clases son distintas (es decir, que no sean identicas)
        """
        result = True
        if not isinstance(other, self.__class__):
            result = False
        #si son de la misma clase, comparamos las propiedades de ambas (pueden tener diferentes y aún asi dar True)
        else:
            result = (self._index, self._classification) == (other._index, other._classification)
        return result

    #Dos objetos equivalentes deben tener el mismo hash!! 
    def __hash__(self)-> int:
        """
        Recibe un objeto y calcula su hash.
        """
        return hash((self._index, self._classification))


# Oráculos, de más tonto a más listo
# Los oráculos, deben de realizar un trabajo complejo: clasificar columnas
#en el caso más complejo, teniendo en cuenta errores del pasado.
#Usamos divide y venceras y cada oráculo, del más tonto al más listo
#se encargará de una parte.

class BaseOracle:
    """
    La clase base y el oráculo más tonto: clasifica las columnas en
    llena y no llenas.
    """
    #creamos un metodo

    def get_recommendation(self, board: Board, player: Player)-> list[ColumnRecommendation]:
        """
        Devuelve una lista de ColumnRecommendations
        La construye sobre la marcha, vamos iterando por la cantidad
        de columnas que tenga el tablero y para cada una, la analizamos
        y obtenemos la recomendación
        """
        recommendations = []
        for index in range(BOARD_COLUMNS):
            recommendations.append(self._get_column_recommendation(board, index, player))
        return recommendations
    
    def _get_column_recommendation(self, board: Board, index: int, player: Player)-> ColumnRecommendation:
        """
        Clasifica una columna como FULL (columna llena) o MAYBE (puedes jugar,
        pero no existe recomendación real de jugada aún).
        Devuelve una ColummRecommendation
        """
        
        #por cada columna del tablero
        for i, col in enumerate(board._columns):
            if i == index: #analizo solo una columna
                    if self._is_full(col):
                        result = ColumnRecommendation(index, ColumnClassification.FULL)
                    else:
                        result = ColumnRecommendation(index, ColumnClassification.MAYBE)
        return result
    
    def _is_full(self, col: list)-> bool:
        result = True
        for el in col:
            if el == None:
                result = False
                break
        return result
    
class SmartOracle(BaseOracle):
    """
    Refina la recomendacion del oraculo base, intentando afinar
    la clasificacion MAYBE a algo más preciso. 
    - WIN: jugar aca me da la victoria inmediata
    -LOSE: jugar aca le da la victoria al rival 
    -MAYBE: jugada neutra
    """
    def _get_column_recommendation(self, board: Board, index: int, player: Player) -> ColumnRecommendation:
        """
        Afina las recomendaciones. 
        """
        #pido la clasificación básica
        basic = super()._get_column_recommendation(board, index, player)
        
        if basic._classification != ColumnClassification.MAYBE:
            return basic #columna llena, no hay nada que refinar
    
        #Jugar aca me da la victoria?
        if self._leads_to_victory(board, index, player._char):
            return ColumnRecommendation(index, ColumnClassification.WIN)

        #Jugar aquí le da la victoria al rival?
        if self._leads_to_victory(board, index, player.opponent._char):
            return ColumnRecommendation(index, ColumnClassification.LOSE)

        return basic



    def _leads_to_victory(self, board: Board, index: int, char: str) -> bool:
        """
        Simula una jugada en index con char y comprueba si hay victoria.
        Trabaja sobre una copia del tablero para no modificar el original.
        """
        temp_board = Board.from_list(deepcopy(board._columns))
        temp_board.add(char, index)
        return temp_board.is_victory(char)

    def _choose_best(self, recommendations: list[ColumnRecommendation]) -> ColumnRecommendation:
        """
        Elige la mejor recomendación según su clasificación.
        Entre iguales, elige aleatoriamente para variar el juego.
        """
        valid = [r for r in recommendations if r.classification != ColumnClassification.FULL]
        best_value = max(r.classification.value for r in valid)
        best_options = [r for r in valid if r.classification.value == best_value]
        return random.choice(best_options)


