import pyfiglet
class Game():

    def start(self):
        """
        Arranca el juego. Imprime el nombre
        del juego y su configuración.
        """
        self.print_logo()

    def print_logo(self):
        logo = pyfiglet.Figlet(font = "univers")
        print(logo.renderText("Coneta Cuatro"))