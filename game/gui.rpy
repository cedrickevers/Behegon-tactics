################################################################################
## Initialisation
################################################################################

## L'instruction init offset fait exécuter les instructions d'initialisation de
## ce fichier tavant les instructions init des autres fichiers.
init offset = -2

## Appelé gui.init réinitialise les styles à leurs valeurs par défaut et
## initialise la largeur et la hauteur du jeu.
init python:
    gui.init(3840, 2160)

## Active la vérification de propriétés invalides ou instables dans les screens
## et transforms
define config.check_conflicting_properties = True


################################################################################
## Variables de Configuration du GUI
################################################################################


## Couleurs ####################################################################
##
## Les couleurs du texte dans l’interface.

## Une couleur utilisée dans l’interface pour mettre l’accent sur un texte
## (surbrillance).
define gui.accent_color = '#660066'

## La couleur utilisée pour le texte d’un bouton quand il n’a jamais été
## sélectionné ou survolé.
define gui.idle_color = '#707070'

## La petite couleur est utilisé pour les textes courts qui nécessitent d’être
## assombris ou éclairés pour obtenir le même effet.
define gui.idle_small_color = '#606060'

## Cette couleur est utilisée pour les boutons et les barres qui sont survolées.
define gui.hover_color = '#660066'

## Cette couleur est utilisé pour le texte d’un bouton sélectionné, mais qui n’a
## pas le focus. Un bouton est sélectionné s’il est sur l’écran actuel ou si
## c’est la valeur de préférence.
define gui.selected_color = '#555555'

## La couleur utilisée pour le texte d’un bouton qui ne peut pas être
## sélectionné.
define gui.insensitive_color = '#7070707f'

## Couleurs utilisées pour les portions de barres qui ne sont pas remplies.
## Elles ne sont pas utilisées directement, mais quand les fichiers d’images
## sont régénérés.
define gui.muted_color = '#a366a3'
define gui.hover_muted_color = '#c199c1'

## Les couleurs utilisées pour les dialogues et les menus de choix.
define gui.text_color = '#404040'
define gui.interface_text_color = '#404040'


## Polices et tailles de police ################################################

## Les polices utilisées pour le texte du jeu.
define gui.text_font = "DejaVuSans.ttf"

## Les polices utilisées pour le nom des personnages.
define gui.name_text_font = "DejaVuSans.ttf"

## Les polices utilisées pour les textes « hors du jeu ».
define gui.interface_text_font = "DejaVuSans.ttf"

## La taille normale pour les dialogues.
define gui.text_size = 66

## La taille pour le nom des personnages.
define gui.name_text_size = 90

## La taille du texte dans l’interface de jeu.
define gui.interface_text_size = 66

## La taille des libellés dans l’interface de jeu.
define gui.label_text_size = 72

## La taille du texte dans la zone de notification.
define gui.notify_text_size = 48

## La taille du titre du jeu.
define gui.title_text_size = 150


## Menu du jeu et menu principal ###############################################

## Les images utilisées pour le menu principal et le menu du jeu.
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"


## Dialogue ####################################################################
##
## Ces variables contrôlent comment les dialogues sont affichés une ligne à la
## fois.

## La hauteur de la fenêtre contenant les dialogues.
define gui.textbox_height = 555

## L’emplacement vertical de la zone de texte à l’écran. 0.0 pour le haut, 0.5
## pour le centre et 1.0 pour le bas.
define gui.textbox_yalign = 1.0


## L’emplacement relatif à la zone de texte du nom du personnage en train de
## parler. La valeur peut être un nombre entier de pixels depuis la gauche ou le
## haut ou 0.5 pour le centre.
define gui.name_xpos = 720
define gui.name_ypos = 0

## L’alignement horizontal du nom du personnage. La valeur peut être 0.0 pour un
## alignement à gauche, 0.5 pour le centrer et 1.0 pour un alignement à droite.
define gui.name_xalign = 0.0

## La largeur, profondeur et les bords de la zone contenant le nom du personnage
## ou « None » pour le dimensionner automatiquement.
define gui.namebox_width = None
define gui.namebox_height = None

