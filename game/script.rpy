# -*- coding: utf-8 -*-

## --- Config ---
define TILE_SIZE = 120
define TILE_COUNT_X = 16
define TILE_COUNT_Y = 9

## --- Variables ---
default map_width_tiles  = 50
default map_height_tiles = 30

# Yoruah (joueur)
default hero_dir = "down"
default hero_tile_x = map_width_tiles // 2
default hero_tile_y = map_height_tiles // 2

# Position de départ avant déplacement (pour annulation)
default hero_start_x = hero_tile_x
default hero_start_y = hero_tile_y

# Ryugaru (PNJ)
default ryugaru_dir = "down"
default ryugaru_tile_x = 37
default ryugaru_tile_y = 15

# Caméra centrée sur Yoruah
default camera_x = max(0, hero_tile_x - TILE_COUNT_X // 2)
default camera_y = max(0, hero_tile_y - TILE_COUNT_Y // 2)

# Déplacement actif (pour éviter inputs pendant animation)
default moving = False

# Variables animation déplacement case par case
default anim_current_step = 0
define anim_steps = 10
default anim_start_x = 0
default anim_start_y = 0
default anim_end_x = 0
default anim_end_y = 0

# Pour sélection des cases mouvables
default selected_tile = None
default movable_tiles = []

# Liste des cases sur le chemin à parcourir (liste de tuples)
default path = []

# Etat du tour : True = déplacement possible, False = tour fini, plus de déplacements
default turn_active = True

# Pour afficher le menu de confirmation après déplacement
default show_confirm_menu = False



#ia ryugaru

default moving_ryu = False
default path_ryu = []

default anim_current_step_ryu = 0
default anim_start_x_ryu = 0
default anim_start_y_ryu = 0
default anim_end_x_ryu = 0
default anim_end_y_ryu = 0









## --- Images ---
init:
    image background_tile = "images/background_map.png"

    # Sprites Yoruah
    image yoruah_down   = "images/yoruah/yoruah_down.png"
    image yoruah_up     = "images/yoruah/yoruah_up.png"
    image yoruah_left   = "images/yoruah/yoruah_left.png"
    image yoruah_right  = "images/yoruah/yoruah_right.png"

    # Sprites Ryugaru
    image ryugaru_down   = "images/ryugaru/ryugaru_down.png"
    image ryugaru_up     = "images/ryugaru/ryugaru_up.png"
    image ryugaru_left   = "images/ryugaru/ryugaru_left.png"
    image ryugaru_right  = "images/ryugaru/ryugaru_right.png"

    # Sprite Yoruah selon direction
    image hero_sprite = ConditionSwitch(
        "hero_dir == 'down'",  "yoruah_down",
        "hero_dir == 'up'",    "yoruah_up",
        "hero_dir == 'left'",  "yoruah_left",
        "hero_dir == 'right'", "yoruah_right"
    )

    # Sprite Ryugaru selon direction
    image ryugaru_sprite = ConditionSwitch(
        "ryugaru_dir == 'down'", "ryugaru_down",
        "ryugaru_dir == 'up'", "ryugaru_up",
        "ryugaru_dir == 'left'", "ryugaru_left",
        "ryugaru_dir == 'right'", "ryugaru_right"
    )

## --- Fonctions ---
init python:
    import renpy.exports as renpy

    def update_camera():
        global camera_x, camera_y
        camera_x = max(0, min(map_width_tiles - TILE_COUNT_X, hero_tile_x - TILE_COUNT_X // 2))
        camera_y = max(0, min(map_height_tiles - TILE_COUNT_Y, hero_tile_y - TILE_COUNT_Y // 2))

    def calculate_movable_tiles(radius=5):
        tiles = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                tx = hero_tile_x + dx
                ty = hero_tile_y + dy
                if 0 <= tx < map_width_tiles and 0 <= ty < map_height_tiles:
                    tiles.append((tx, ty))
        return tiles

    def calculate_and_show_moves():
        global movable_tiles
        if turn_active and not moving:
            movable_tiles = calculate_movable_tiles(5)

    def build_path(target_x, target_y):
        """Construit un chemin simple en ligne droite: d'abord horizontal, puis vertical."""
        path = []
        x, y = hero_tile_x, hero_tile_y

        # Horizontal
        step_x = 1 if target_x > x else -1
        for nx in range(x + step_x, target_x + step_x, step_x):
            path.append((nx, y))

        # Vertical
        step_y = 1 if target_y > y else -1
        for ny in range(y + step_y, target_y + step_y, step_y):
            path.append((target_x, ny))

        return path

    def start_move_to(target_x, target_y):
        global moving, anim_current_step, anim_start_x, anim_start_y, anim_end_x, anim_end_y
        global hero_dir, selected_tile, movable_tiles, hero_tile_x, hero_tile_y, path
        global hero_start_x, hero_start_y, show_confirm_menu

        if moving or not turn_active:
            return

        if (target_x, target_y) not in movable_tiles:
            return

        # Sauvegarde position départ pour annulation possible
        hero_start_x = hero_tile_x
        hero_start_y = hero_tile_y

        path = build_path(target_x, target_y)
        if not path:
            return

        # Démarrer la première étape de déplacement
        next_tile = path.pop(0)
        nx, ny = next_tile
        dx = nx - hero_tile_x
        dy = ny - hero_tile_y

        if dx > 0:
            hero_dir = "right"
        elif dx < 0:
            hero_dir = "left"
        elif dy > 0:
            hero_dir = "down"
        elif dy < 0:
            hero_dir = "up"

        moving = True
        anim_current_step = 0
        anim_start_x = hero_tile_x * TILE_SIZE
        anim_start_y = hero_tile_y * TILE_SIZE
        anim_end_x = nx * TILE_SIZE
        anim_end_y = ny * TILE_SIZE

        selected_tile = None
        movable_tiles = []

        show_confirm_menu = False

    def update_animation():
        global anim_current_step, moving, hero_tile_x, hero_tile_y, camera_x, camera_y
        global anim_start_x, anim_start_y, anim_end_x, anim_end_y, path, hero_dir, show_confirm_menu

        if not moving:
            return

        anim_current_step += 1

        if anim_current_step >= anim_steps:
            # Fin d'une étape
            hero_tile_x = anim_end_x // TILE_SIZE
            hero_tile_y = anim_end_y // TILE_SIZE

            if path:
                # Prochaine case dans le chemin
                next_tile = path.pop(0)
                nx, ny = next_tile

                dx = nx - hero_tile_x
                dy = ny - hero_tile_y

                if dx > 0:
                    hero_dir = "right"
                elif dx < 0:
                    hero_dir = "left"
                elif dy > 0:
                    hero_dir = "down"
                elif dy < 0:
                    hero_dir = "up"

                anim_current_step = 0
                anim_start_x = hero_tile_x * TILE_SIZE
                anim_start_y = hero_tile_y * TILE_SIZE
                anim_end_x = nx * TILE_SIZE
                anim_end_y = ny * TILE_SIZE

            else:
                # Fin du déplacement complet => afficher menu confirmation
                update_camera()
                moving = False
                anim_current_step = 0
                show_confirm_menu = True

        renpy.restart_interaction()

    def cancel_move():
        global hero_tile_x, hero_tile_y, moving, show_confirm_menu
        if moving:
            return
        hero_tile_x = hero_start_x
        hero_tile_y = hero_start_y
        update_camera()
        show_confirm_menu = False

    def confirm_move():
        global turn_active, show_confirm_menu
        turn_active = False
        show_confirm_menu = False

        # Lancer déplacement Ryugaru
        start_ryugaru_move()

## --- Screen de confirmation modal ---
screen confirm_move_menu():
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xsize 400
        ysize 200
        background "#000000AA"
        has vbox spacing 20

        text "Valider votre déplacement ?" size 40 xalign 0.5

        hbox:
            spacing 50
            textbutton "Oui" action [Function(confirm_move), Hide("confirm_move_menu")]
            textbutton "Non" action [Function(cancel_move), Hide("confirm_move_menu")]

    timer 5.0 action [Function(cancel_move), Hide("confirm_move_menu")]
screen combat_screen():
    fixed:
        add "background_tile" xpos -camera_x * TILE_SIZE ypos -camera_y * TILE_SIZE xysize (map_width_tiles * TILE_SIZE, map_height_tiles * TILE_SIZE)

        # Grille visible
        for x in range(TILE_COUNT_X + 1):
            for y in range(TILE_COUNT_Y + 1):
                $ tile_x = int(camera_x) + x
                $ tile_y = int(camera_y) + y
                if tile_x < map_width_tiles and tile_y < map_height_tiles:
                    add "images/grid.png" xpos x * TILE_SIZE ypos y * TILE_SIZE

        # Surlignage des cases accessibles si sélection en cours et tour actif
        if turn_active and not moving:
            for (tx, ty) in movable_tiles:
                $ screen_x = int((tx - camera_x) * TILE_SIZE)
                $ screen_y = int((ty - camera_y) * TILE_SIZE)
                add Solid("#55FF0055") xpos screen_x ypos screen_y xsize TILE_SIZE ysize TILE_SIZE

                button:
                    xpos screen_x
                    ypos screen_y
                    xsize TILE_SIZE
                    ysize TILE_SIZE
                    action Function(start_move_to, tx, ty)
                    background None

        # Position animée du héros si en déplacement
        if moving:
            $ interp_x = anim_start_x + (anim_end_x - anim_start_x) * anim_current_step / anim_steps
            $ interp_y = anim_start_y + (anim_end_y - anim_start_y) * anim_current_step / anim_steps
            $ screen_x = int(interp_x - camera_x * TILE_SIZE)
            $ screen_y = int(interp_y - camera_y * TILE_SIZE)
        else:
            $ screen_x = int((hero_tile_x - camera_x) * TILE_SIZE)
            $ screen_y = int((hero_tile_y - camera_y) * TILE_SIZE)

        add "hero_sprite" xpos screen_x ypos screen_y size (TILE_SIZE, TILE_SIZE)

        # Position animée de Ryugaru si en déplacement
        if moving_ryu:
            $ interp_x_ryu = anim_start_x_ryu + (anim_end_x_ryu - anim_start_x_ryu) * anim_current_step_ryu / anim_steps
            $ interp_y_ryu = anim_start_y_ryu + (anim_end_y_ryu - anim_start_y_ryu) * anim_current_step_ryu / anim_steps
            $ ryu_screen_x = int(interp_x_ryu - camera_x * TILE_SIZE)
            $ ryu_screen_y = int(interp_y_ryu - camera_y * TILE_SIZE)
        else:
            $ ryu_screen_x = int((ryugaru_tile_x - camera_x) * TILE_SIZE)
            $ ryu_screen_y = int((ryugaru_tile_y - camera_y) * TILE_SIZE)

        add "ryugaru_sprite" xpos ryu_screen_x ypos ryu_screen_y size (TILE_SIZE, TILE_SIZE)

        # Debug info
        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10 ypos 10
            text "Hero Pos: ([hero_tile_x], [hero_tile_y])" size 30 color "#000000"

        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10 ypos 50
            text "Hero Dir: [hero_dir]" size 30 color "#000000"

        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10 ypos 90
            text "Moving: [moving]" size 30 color "#000000"

        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10 ypos 130
            text "Ryugaru Moving: [moving_ryu]" size 30 color "#000000"

    timer 0.02 repeat True action [Function(update_animation), Function(update_animation_ryu)]

    # Clic sur héros pour afficher cases mouvables (si pas en déplacement et tour actif)
    button:
        xpos int((hero_tile_x - camera_x) * TILE_SIZE)
        ypos int((hero_tile_y - camera_y) * TILE_SIZE)
        xsize TILE_SIZE
        ysize TILE_SIZE
        background None
        action If(turn_active and not moving, Function(calculate_and_show_moves))

    # Affiche le menu de confirmation modal quand nécessaire
    if show_confirm_menu:
        use confirm_move_menu




#depalcement ryugaru
init python:



    def build_path_from_to(start_x, start_y, target_x, target_y):
        path = []

        # Horizontal
        step_x = 1 if target_x > start_x else -1
        for nx in range(start_x + step_x, target_x + step_x, step_x):
            path.append((nx, start_y))

        # Vertical
        step_y = 1 if target_y > start_y else -1
        for ny in range(start_y + step_y, target_y + step_y, step_y):
            path.append((target_x, ny))

        return path


init python:

    def update_animation_ryu():
        global anim_current_step_ryu, moving_ryu, ryugaru_tile_x, ryugaru_tile_y
        global anim_start_x_ryu, anim_start_y_ryu, anim_end_x_ryu, anim_end_y_ryu, path_ryu, ryugaru_dir

        if not moving_ryu:
            return

        anim_current_step_ryu += 1

        if anim_current_step_ryu >= anim_steps:
            ryugaru_tile_x = anim_end_x_ryu // TILE_SIZE
            ryugaru_tile_y = anim_end_y_ryu // TILE_SIZE

            if path_ryu:
                next_tile = path_ryu.pop(0)
                nx, ny = next_tile

                dx = nx - ryugaru_tile_x
                dy = ny - ryugaru_tile_y

                if dx > 0:
                    ryugaru_dir = "right"
                elif dx < 0:
                    ryugaru_dir = "left"
                elif dy > 0:
                    ryugaru_dir = "down"
                elif dy < 0:
                    ryugaru_dir = "up"

                anim_current_step_ryu = 0
                anim_start_x_ryu = ryugaru_tile_x * TILE_SIZE
                anim_start_y_ryu = ryugaru_tile_y * TILE_SIZE
                anim_end_x_ryu = nx * TILE_SIZE
                anim_end_y_ryu = ny * TILE_SIZE

            else:
                moving_ryu = False
                anim_current_step_ryu = 0

        renpy.restart_interaction()
    def start_move_ryu(target_x, target_y):
        global moving_ryu, anim_current_step_ryu, anim_start_x_ryu, anim_start_y_ryu, anim_end_x_ryu, anim_end_y_ryu
        global ryugaru_dir, ryugaru_tile_x, ryugaru_tile_y, path_ryu

        if moving_ryu:
            return

        # Utiliser build_path_from_to (4 arguments), pas build_path (2 arguments)
        path_ryu = build_path_from_to(ryugaru_tile_x, ryugaru_tile_y, target_x, target_y)
        if not path_ryu:
            return

        next_tile = path_ryu.pop(0)
        nx, ny = next_tile
        dx = nx - ryugaru_tile_x
        dy = ny - ryugaru_tile_y

        if dx > 0:
            ryugaru_dir = "right"
        elif dx < 0:
            ryugaru_dir = "left"
        elif dy > 0:
            ryugaru_dir = "down"
        elif dy < 0:
            ryugaru_dir = "up"

        moving_ryu = True
        anim_current_step_ryu = 0
        anim_start_x_ryu = ryugaru_tile_x * TILE_SIZE
        anim_start_y_ryu = ryugaru_tile_y * TILE_SIZE
        anim_end_x_ryu = nx * TILE_SIZE
        anim_end_y_ryu = ny * TILE_SIZE

    def start_ryugaru_move():
        global turn_active

        max_move = 5

        dx = hero_tile_x - ryugaru_tile_x
        dy = hero_tile_y - ryugaru_tile_y

        # Limite le déplacement de Ryugaru à max_move cases (Manhattan)
        move_x = max(-max_move, min(dx, max_move))
        move_y = max(-max_move, min(dy, max_move))

        dest_x = ryugaru_tile_x + move_x
        dest_y = ryugaru_tile_y + move_y

        start_move_ryu(dest_x, dest_y)  # <-- ici la fonction doit être définie au-dessus

        turn_active = False


## --- Menu démarrage ---
screen start_menu():
    tag menu
    frame:
        xalign 0.5
        yalign 0.5
        has vbox spacing 20

        text "Que voulez-vous faire ?" xalign 0.5 size 50

        textbutton "Combat" action Jump("combat")
        textbutton "Déplacement" action Jump("deplacement")

## --- Labels ---
label start:
    call screen start_menu
    return

label combat:
    call screen combat_screen
    return

label deplacement:
    call screen combat_screen
    return
