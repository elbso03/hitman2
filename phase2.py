from pprint import pprint
from hitman.hitman import HC, HitmanReferee


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.h = 0
        self.g = 0
        self.l = 0
        self.orientation = None

    def __eq__(self, other):
        return self.position == other.position


def get_neighbours(true_map, coord, length):
    l = {}
    coord_to_check = []
    for i in range(length):
        coord_to_check.append((0, -i - 1))
        coord_to_check.append((0, i + 1))
        coord_to_check.append((-i - 1, 0))
        coord_to_check.append((i + 1, 0))
    for new_position in coord_to_check:
        testcoord = (coord[0] + new_position[0], coord[1] + new_position[1])
        if testcoord in true_map:
            l[testcoord] = true_map[testcoord]
    return l


def cost_case(true_map, coord, costume):
    total_cost = 0
    neighbours2 = get_neighbours(true_map, coord, 2)
    # vu garde
    if not costume:
        for neighbour in neighbours2:
            match neighbours2[neighbour]:
                case HC.GUARD_E:
                    if (coord[0] == neighbour[0] + 1) or (coord[0] == neighbour[0] + 2):
                        total_cost += 5
                case HC.GUARD_W:
                    if (coord[0] == neighbour[0] - 1) or (coord[0] == neighbour[0] - 2):
                        total_cost += 5
                case HC.GUARD_S:
                    if (coord[1] == neighbour[1] - 1) or (coord[1] == neighbour[1] - 2):
                        total_cost += 5
                case HC.GUARD_N:
                    if (coord[1] == neighbour[1] + 1) or (coord[1] == neighbour[1] + 2):
                        total_cost += 5
    return total_cost


def in_range(true_map, coord):
    neighbours2 = get_neighbours(true_map, coord, 2)
    neighbours1 = get_neighbours(true_map, coord, 1)
    for neighbour in neighbours2:
        match neighbours2[neighbour]:
            case HC.GUARD_E:
                if (coord[0] == neighbour[0] + 1) or (coord[0] == neighbour[0] + 2):
                    return True
            case HC.GUARD_W:
                if (coord[0] == neighbour[0] - 1) or (coord[0] == neighbour[0] - 2):
                    return True
            case HC.GUARD_S:
                if (coord[1] == neighbour[1] - 1) or (coord[1] == neighbour[1] - 2):
                    return True
            case HC.GUARD_N:
                if (coord[1] == neighbour[1] + 1) or (coord[1] == neighbour[1] + 2):
                    return True
    for neighbour in neighbours1:
        match neighbours1[neighbour]:
            case HC.CIVIL_E:
                if (coord[0] == neighbour[0] + 1):
                    return True
            case HC.CIVIL_W:
                if (coord[0] == neighbour[0] - 1):
                    return True
            case HC.CIVIL_S:
                if (coord[1] == neighbour[1] - 1):
                    return True
            case HC.CIVIL_N:
                if (coord[1] == neighbour[1] + 1):
                    return True
    return False