## Les bordures de la zone contenant le nom du personnage dans l’ordre suivant
## gauche, haut, droite, bas.
define gui.namebox_borders = Borders(5, 5, 5, 5)

## Si « True » (vrai), l’arrière plan de zone du nom sera en mosaïque, si
## « False »(faux), l’arrière plan de la zone du nom sera mis à l’échelle.
define gui.namebox_tile = False


## L’emplacement du dialogue relatif à la zone de texte. La valeur peut être un
## nombre entier de pixels depuis la gauche ou le haut ou 0.5 pour le centre.
define gui.dialogue_xpos = 804
define gui.dialogue_ypos = 150

## La largeur maximale en pixels de la zone de dialogue.
define gui.dialogue_width = 2232

## L’alignement horizontal de la zone de dialogue. La valeur peut être 0.0 pour
## un alignement à gauche, 0.5 pour le centrer et 1.0 pour un alignement à
## droite.
define gui.dialogue_text_xalign = 0.0


## Boutons #####################################################################
##
## Ces variables, ainsi que les fichiers d’image dans gui/button, contrôlent la
## façon d’afficher les boutons et leur aspect.

## La largeur et la hauteur d’un bouton en pixels. Si aucune valeur n’est
## renseignée (None), Ren’Py calcule la taille.
define gui.button_width = None
define gui.button_height = None

## Les bordures de chaque côté du bouton dans l’ordre suivant gauche, haut,
## droit, bas.
define gui.button_borders = Borders(12, 12, 12, 12)

## Si « True » (vrai), l’image d’arrière plan sera en mosaïque, si
## « False »(faux), elle sera mise à l’échelle.
define gui.button_tile = False

## La police utilisée par le bouton.
define gui.button_text_font = gui.interface_text_font

## La taille du texte utilisée pour le bouton.
define gui.button_text_size = gui.interface_text_size

## La couleur du texte des boutons dans différents états.
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color

## L'alignement horizontal du texte des boutons. (0.0 est à gauche, 0.5 est au
## centre, 1.0 est à droite).
define gui.button_text_xalign = 0.0


## Ces variables surchargent les paramètres par défaut pour différents types de
## boutons. Veuillez consulter la documentation de l’interface de jeu (GUI) pour
## les types de boutons disponibles et leurs usages.
##
## Ces personnalisations sont utilisées par l’interface par défaut :

define gui.radio_button_borders = Borders(54, 12, 12, 12)

define gui.check_button_borders = Borders(54, 12, 12, 12)

define gui.confirm_button_text_xalign = 0.5

define gui.page_button_borders = Borders(30, 12, 30, 12)

define gui.quick_button_borders = Borders(30, 12, 30, 0)
define gui.quick_button_text_size = 42
define gui.quick_button_text_idle_color = gui.idle_small_color
define gui.quick_button_text_selected_color = gui.accent_color

## Vous pouvez également ajouter vos propres personnalisations en ajoutant des
## variables correctement nommées. Par exemple, vous pouvez décommanter la ligne
## suivante pour personnaliser la largeur du bouton de navigation.

# define gui.navigation_button_width = 250


## Boutons pour les choix ######################################################
##
## Les boutons pour les choix (Choice buttons) sont utilisés dans le jeu pour
## permettre au joueur de choisir telle ou telle action, tel ou tel dialogue.

define gui.choice_button_width = 2370
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(300, 15, 300, 15)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = '#707070'
define gui.choice_button_text_hover_color = "#ffffff"
define gui.choice_button_text_insensitive_color = '#7070707f'


## Boutons des emplacements de fichiers. #######################################
##
## Un bouton d’emplacement de fichier est un type spécial de bouton. Il contient
## une vignette et un texte décrivant le contenu de la sauvegarde présente dans
## l’emplacement. Un emplacement de sauvegarde utilise une image dans gui/
## button, comme les autres types de bouton.

## Le bouton d’emplacement de sauvegarde.
define gui.slot_button_width = 828
define gui.slot_button_height = 618
define gui.slot_button_borders = Borders(30, 30, 30, 30)
define gui.slot_button_text_size = 42
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color
define gui.slot_button_text_selected_idle_color = gui.selected_color
define gui.slot_button_text_selected_hover_color = gui.hover_color

