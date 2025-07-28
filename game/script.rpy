# combat_turn_based.rpy
# -*- coding: utf-8 -*-

init:
    image background_tile = Solid("#AAAAAA")
    image hero = Solid("#FF0000")
    image hero2 = Solid("#00AA00")
    image hero3 = Solid("#AA00AA")
    image hero4 = Solid("#AA5500")
    image enemy1 = Solid("#0000FF")
    image enemy2 = Solid("#FFFF00")
    image enemy3 = Solid("#00FFFF")
    image enemy4 = Solid("#FF00FF")
    image cursor = Solid("#FFFF0055")

define TILE_SIZE = 64
define TILE_COUNT_X = 10
define TILE_COUNT_Y = 8

default map_width_tiles = 15
default map_height_tiles = 12

default camera_x = 0
default camera_y = 0

default current_turn = "hero"
default turn_active = True
default selection_mode = False

default anim_steps = 8

default selected_hero_index = 0
default current_enemy_index = 0

default cursor_x = 0
default cursor_y = 0

default movable_tiles = []

default hero_units = [
    {"id": "hero1", "image": "hero",  "tile_x": 1, "tile_y": 9, "moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
    {"id": "hero2", "image": "hero2", "tile_x": 2, "tile_y": 9, "moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
    {"id": "hero3", "image": "hero3", "tile_x": 1, "tile_y": 10,"moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
    {"id": "hero4", "image": "hero4", "tile_x": 2, "tile_y": 10,"moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
]

default enemy_units = [
    {"id": "enemy1", "image": "enemy1", "tile_x": 12, "tile_y": 2, "moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
    {"id": "enemy2", "image": "enemy2", "tile_x": 13, "tile_y": 2, "moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
    {"id": "enemy3", "image": "enemy3", "tile_x": 12, "tile_y": 3, "moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
    {"id": "enemy4", "image": "enemy4", "tile_x": 13, "tile_y": 3, "moving": False, "path": [], "anim_current_step": 0, "anim_start_x": 0, "anim_start_y": 0, "anim_end_x": 0, "anim_end_y": 0},
]

default game_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,0,1,1,0,0,0],
    [0,0,0,1,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,1,0,0,1,1,0,0,0,1,0,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,1,1,0,0,1,0,0,0,0,1,1,0,0],
    [0,0,0,1,0,0,1,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

init python:
    import heapq

    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def neighbors(pos):
        x, y = pos
        results = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < map_width_tiles and 0 <= ny < map_height_tiles:
                if game_map[ny][nx] == 0:
                    occupied = False
                    for hu in hero_units:
                        if (hu['tile_x'], hu['tile_y']) == (nx, ny):
                            occupied = True
                            break
                    if not occupied:
                        for en in enemy_units:
                            if (en['tile_x'], en['tile_y']) == (nx, ny):
                                occupied = True
                                break
                    if not occupied:
                        results.append((nx, ny))
        return results

    def astar(start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break
            for next_pos in neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        current = goal
        path = []
        while current != start:
            if current not in came_from:
                return []
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def update_camera():
        global camera_x, camera_y
        hx = hero_units[selected_hero_index]["tile_x"]
        hy = hero_units[selected_hero_index]["tile_y"]
        camera_x = max(0, min(map_width_tiles - TILE_COUNT_X, hx - TILE_COUNT_X // 2))
        camera_y = max(0, min(map_height_tiles - TILE_COUNT_Y, hy - TILE_COUNT_Y // 2))

    def start_move_selected_hero():
        unit = hero_units[selected_hero_index]
        if not unit['path'] or unit['moving']:
            return
        nx, ny = unit['path'].pop(0)
        unit['anim_current_step'] = 0
        unit['anim_start_x'] = unit['tile_x'] * TILE_SIZE
        unit['anim_start_y'] = unit['tile_y'] * TILE_SIZE
        unit['anim_end_x'] = nx * TILE_SIZE
        unit['anim_end_y'] = ny * TILE_SIZE
        unit['moving'] = True

    def plan_enemy_path(idx):
        if idx < 0 or idx >= len(enemy_units):
            return
        enemy = enemy_units[idx]
        start = (enemy['tile_x'], enemy['tile_y'])
        target = (hero_units[selected_hero_index]['tile_x'], hero_units[selected_hero_index]['tile_y'])
        path_tmp = astar(start, target)
        if path_tmp:
            enemy['path'] = path_tmp[:3]
        else:
            enemy['path'] = []

    def start_move_enemy(idx):
        enemy = enemy_units[idx]
        if enemy['moving'] or not enemy['path']:
            return
        nx, ny = enemy['path'].pop(0)
        enemy['anim_current_step'] = 0
        enemy['anim_start_x'] = enemy['tile_x'] * TILE_SIZE
        enemy['anim_start_y'] = enemy['tile_y'] * TILE_SIZE
        enemy['anim_end_x'] = nx * TILE_SIZE
        enemy['anim_end_y'] = ny * TILE_SIZE
        enemy['moving'] = True

    def start_enemy_phase():
        global turn_active, current_turn, current_enemy_index
        current_enemy_index = 0
        turn_active = False
        current_turn = "enemy"
        for i in range(len(enemy_units)):
            plan_enemy_path(i)
        if enemy_units:
            if enemy_units[0]['path']:
                start_move_enemy(0)

    def update_animation_heroes():
        global selected_hero_index, turn_active, current_turn, movable_tiles, selection_mode
        unit = hero_units[selected_hero_index]
        if not unit['moving']:
            return
        unit['anim_current_step'] += 1
        if unit['anim_current_step'] >= anim_steps:
            unit['tile_x'] = unit['anim_end_x'] // TILE_SIZE
            unit['tile_y'] = unit['anim_end_y'] // TILE_SIZE
            unit['moving'] = False
            if unit['path']:
                start_move_selected_hero()
            else:
                # Passe au héros suivant SEULEMENT après tout le path
                selected_hero_index_next = (selected_hero_index + 1) % len(hero_units)
                if selected_hero_index_next == 0:
                    turn_active = False
                    current_turn = "enemy"
                    start_enemy_phase()
                else:
                    selected_hero_index = selected_hero_index_next
                    global cursor_x, cursor_y
                    cursor_x = hero_units[selected_hero_index]['tile_x']
                    cursor_y = hero_units[selected_hero_index]['tile_y']
                    update_camera()
                    selection_mode = True
                    movable_tiles = calculate_movable_tiles(selected_hero_index, max_range=5)
        renpy.restart_interaction()

    def update_animation_enemies():
        global current_enemy_index, turn_active, current_turn, selection_mode, movable_tiles
        if current_turn != "enemy":
            return
        if current_enemy_index >= len(enemy_units):
            return
        enemy = enemy_units[current_enemy_index]
        if not enemy['moving']:
            return
        enemy['anim_current_step'] += 1
        if enemy['anim_current_step'] >= anim_steps:
            enemy['tile_x'] = enemy['anim_end_x'] // TILE_SIZE
            enemy['tile_y'] = enemy['anim_end_y'] // TILE_SIZE
            enemy['moving'] = False
            if enemy['path']:
                start_move_enemy(current_enemy_index)
            else:
                current_enemy_index += 1
                if current_enemy_index < len(enemy_units):
                    if enemy_units[current_enemy_index]['path']:
                        start_move_enemy(current_enemy_index)
                else:
                    turn_active = True
                    current_turn = "hero"
                    global cursor_x, cursor_y
                    cursor_x = hero_units[selected_hero_index]['tile_x']
                    cursor_y = hero_units[selected_hero_index]['tile_y']
                    update_camera()
                    selection_mode = True
                    movable_tiles = calculate_movable_tiles(selected_hero_index, max_range=5)
        renpy.restart_interaction()

    def calculate_movable_tiles(unit_index=None, max_range=5):
        if unit_index is None:
            unit_index = selected_hero_index
        unit = hero_units[unit_index]
        start = (unit['tile_x'], unit['tile_y'])
        reachable = []
        for y in range(map_height_tiles):
            for x in range(map_width_tiles):
                if game_map[y][x] == 0:
                    dist = abs(x - start[0]) + abs(y - start[1])
                    if dist <= max_range:
                        occupied = False
                        for hu in hero_units:
                            if (hu['tile_x'], hu['tile_y']) == (x, y):
                                occupied = True
                                break
                        if not occupied:
                            for en in enemy_units:
                                if (en['tile_x'], en['tile_y']) == (x, y):
                                    occupied = True
                                    break
                        if occupied:
                            continue
                        path_tmp = astar(start, (x, y))
                        if path_tmp and len(path_tmp) <= max_range:
                            reachable.append((x, y))
        return reachable

    def move_selected_hero(dx, dy):
        global cursor_x, cursor_y
        if current_turn != "hero":
            return
        unit = hero_units[selected_hero_index]
        if unit['moving'] or not turn_active:
            return
        if selection_mode:
            new_x = cursor_x + dx
            new_y = cursor_y + dy
            if (new_x, new_y) in movable_tiles:
                cursor_x = new_x
                cursor_y = new_y

    def validate_move():
        global selection_mode, movable_tiles
        if current_turn != "hero" or not turn_active:
            return
        if not selection_mode:
            return
        unit = hero_units[selected_hero_index]
        if (cursor_x, cursor_y) == (unit['tile_x'], unit['tile_y']):
            selection_mode = False
            movable_tiles = []
            return
        if (cursor_x, cursor_y) not in movable_tiles:
            return
        unit['path'] = []
        path_tmp = astar((unit['tile_x'], unit['tile_y']), (cursor_x, cursor_y))
        if path_tmp and len(path_tmp) <= 5:
            unit['path'] = path_tmp
            selection_mode = False
            movable_tiles = []
            start_move_selected_hero()

    def toggle_tab_action():
        global selection_mode, selected_hero_index, cursor_x, cursor_y, movable_tiles
        if selection_mode:
            selection_mode = False
            movable_tiles = []
            return
        selected_hero_index = (selected_hero_index + 1) % len(hero_units)
        cursor_x = hero_units[selected_hero_index]['tile_x']
        cursor_y = hero_units[selected_hero_index]['tile_y']
        update_camera()
        selection_mode = True
        movable_tiles = calculate_movable_tiles(selected_hero_index, max_range=5)

screen combat_screen():

    key "K_UP" action Function(move_selected_hero, 0, -1)
    key "K_DOWN" action Function(move_selected_hero, 0, 1)
    key "K_LEFT" action Function(move_selected_hero, -1, 0)
    key "K_RIGHT" action Function(move_selected_hero, 1, 0)
    key "K_RETURN" action Function(validate_move)
    key "K_TAB" action Function(toggle_tab_action)
    key "K_ESCAPE" action [SetVariable("selection_mode", False), SetVariable("movable_tiles", [])]

    fixed:
        for x in range(TILE_COUNT_X):
            for y in range(TILE_COUNT_Y):
                $ tile_x = camera_x + x
                $ tile_y = camera_y + y
                if tile_x < map_width_tiles and tile_y < map_height_tiles:
                    if game_map[tile_y][tile_x] == 1:
                        add Solid("#444444") xpos x * TILE_SIZE ypos y * TILE_SIZE xsize TILE_SIZE ysize TILE_SIZE
                    else:
                        add Solid("#AAAAAA") xpos x * TILE_SIZE ypos y * TILE_SIZE xsize TILE_SIZE ysize TILE_SIZE

        if selection_mode:
            for (mx, my) in movable_tiles:
                $ screen_x = (mx - camera_x) * TILE_SIZE
                $ screen_y = (my - camera_y) * TILE_SIZE
                add Solid("#6699FF88") xpos screen_x ypos screen_y xsize TILE_SIZE ysize TILE_SIZE

        if selection_mode:
            $ cursor_screen_x = (cursor_x - camera_x) * TILE_SIZE
            $ cursor_screen_y = (cursor_y - camera_y) * TILE_SIZE
            add "cursor" xpos cursor_screen_x ypos cursor_screen_y size (TILE_SIZE, TILE_SIZE)

        for i, hu in enumerate(hero_units):
            if hu['moving']:
                $ interp_x = hu['anim_start_x'] + (hu['anim_end_x'] - hu['anim_start_x']) * hu['anim_current_step'] / anim_steps
                $ interp_y = hu['anim_start_y'] + (hu['anim_end_y'] - hu['anim_start_y']) * hu['anim_current_step'] / anim_steps
                $ screen_x = int(interp_x - camera_x * TILE_SIZE)
                $ screen_y = int(interp_y - camera_y * TILE_SIZE)
            else:
                $ screen_x = int((hu['tile_x'] - camera_x) * TILE_SIZE)
                $ screen_y = int((hu['tile_y'] - camera_y) * TILE_SIZE)
            if i == selected_hero_index and selection_mode:
                add Solid("#FFFF00") xpos screen_x-2 ypos screen_y-2 xsize TILE_SIZE+4 ysize TILE_SIZE+4 alpha 0.4
            add hu['image'] xpos screen_x ypos screen_y size (TILE_SIZE, TILE_SIZE)

        for en in enemy_units:
            if en['moving']:
                $ interp_x = en['anim_start_x'] + (en['anim_end_x'] - en['anim_start_x']) * en['anim_current_step'] / anim_steps
                $ interp_y = en['anim_start_y'] + (en['anim_end_y'] - en['anim_start_y']) * en['anim_current_step'] / anim_steps
                $ ex = int(interp_x - camera_x * TILE_SIZE)
                $ ey = int(interp_y - camera_y * TILE_SIZE)
            else:
                $ ex = int((en['tile_x'] - camera_x) * TILE_SIZE)
                $ ey = int((en['tile_y'] - camera_y) * TILE_SIZE)
            add en['image'] xpos ex ypos ey size (TILE_SIZE, TILE_SIZE)

        if selection_mode:
            frame:
                background "#222222E0"
                xpos 400 ypos 5 xpadding 20 ypadding 6
                text "Sélection : [hero_units[selected_hero_index]['id']]" size 24 color "#FFD700"

        frame:
            background "#FFFFFF80"
            xpadding 10
            ypadding 5
            xpos 10
            ypos 10
            text "Tour: [current_turn]" size 20 color "#000000"
            text "Héros: [hero_units[selected_hero_index]['id']]" size 20 color "#000000" ypos 25
            text "Mode sélection: [selection_mode]" size 20 color "#000000" ypos 50

    timer 0.03 repeat True action [Function(update_animation_heroes), Function(update_animation_enemies)]

label start:
    scene black
    $ cursor_x = hero_units[selected_hero_index]['tile_x']
    $ cursor_y = hero_units[selected_hero_index]['tile_y']
    $ update_camera()
    $ selection_mode = True
    $ movable_tiles = calculate_movable_tiles(selected_hero_index, max_range=5)
    show screen combat_screen
    """
    Tour par tour avec déplacement au clavier, jusqu'à quatre héros et autant d'ennemis.
    TAB pour sélectionner le héros suivant (effet visuel jaune), flèches pour déplacer le curseur (cases bleues), ENTER pour valider le déplacement.
    Le déplacement est ANIMÉ case par case, façon Bahamut Lagoon !
    """
    return