def exploitchemin(hr, true_map, status, chemin):
    for c in chemin:
        # pprint(status)
        if (status['has_suit']) and (not status['is_suit_on']) and (not status['is_in_guard_range']) and (
                not status['is_in_civil_range']):
            status = hr.put_on_suit()
        current_pos = status['position']
        direction = None
        madirection = status['orientation']
        if c == (current_pos[0], current_pos[1] + 1):
            direction = HC.N
        elif c == (current_pos[0], current_pos[1] - 1):
            direction = HC.S
        elif c == (current_pos[0] + 1, current_pos[1]):
            direction = HC.E
        elif c == (current_pos[0] - 1, current_pos[1]):
            direction = HC.W
        # print(status['orientation'])
        if (true_map[c] != HC.GUARD_N) and (true_map[c] != HC.GUARD_S) and (true_map[c] != HC.GUARD_E) and (
                true_map[c] != HC.GUARD_W):
            match direction:
                case HC.N:
                    match madirection:
                        case HC.N:
                            status = hr.move()
                        case HC.E:
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.S:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.W:
                            status = hr.turn_clockwise()
                            status = hr.move()
                case HC.S:
                    match madirection:
                        case HC.S:
                            status = hr.move()
                        case HC.W:
                            status = hr.turn_anti_clockwise()
                            # print('A')
                            status = hr.move()
                        case HC.N:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.E:
                            status = hr.turn_clockwise()
                            status = hr.move()
                case HC.E:
                    match madirection:
                        case HC.E:
                            status = hr.move()
                        case HC.S:
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.W:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.N:
                            status = hr.turn_clockwise()
                            status = hr.move()
                case HC.W:
                    match madirection:
                        case HC.W:
                            status = hr.move()
                        case HC.N:
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.E:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                            status = hr.move()
                        case HC.S:
                            status = hr.turn_clockwise()
                            status = hr.move()
            match true_map[c]:
                case HC.PIANO_WIRE:
                    if not status['has_weapon']:
                        status = hr.take_weapon()
                        true_map[c] = HC.EMPTY
                case HC.SUIT:
                    if not status['has_suit']:
                        status = hr.take_suit()
                    if (not status['is_in_guard_range']) and (not status['is_in_civil_range']):
                        status = hr.put_on_suit()
                case HC.TARGET:
                    status = hr.kill_target()
        elif not status['is_in_guard_range']:
            match direction:
                case HC.N:
                    match madirection:
                        case HC.E:
                            status = hr.turn_anti_clockwise()
                        case HC.S:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                        case HC.W:
                            status = hr.turn_clockwise()
                case HC.S:
                    match madirection:
                        case HC.W:
                            status = hr.turn_anti_clockwise()
                        case HC.N:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                        case HC.E:
                            status = hr.turn_clockwise()
                case HC.E:
                    match madirection:
                        case HC.S:
                            status = hr.turn_anti_clockwise()
                        case HC.W:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                        case HC.N:
                            status = hr.turn_clockwise()
                case HC.W:
                    match madirection:
                        case HC.N:
                            status = hr.turn_anti_clockwise()
                        case HC.E:
                            status = hr.turn_anti_clockwise()
                            status = hr.turn_anti_clockwise()
                        case HC.S:
                            status = hr.turn_clockwise()
            status = hr.neutralize_guard()
            true_map[c] = HC.EMPTY
            status = hr.move()
    return status


def astar(true_map, start, end, m, n, have_costume, costume):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return [path[::-1], have_costume, costume]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (n - 1) or node_position[0] < 0 or node_position[1] > (m - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if true_map[node_position] == HC.WALL:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue
            if (true_map[child.position] == HC.GUARD_N) or (true_map[child.position] == HC.GUARD_S) or (
                    true_map[child.position] == HC.GUARD_E) or (true_map[child.position] == HC.GUARD_W):
                if in_range(true_map, child.position):
                    child.g += 120
                else:
                    child.g += 20

            if (true_map[child.position] == HC.SUIT):
                have_costume = True
            if have_costume and (not in_range(true_map, child.position)):
                costume = True

            # Create the f, g, and h values
            child.l = abs((child.position[0] - start_node.position[0])) + abs(
                (child.position[1] - start_node.position[1]))
            child.g += cost_case(true_map, current_node.position, costume)
            child.h = abs((child.position[0] - end_node.position[0])) + abs((child.position[1] - end_node.position[1]))
            child.f = child.g + child.h + child.l

            # Child is already in the open list
            check = False
            for open_node in open_list:
                if child == open_node and child.l > open_node.l:
                    check = True
            if check:
                continue

            # Add the child to the open list
            open_list.append(child)


def phase2_run(hr: HitmanReferee, true_map, status):
    target = None
    piano = None
    for case in true_map:
        if true_map[case] == HC.PIANO_WIRE:
            piano = case
        if true_map[case] == HC.TARGET:
            target = case
    # print(true_map)
    algo = astar(true_map, status['position'], piano, 6, 7, False, False)
    chemin = algo[0]
    algo = astar(true_map, piano, target, 6, 7, algo[1], algo[2])
    chemin += (algo[0])[1:]
    algo = astar(true_map, target, (0, 0), 6, 7, algo[1], algo[2])
    chemin += (algo[0])[1:]
    # print(chemin)
    status = exploitchemin(hr, true_map, status, chemin)
