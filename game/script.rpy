# -*- coding: utf-8 -*-

## --- Config ---
define TILE_SIZE = 120
define TILE_COUNT_X = 16
define TILE_COUNT_Y = 9

## --- Variables ---
default map_width_tiles  = 50
default map_height_tiles = 30

# Yoruah
default hero_dir = "down"
default hero_tile_x = map_width_tiles // 2
default hero_tile_y = map_height_tiles // 2

# Ryugaru
default ryugaru_dir = "down"
default ryugaru_tile_x = 37
default ryugaru_tile_y = 15

default camera_x = max(0, hero_tile_x - TILE_COUNT_X // 2)
default camera_y = max(0, hero_tile_y - TILE_COUNT_Y // 2)

## --- Images ---
init:
    image background_tile = "images/background_map.png"

    # Yoruah sprites
    image yoruah_down   = "images/yoruah/yoruah_down.png"
    image yoruah_up     = "images/yoruah/yoruah_up.png"
    image yoruah_left   = "images/yoruah/yoruah_left.png"
    image yoruah_right  = "images/yoruah/yoruah_right.png"

    # Ryugaru sprites
    image ryugaru_down   = "images/ryugaru/ryugaru_down.png"
    image ryugaru_up     = "images/ryugaru/ryugaru_up.png"
    image ryugaru_left   = "images/ryugaru/ryugaru_left.png"
    image ryugaru_right  = "images/ryugaru/ryugaru_right.png"

    image hero_sprite = ConditionSwitch(
        "hero_dir == 'down'",  "yoruah_down",
        "hero_dir == 'up'",    "yoruah_up",
        "hero_dir == 'left'",  "yoruah_left",
        "hero_dir == 'right'", "yoruah_right"
    )

    image ryugaru_sprite = ConditionSwitch(
        "ryugaru_dir == 'down'", "ryugaru_down",
        "ryugaru_dir == 'up'", "ryugaru_up",
        "ryugaru_dir == 'left'", "ryugaru_left",
        "ryugaru_dir == 'right'", "ryugaru_right"
    )

## --- Fonction mise à jour caméra ---
init python:
    def update_camera():
        global camera_x, camera_y

        camera_x = max(0, min(map_width_tiles - TILE_COUNT_X, hero_tile_x - TILE_COUNT_X // 2))
        camera_y = max(0, min(map_height_tiles - TILE_COUNT_Y, hero_tile_y - TILE_COUNT_Y // 2))

## --- Fonction déplacer héros ---
init python:
    def move_hero(dx, dy):
        global hero_tile_x, hero_tile_y, hero_dir
        new_x = hero_tile_x + dx
        new_y = hero_tile_y + dy

        # Limite dans la map
        if 0 <= new_x < map_width_tiles and 0 <= new_y < map_height_tiles:
            hero_tile_x = new_x
            hero_tile_y = new_y

            # Mise à jour direction
            if dx == 1:
                hero_dir = "right"
            elif dx == -1:
                hero_dir = "left"
            elif dy == 1:
                hero_dir = "down"
            elif dy == -1:
                hero_dir = "up"

            # Met à jour la caméra après déplacement
            update_camera()

## --- Fonction déplacer Ryugaru ---
init python:
    def move_ryugaru(dx, dy):
        global ryugaru_tile_x, ryugaru_tile_y, ryugaru_dir
        new_x = ryugaru_tile_x + dx
        new_y = ryugaru_tile_y + dy

        # Limite dans la map
        if 0 <= new_x < map_width_tiles and 0 <= new_y < map_height_tiles:
            ryugaru_tile_x = new_x
            ryugaru_tile_y = new_y

            # Mise à jour direction
            if dx == 1:
                ryugaru_dir = "right"
            elif dx == -1:
                ryugaru_dir = "left"
            elif dy == 1:
                ryugaru_dir = "down"
            elif dy == -1:
                ryugaru_dir = "up"

            # Optionnel : ne pas bouger la caméra ici pour suivre Yoruah uniquement

## --- Menu de démarrage ---
screen start_menu():
    tag menu
    frame:
        xalign 0.5
        yalign 0.5
        has vbox spacing 20

        text "Que voulez-vous faire ?" xalign 0.5 size 50

        textbutton "Combat" action Jump("combat")
        textbutton "Déplacement" action Jump("deplacement")

## --- Écran combat ---
screen combat_screen():
    fixed:
        # Fond
        add "background_tile" xpos -camera_x * TILE_SIZE ypos -camera_y * TILE_SIZE xysize (map_width_tiles * TILE_SIZE, map_height_tiles * TILE_SIZE)

        # Grille visible
        for x in range(TILE_COUNT_X + 1):
            for y in range(TILE_COUNT_Y + 1):
                $ tile_x = camera_x + x
                $ tile_y = camera_y + y

                if tile_x < map_width_tiles and tile_y < map_height_tiles:
                    add "images/grid.png" xpos x * TILE_SIZE ypos y * TILE_SIZE

        # Yoruah au centre
        $ screen_x = (TILE_COUNT_X // 2) * TILE_SIZE
        $ screen_y = (TILE_COUNT_Y // 2) * TILE_SIZE
        add "hero_sprite" xpos screen_x ypos screen_y size (TILE_SIZE, TILE_SIZE)

        # Ryugaru selon position relative à caméra
        $ ryu_screen_x = (ryugaru_tile_x - camera_x) * TILE_SIZE
        $ ryu_screen_y = (ryugaru_tile_y - camera_y) * TILE_SIZE
        add "ryugaru_sprite" xpos ryu_screen_x ypos ryu_screen_y size (TILE_SIZE, TILE_SIZE)

        # Debug info
        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10
            ypos 70
            text "Hero Pos: ([hero_tile_x], [hero_tile_y])" size 40 color "#000000"

        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10
            ypos 130
            text "Hero Dir: [hero_dir]" size 40 color "#000000"

    key "K_UP" action Function(move_hero, 0, -1)
    key "K_DOWN" action Function(move_hero, 0, 1)
    key "K_LEFT" action Function(move_hero, -1, 0)
    key "K_RIGHT" action Function(move_hero, 1, 0)
    key "K_ESCAPE" action Return()

## --- Écran déplacement (backup) ---
screen deplacement_screen():
    fixed:
        # Fond
        add "background_tile" xpos -camera_x * TILE_SIZE ypos -camera_y * TILE_SIZE xysize (map_width_tiles * TILE_SIZE, map_height_tiles * TILE_SIZE)

        # Grille visible
        for x in range(TILE_COUNT_X + 1):
            for y in range(TILE_COUNT_Y + 1):
                $ tile_x = camera_x + x
                $ tile_y = camera_y + y

                if tile_x < map_width_tiles and tile_y < map_height_tiles:
                    add "images/grid.png" xpos x * TILE_SIZE ypos y * TILE_SIZE

        # Yoruah au centre
        $ screen_x = (TILE_COUNT_X // 2) * TILE_SIZE
        $ screen_y = (TILE_COUNT_Y // 2) * TILE_SIZE
        add "hero_sprite" xpos screen_x ypos screen_y size (TILE_SIZE, TILE_SIZE)

        # Ryugaru selon position relative à caméra
        $ ryu_screen_x = (ryugaru_tile_x - camera_x) * TILE_SIZE
        $ ryu_screen_y = (ryugaru_tile_y - camera_y) * TILE_SIZE
        add "ryugaru_sprite" xpos ryu_screen_x ypos ryu_screen_y size (TILE_SIZE, TILE_SIZE)

        # Debug info
        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10
            ypos 70
            text "Hero Pos: ([hero_tile_x], [hero_tile_y])" size 40 color "#000000"

        frame:
            background "#87CEEB80"
            xpadding 20
            ypadding 10
            xpos 10
            ypos 130
            text "Hero Dir: [hero_dir]" size 40 color "#000000"

    key "K_UP" action Function(move_hero, 0, -1)
    key "K_DOWN" action Function(move_hero, 0, 1)
    key "K_LEFT" action Function(move_hero, -1, 0)
    key "K_RIGHT" action Function(move_hero, 1, 0)
    key "K_ESCAPE" action Return()

## --- Labels ---
label start:
    call screen start_menu
    return

label combat:
    call screen combat_screen
    return

label deplacement:
    call screen deplacement_screen
    return
