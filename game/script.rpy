# -*- coding: utf-8 -*-

define TILE_SIZE = 64
define TILE_COUNT_X = 10
define TILE_COUNT_Y = 8

default map_width_tiles = 15
default map_height_tiles = 12

default hero_tile_x = 2
default hero_tile_y = 2
default ryugaru_tile_x = 12
default ryugaru_tile_y = 9

default hero_dir = "down"
default ryugaru_dir = "up"

default camera_x = 0
default camera_y = 0

default moving = False
default moving_ryu = False

default path = []
default path_ryu = []

default anim_current_step = 0
default anim_current_step_ryu = 0
define anim_steps = 8

default anim_start_x = 0
default anim_start_y = 0
default anim_end_x = 0
default anim_end_y = 0

default anim_start_x_ryu = 0
default anim_start_y_ryu = 0
default anim_end_x_ryu = 0
default anim_end_y_ryu = 0

default current_turn = "hero"
default turn_active = True

default selection_mode = False
default cursor_x = 0
default cursor_y = 0
default movable_tiles = []

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
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(pos):
        x, y = pos
        results = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < map_width_tiles and 0 <= ny < map_height_tiles:
                if game_map[ny][nx] == 0:
                    if (nx, ny) != (hero_tile_x, hero_tile_y) and (nx, ny) != (ryugaru_tile_x, ryugaru_tile_y):
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
        camera_x = max(0, min(map_width_tiles - TILE_COUNT_X, hero_tile_x - TILE_COUNT_X // 2))
        camera_y = max(0, min(map_height_tiles - TILE_COUNT_Y, hero_tile_y - TILE_COUNT_Y // 2))

    def start_move(character):
        global moving, moving_ryu
        global anim_current_step, anim_current_step_ryu
        global anim_start_x, anim_start_y, anim_end_x, anim_end_y
        global anim_start_x_ryu, anim_start_y_ryu, anim_end_x_ryu, anim_end_y_ryu
        global path, path_ryu
        global hero_dir, ryugaru_dir
        global hero_tile_x, hero_tile_y, ryugaru_tile_x, ryugaru_tile_y

        if character == "hero":
            if moving or not turn_active or current_turn != "hero":
                return
            if not path:
                return
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
            moving = True
        elif character == "ryugaru":
            if moving_ryu or turn_active or current_turn != "ryugaru":
                return
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
            anim_current_step_ryu = 0
            anim_start_x_ryu = ryugaru_tile_x * TILE_SIZE
            anim_start_y_ryu = ryugaru_tile_y * TILE_SIZE
            anim_end_x_ryu = nx * TILE_SIZE
            anim_end_y_ryu = ny * TILE_SIZE
            moving_ryu = True

    def update_animation():
        global anim_current_step, moving
        global hero_tile_x, hero_tile_y
        global anim_start_x, anim_start_y, anim_end_x, anim_end_y
        global path, current_turn, turn_active

        if not moving:
            return

        anim_current_step += 1
        if anim_current_step >= anim_steps:
            hero_tile_x = anim_end_x // TILE_SIZE
            hero_tile_y = anim_end_y // TILE_SIZE
            update_camera()

            if path:
                start_move("hero")
            else:
                moving = False
                turn_active = False
                current_turn = "ryugaru"
                start_ryugaru_move()

        renpy.restart_interaction()

    def update_animation_ryu():
        global anim_current_step_ryu, moving_ryu
        global ryugaru_tile_x, ryugaru_tile_y
        global anim_start_x_ryu, anim_start_y_ryu, anim_end_x_ryu, anim_end_y_ryu
        global path_ryu, current_turn, turn_active

        if not moving_ryu:
            return

        anim_current_step_ryu += 1
        if anim_current_step_ryu >= anim_steps:
            ryugaru_tile_x = anim_end_x_ryu // TILE_SIZE
            ryugaru_tile_y = anim_end_y_ryu // TILE_SIZE
            update_camera()

            if path_ryu:
                start_move("ryugaru")
            else:
                moving_ryu = False
                turn_active = True
                current_turn = "hero"

        renpy.restart_interaction()

    def calculate_movable_tiles(character, max_range=5):
        if character == "hero":
            start = (hero_tile_x, hero_tile_y)
        else:
            start = (ryugaru_tile_x, ryugaru_tile_y)

        reachable = []

        for y in range(map_height_tiles):
            for x in range(map_width_tiles):
                if game_map[y][x] == 0:
                    dist = abs(x - start[0]) + abs(y - start[1])
                    if dist <= max_range:
                        path_tmp = astar(start, (x,y))
                        if path_tmp:
                            reachable.append((x,y))

        return reachable

    def start_ryugaru_move():
        global path_ryu
        start = (ryugaru_tile_x, ryugaru_tile_y)
        goal = (hero_tile_x, hero_tile_y)

        path_tmp = astar(start, goal)

        if path_tmp:
            path_ryu = path_tmp[:5]
            start_move("ryugaru")
        else:
            global current_turn, turn_active
            current_turn = "hero"
            turn_active = True

    def move_hero(dx, dy):
        global hero_tile_x, hero_tile_y, hero_dir, path, moving
        if moving or not turn_active or current_turn != "hero" or selection_mode:
            return

        new_x = hero_tile_x + dx
        new_y = hero_tile_y + dy

        if 0 <= new_x < map_width_tiles and 0 <= new_y < map_height_tiles:
            if game_map[new_y][new_x] == 0 and (new_x, new_y) != (ryugaru_tile_x, ryugaru_tile_y):
                # Définir la direction en fonction du déplacement
                if dx > 0:
                    hero_dir = "right"
                elif dx < 0:
                    hero_dir = "left"
                elif dy > 0:
                    hero_dir = "down"
                elif dy < 0:
                    hero_dir = "up"
                # Créer un chemin simple d'une case pour le déplacement animé
                path = [(new_x, new_y)]
                start_move("hero")

init:
    image background_tile = "background_tile.png"
    image hero = "hero.png"
    image ryugaru = "ryugaru.png"
    image cursor = Solid("#FFFF0055")

screen combat_screen():

    key "K_UP" action Function(move_hero, 0, -1)
    key "K_DOWN" action Function(move_hero, 0, 1)
    key "K_LEFT" action Function(move_hero, -1, 0)
    key "K_RIGHT" action Function(move_hero, 1, 0)
    key "K_ESCAPE" action SetVariable("selection_mode", False)

    fixed:
        # Affichage map et obstacles
        for x in range(TILE_COUNT_X):
            for y in range(TILE_COUNT_Y):
                $ tile_x = camera_x + x
                $ tile_y = camera_y + y
                if tile_x < map_width_tiles and tile_y < map_height_tiles:
                    if game_map[tile_y][tile_x] == 1:
                        add Solid("#444444") xpos x * TILE_SIZE ypos y * TILE_SIZE xsize TILE_SIZE ysize TILE_SIZE
                    else:
                        add Solid("#AAAAAA") xpos x * TILE_SIZE ypos y * TILE_SIZE xsize TILE_SIZE ysize TILE_SIZE

        # Position animée héros
        if moving:
            $ interp_x = anim_start_x + (anim_end_x - anim_start_x) * anim_current_step / anim_steps
            $ interp_y = anim_start_y + (anim_end_y - anim_start_y) * anim_current_step / anim_steps
            $ screen_x = int(interp_x - camera_x * TILE_SIZE)
            $ screen_y = int(interp_y - camera_y * TILE_SIZE)
        else:
            $ screen_x = int((hero_tile_x - camera_x) * TILE_SIZE)
            $ screen_y = int((hero_tile_y - camera_y) * TILE_SIZE)

        add "hero" xpos screen_x ypos screen_y size (TILE_SIZE, TILE_SIZE)

        # Position animée Ryugaru
        if moving_ryu:
            $ interp_x_ryu = anim_start_x_ryu + (anim_end_x_ryu - anim_start_x_ryu) * anim_current_step_ryu / anim_steps
            $ interp_y_ryu = anim_start_y_ryu + (anim_end_y_ryu - anim_start_y_ryu) * anim_current_step_ryu / anim_steps
            $ ryu_screen_x = int(interp_x_ryu - camera_x * TILE_SIZE)
            $ ryu_screen_y = int(interp_y_ryu - camera_y * TILE_SIZE)
        else:
            $ ryu_screen_x = int((ryugaru_tile_x - camera_x) * TILE_SIZE)
            $ ryu_screen_y = int((ryugaru_tile_y - camera_y) * TILE_SIZE)

        add "ryugaru" xpos ryu_screen_x ypos ryu_screen_y size (TILE_SIZE, TILE_SIZE)

        # Debug info
        frame:
            background "#FFFFFF80"
            xpadding 10
            ypadding 5
            xpos 10
            ypos 10
            text "Tour: [current_turn]" size 20 color "#000000"

    timer 0.03 repeat True action [Function(update_animation), Function(update_animation_ryu)]


init python:
    def end_hero_turn():
        global current_turn, turn_active, moving, path
        if moving:
            return
        path = []
        turn_active = False
        current_turn = "ryugaru"
        start_ryugaru_move()

label start:
    scene black
    show screen combat_screen
    "Tour par tour avec déplacement au clavier."
    return