## La largeur et la hauteur des vignettes de sauvegarde utilisée pour les
## emplacements de sauvegarde.
define config.thumbnail_width = 768
define config.thumbnail_height = 432

## Le nombre de colonnes et de lignes pour la grille des emplacements de
## sauvegarde.
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2


## Positionnement et espacement ################################################
##
## Ces variables contrôlent l’espacement et le positionnement des différents
## éléments de l’interface utilisateur.

## La position sur le côté gauche des boutons de navigation, relatif au côté
## gauche de l'écran.
define gui.navigation_xpos = 120

## La position vertical du l’indicateur de saut des dialogues.
define gui.skip_ypos = 30

## La position verticale de la zone de notification.
define gui.notify_ypos = 135

## L’espacement entre les différents choix du menu.
define gui.choice_spacing = 66

## Boutons dans la section de navigation du menu principal et du menu de jeu.
define gui.navigation_spacing = 12

## Contrôle l’espacement entre les préférences.
define gui.pref_spacing = 30

## Contrôle l’espacements entre les boutons de préférences.
define gui.pref_button_spacing = 0

## L’espacement entre les boutons de page.
define gui.page_spacing = 0

## L’espacement entre les emplacements de sauvegarde.
define gui.slot_spacing = 30

## La position du texte du menu principal.
define gui.main_menu_text_xalign = 1.0


## Cadres ######################################################################
##
## Ces variables contrôlent le look des cadres qui peuvent contenir les
## composants de l’interface utilisateur quand un overlay ou une fenêtre ne sont
## pas présents.

## Frames génériques.
define gui.frame_borders = Borders(12, 12, 12, 12)

## Le cadre qui est utilisé par les écrans de confirmation.
define gui.confirm_frame_borders = Borders(120, 120, 120, 120)

## Le cadre qui est utilisé par l’écran de saut des dialogues.
define gui.skip_frame_borders = Borders(48, 15, 150, 15)

## Le cadre qui est utilisé par la zone de notification.
define gui.notify_frame_borders = Borders(48, 15, 120, 15)

## Est-ce que les arrière-plans des cadres doivent être en mosaïque ?
define gui.frame_tile = False


## Barres, ascenseurs et curseurs ##############################################
##
## Ceux-ci contrôlent le look et la taille des barres, des ascenseurs et des
## curseurs.
##
## Le GUI par défaut utilise uniquement des sliders et des barres de scrolling
## verticales. Toutes les autres barres ne sont utilisées que dans des screens
## écrits par l'utilisateur.

## La hauteur des barres, des ascenseurs et des curseurs horizontaux. La largeur
## des barres, des ascenseurs et des curseurs verticaux.
define gui.bar_size = 75
define gui.scrollbar_size = 36
define gui.slider_size = 75

## « True » (Vrai)  si les images de barres doivent être en mosaïques.
## « False »(Faux) si elles doivent être mise à l'échelle (étirement).
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False

## Bordures horizontales.
define gui.bar_borders = Borders(12, 12, 12, 12)
define gui.scrollbar_borders = Borders(12, 12, 12, 12)
define gui.slider_borders = Borders(12, 12, 12, 12)

## Bordures verticales.
define gui.vbar_borders = Borders(12, 12, 12, 12)
define gui.vscrollbar_borders = Borders(12, 12, 12, 12)
define gui.vslider_borders = Borders(12, 12, 12, 12)

## What to do with unscrollable scrollbars in the game menu. "hide" hides them,
## while None shows them.
define gui.unscrollable = "hide"


## Historique ##################################################################
##
## L’écran de l’historique affiche les dialogues que le joueur vient de lire.

## Le nombre de blocs que l’historique de dialogue Ren’Py va conserver.
define config.history_length = 250

## La hauteur de l’écran historique ou « None » pour calculer la hauteur au prix
## d’une légère perte de performance.
define gui.history_height = 420

## Additional space to add between history screen entries.
define gui.history_spacing = 0

