from player import Player
class Match():
    
    def __init__(self, player1, player2):
        """
        Player 1 es igual al char "x"
        Player 2 es igual al char "o"
        """
        #le asignamos su char
        player1._char = "x" 
        player2._char = "o"

        #le asignamos su oponente
        player1.opponent = player2
        player2.opponent = player1 #tuve que añadirlo porque no es muy inteligente, no lo supone al menos que lo específique

        #creamos un mapa que tiene a cada jugador indexado por su char
        self._players = {"x" : player1, "o": player2}
        
        #los guardamos en una estructura para poder ir seleccionandolos según su turno
        #lista redonda de 2 elementos, iremos invirtiendo la lista para ir alternando la elección entre player1 y 2
        self._round = [player1, player2]

    @property
    def next_player(self):
        """
        Despues de acabar una jugada, permite elegir un
        jugador diferente (el oponente) para que continue el
        juego por turnos
        """
        next = self._round[0] #primero elijo el 1er elemento 
        self._round.reverse() #la invierto así me da el "segundo elemento" (que ahora es el 1ero)
        return next
    def get_player(self, char):
        """
        Metodo que me permite acceder a él por su char
        """
        return self._players[char]
    