

from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
# Create new player to start world
player = Player(world.starting_room)


# Dictionary to reverse movement of each direction
convert_direction = {
    "n": "s",
    "s": "n",
    "w": "e",
    "e": "w"
}


# Function to retrieve the number of unexplored exits for a room
def get_number_of_unexplored_paths(room):
    unexplored_exits_count = 0

    for direction in room:
        if room[direction] == "?":
            unexplored_exits_count += 1

    return unexplored_exits_count


# Function to build initial visited dict entry. Ex ouput -> visited[room_id] = { "n": ?, "s": ?, "e": ?, "w": ? }
def build_initial_dict_entry_value(visited, room):
    possible_room_exits = room.get_exits()

    visited[room.id] = {}

    for move in possible_room_exits:
        visited[room.id][move] = "?"


# Main function to traverse maze -> output is an array containing the final directions to traverse maze
def get_traversal_directions(maze):
    final_directions = []
    reverse_directions = []
    new_player = Player(maze.starting_room)
    visited = {}
    # Create an entry for the starting room in the visited dict
    build_initial_dict_entry_value(visited, new_player.current_room)
    # Loop will run until all rooms have been visited
    while len(visited) < len(room_graph):
        # If there are unexplored exits in the player's current room
        if get_number_of_unexplored_paths(visited[new_player.current_room.id]) > 0:
            # Loop thru available exits in current room
            for move in new_player.current_room.get_exits():
                # If exit is unexplored
                if visited[new_player.current_room.id][move] == "?":
                    # Store current room id to fill in visited[next_room_id] = { reverse_of_move : prev_room_id }
                    prev_room_id = new_player.current_room.id
                    # Store the opposite of each movement in reverse_directions array to simplify backtracking
                    backtrack_move = convert_direction[move]
                    # Move player
                    new_player.travel(move)
                    # Append the opposite of the move to reverse_directions arr
                    final_directions.append(move)
                    # Append the actual move into the final_directions arr
                    reverse_directions.append(backtrack_move)
                    # Replace the question mark at visited[prev_room_id] = { move: new_room_id } with current_room_id
                    visited[prev_room_id][move] = new_player.current_room.id
                    # Check if the new room has been visited already
                    if new_player.current_room.id not in visited:
                        # If not, create an entry for it in the visited dict and then break out of loop
                        build_initial_dict_entry_value(
                            visited, new_player.current_room)
                        visited[new_player.current_room.id][backtrack_move] = prev_room_id
                        break

        # Else there are no unexplored exits in the current room and it's time to backtrack
        else:
            # Last element of backtrack_array will be next move
            backtrack_move = reverse_directions.pop()
            # Move player back to the previous room
            new_player.travel(backtrack_move)
            # Append the backtrack move to the final_directions arr
            final_directions.append(backtrack_move)
    # Return final directions array
    return final_directions


# traversal_path = ['n', 'n']
traversal_path = get_traversal_directions(world)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