## La position, largeur et alignement du label donnant le nom du personnage en
## train de parler.
define gui.history_name_xpos = 465
define gui.history_name_ypos = 0
define gui.history_name_width = 465
define gui.history_name_xalign = 1.0

## La position, largeur et alignement de la zone de dialogue.
define gui.history_text_xpos = 510
define gui.history_text_ypos = 6
define gui.history_text_width = 2220
define gui.history_text_xalign = 0.0


## Mode NVL ####################################################################
##
## L’écran du mode NVL affiche les dialogues prononcés par les personnages eux-
## mêmes en mode NVL.

## Les bordures de l’arrière-plan de la fenêtre en mode NVL.
define gui.nvl_borders = Borders(0, 30, 0, 60)

## Le nombre maximum d'entrées en mode NVL que Ren'Py affichera. Quand plus
## d'entrées sont affichées, les plus anciennes seront retirées.
define gui.nvl_list_length = 6

## La hauteur d’une entrée en mode NVL. Initialisez-la à « None » pour que la
## hauteur des entrées s’ajuste automatiquement.
define gui.nvl_height = 345

## L’espacement entre les entrées en mode NVL quand gui.nvl_height est à
## « None » et entre les entrées en mode NVL et le menu en mode NVL.
define gui.nvl_spacing = 30

## La position, largeur et alignement du label donnant le nom du personnage en
## train de parler.
define gui.nvl_name_xpos = 1290
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 450
define gui.nvl_name_xalign = 1.0

## La position, largeur et alignement de la zone de dialogue.
define gui.nvl_text_xpos = 1350
define gui.nvl_text_ypos = 24
define gui.nvl_text_width = 1770
define gui.nvl_text_xalign = 0.0

## La position, profondeur et l’alignement du text nvl_tought (Le texte prononcé
## par le personnage nvl_narrator).
define gui.nvl_thought_xpos = 720
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 2340
define gui.nvl_thought_xalign = 0.0

## La position de nvl menu_buttons.
define gui.nvl_button_xpos = 1350
define gui.nvl_button_xalign = 0.0


## Localisation (traduction et adaptation aux langues et cultures) #############

## Ceci contrôle où un saut de ligne est autorisé. La valeur par défaut convient
## à la plupart des langues. Une liste des valeurs disponible peut être trouvée
## sur https://www.renpy.org/doc/html/style_properties.html#style-property-
## language

define gui.language = "unicode"


################################################################################
## Appareils mobiles
################################################################################

init python:

    ## Ceci augmente la taille des boutons d’accès rapide pour les rendre plus
    ## accessibles sur les tablettes et les téléphones.
    @gui.variant
    def touch():

        gui.quick_button_borders = Borders(120, 42, 120, 0)

    ## Ceci change la taille et l’espacement de différents élements de la GUI
    ## pour s’assurer qu’ils soient visibles sur les téléphones.
    @gui.variant
    def small():

        ## Tailles des polices.
        gui.text_size = 90
        gui.name_text_size = 108
        gui.notify_text_size = 75
        gui.interface_text_size = 90
        gui.button_text_size = 90
        gui.label_text_size = 102

        ## Ajuste la position de la zone de texte.
        gui.textbox_height = 720
        gui.name_xpos = 240
        gui.dialogue_xpos = 270
        gui.dialogue_width = 3300

        ## Changer la taille et l'espacement de diverses choses.
        gui.slider_size = 108

        gui.choice_button_width = 3720
        gui.choice_button_text_size = 90

        gui.navigation_spacing = 60
        gui.pref_button_spacing = 30

        gui.history_height = 570
        gui.history_text_width = 2070

        gui.quick_button_text_size = 60

        ## Remplit le canvas du bouton.
        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        ## Mode NVL.
        gui.nvl_height = 510

        gui.nvl_name_width = 915
        gui.nvl_name_xpos = 975

        gui.nvl_text_width = 2745
        gui.nvl_text_xpos = 1035
        gui.nvl_text_ypos = 15

        gui.nvl_thought_width = 3720
        gui.nvl_thought_xpos = 60

        gui.nvl_button_width = 3720
        gui.nvl_button_xpos = 60
