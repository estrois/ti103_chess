"""
Ce module représente l'échiquier.

C'est lui qui va gérer les événements des joueurs et prendre en charge l'affichage du jeu sur l'écran. Pour ce faire,
nous avons besoin des packages pygame et chess. Pygame est le moteur de jeu qui réagit aux clicks des souris. chess lui
est le moteur de jeu d'échecs, celui qui valide si le mouvement proposé par le joueur est valide.

Ce module est composé de plusieurs éléments:
1. Une classe pour décrire une pièce du jeu particulière
2. Une classe pour décrire l'échiquier lui-même.
3. Une initiale pour chaque type de pièce, afin de représenter un mouvement.
"""
import chess
import pygame
import sys


# On code le dictionnaire qui représente les pièces d'échec. Les initiales servent à décrire la pièce lors de son
# mouvement. Par exemple 'e5' représente le mouvement d'un pion vers la case e5, alors que Nb3 représente le déplacement
# d'un cavalier vers la case b3.
piece_initiale = {
    'Roi': 'K',
    'Dame': 'Q',
    'Fou': 'B',
    'Cavalier': 'N',
    'Tour': 'R',
    'Pion': ''
}


class Piece:
    """
    Représente une simple pièce d'échec.

    Une pièce possède un nom et une couleur. Elle a aussi une case, et donc possède des coordonnées à l'écran. Elle
    possède enfin une image, et une référence à la surface de jeu à afficher.
    """
    def __init__(self, nom, couleur, x, y, taille, image, ecran):
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.ecran = ecran
        self.image = image

    def affiche(self):
        """
        Cette méthode force l'affichage de la pièce sur l'écran.

        Un rectangle de la surface de jeu est redefini pour son affichage. Pour afficher le rectangle, on va avoir
        besoin de connaître les coordonnées de son coin en haut à gauche. Ce seront les coordonnées possédées par la
        pièce elle-même. La taille du rectangle viendra de la dimension de l'image elle-même.

             (x, y)
                  +------largeur --------+
                  |                      |
                  |                      |
              longueur                   |  <----- Zone a afficher sur l'ecran.
                  |                      |
                  |                      |
                  +----------------------+
        """
        r = self.image.get_rect()       # On récupère la taille de l'image à afficher
        r.topleft = self.x, self.y      # On passe les coordonnées de la pièce comme coin en haut à gauche du rectangle
        self.ecran.blit(self.image, r)  # On affichage l'image dans le rectangle crée à l'intérieur de la zone écran

    def case(self):
        """
        Retourne la case correspondante de la piece affichee a l'ecran.
        """
        return chr(97 + (self.x // 85)) + str(((680 - self.y) // 85))


class Echiquier:
    """
    Représente un echiquier.
    """
    def __init__(self, ecran, echiquier, image):
        self.moteur = chess.Board()  # Moteur va valider si les mouvements sont valables.
        self.ecran = ecran
        self.echiquier = echiquier
        self.pieces = [Piece("Roi",      "Noir",  85 * 4, 0,      85, self._image(image, (68, 70, 85, 85)),   ecran),
                       Piece("Dame",     "Noir",  85 * 3, 0,      85, self._image(image, (234, 70, 85, 85)),  ecran),
                       Piece("Tour",     "Noir",  85 * 0, 0,      85, self._image(image, (400, 70, 85, 85)),  ecran),
                       Piece("Tour",     "Noir",  85 * 7, 0,      85, self._image(image, (400, 70, 85, 85)),  ecran),
                       Piece("Fou",      "Noir",  85 * 2, 0,      85, self._image(image, (566, 70, 85, 85)),  ecran),
                       Piece("Fou",      "Noir",  85 * 5, 0,      85, self._image(image, (566, 70, 85, 85)),  ecran),
                       Piece("Cavalier", "Noir",  85 * 1, 0,      85, self._image(image, (736, 70, 85, 85)),  ecran),
                       Piece("Cavalier", "Noir",  85 * 6, 0,      85, self._image(image, (736, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 0, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 1, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 2, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 3, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 4, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 5, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 6, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 7, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Roi",      "Blanc", 85 * 4, 85 * 7, 85, self._image(image, (68, 214, 85, 85)),  ecran),
                       Piece("Dame",     "Blanc", 85 * 3, 85 * 7, 85, self._image(image, (234, 214, 85, 85)), ecran),
                       Piece("Tour",     "Blanc", 85 * 0, 85 * 7, 85, self._image(image, (400, 214, 85, 85)), ecran),
                       Piece("Tour",     "Blanc", 85 * 7, 85 * 7, 85, self._image(image, (400, 214, 85, 85)), ecran),
                       Piece("Fou",      "Blanc", 85 * 2, 85 * 7, 85, self._image(image, (566, 214, 85, 85)), ecran),
                       Piece("Fou",      "Blanc", 85 * 5, 85 * 7, 85, self._image(image, (566, 214, 85, 85)), ecran),
                       Piece("Cavalier", "Blanc", 85 * 1, 85 * 7, 85, self._image(image, (736, 214, 85, 85)), ecran),
                       Piece("Cavalier", "Blanc", 85 * 6, 85 * 7, 85, self._image(image, (736, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 0, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 1, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 2, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 3, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 4, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 5, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 6, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 7, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran)]


    def jouer(self):
        """
        C'est ici que se trouve la boucle de jeu, dans laquelle se rafraichit l'image de l'echiquier.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

# partie 4 determiner si et quelle piece sera choisie pour deplacer.
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        casedepart = chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)
                        print(' manuel case de depart: ' + casedepart)

                        for i in self.pieces:   # donne acces aux attributs de chaque piece

                            if ((x // 85) * 85) == i.x and ((y // 85) * 85) == i.y:
                                print(i.nom + " " + i.couleur + " est a: " + i.case())
                                pieceprise = i
                                break

# Partie 5 deplacer la piece choisie
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        x, y = event.pos
                        casearrivee = chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)
                        mvmnt = str(casedepart + casearrivee)

  #partie 6 validite du mouvement.

                        print("recherche de mouvements legaux")
                        for k in self.moteur.legal_moves:
                            answer = str(k)
                            if(answer==mvmnt):
                                # Deplace la piece jouee
                                print(f"{piece_initiale[i.nom]}{i.case()}{casearrivee}")
                                self.moteur.push_san(f"{piece_initiale[i.nom]}{i.case()}{casearrivee}")
                                for n, p in enumerate(self.pieces):
                                    if ((x // 85) * 85) == p.x and ((y // 85) * 85) == p.y:
                                        print(f"{p.couleur} {p.nom} being captured")
                                        self.pieces.pop(n)
                                        break
                                i.x = ((x // 85) * 85)
                                i.y = 680 - (((680 - y) // 85 + 1) * 85)
                                print("i,x = ", str(i.x) + "i,y = ", str(i.y))
                            # envoie a la piece x et y du coin superieur gauche de la case ou aterrit la piece





#Partie 7 Determiner la prise d'une piece

                        # for m, p in enumerate(pieces):
                        #     print(type(m))
                        #     if (x // 85 == p.x // 85) and (y // 85 == p.y // 85):
                        #         print(f"{p.color} {p.name} being captured")
                        #         pieces.pop(m)
                        #         break


                        # for j in self.pieces:  # donne acces aux attributs de chaque piece
                        #      # detection de collision ou bien si j ai depose au dessus d une piece
                        #
                            # if ((x // 85) * 85) == j.x and ((y // 85) * 85) == j.y:
                            #     print("je ne passe jamais ici")
                            #     print(j.nom + " " + j.couleur + " " + j.case()+ " x: " + str(j.x) + " y: " + str(j.y))
                            #     piecedepose = j.case()
                            #     print(j.case())
                            #     print(str(i.x) + ":" + str(i.y) + "-" + str(j.x) + ":" + str(j.y))
                            #     print(i.case(), j.case())
                            #     break


            self.ecran.fill((255, 255, 255))
            self.ecran.blit(self.echiquier, self.echiquier.get_rect())

            [p.affiche() for p in self.pieces]
            pygame.display.update()

    def _image(self, image, pos):
        """
        Genere la piece de l'image a partir de l'image generale du jeu d'echec.
        """
        r = pygame.Rect(pos)
        obj = pygame.Surface(r.size).convert()
        obj.blit(image, (0, 0), r)
        return obj

    def to_tile(x, y):
        return chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)

def nouvelle_partie():
    """
    C'est ici que l'on cree une nouvelle partie.

    La fonction retourne un echiquier et ses pieces disposees pour debuter une partie.
    """
    pygame.init()                                # Initialisation du moteur de jeu pygame
    ecran = pygame.display.set_mode((680, 680))  # On cree une fenetre de 680 pixel par 680 pixels
    pygame.display.set_caption("Echecs")         # Le titre de la fenetre s'appelle Echecs

    echiquier = pygame.Surface((680, 680))       # On definit une surface a l'ecran pour representer l'echiquier
    echiquier.fill((175, 141, 120))              # Que l'on peint en marron (uni) voici le RGB(175, 141, 120)

    # Les lignes suivantes permettent de peindre dans un marron legerement different les cases de l'echiquier
    # precedemment defini.
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    for x in range(1, 9, 2):
        for y in range(1, 9, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    # Ici, on cree enfin le jeu d'echecs ainsi que les nouvelles pieces a afficher
    return Echiquier(ecran, echiquier, pygame.image.load("ressources/img.png").convert())


if __name__ == '__main__':
    partie = nouvelle_partie()
    partie.jouer()
