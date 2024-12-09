#! /usr/bin/env python3

import csv
from collections import deque

def parse_tm_file(filename):
    """
    Parse a Turing Machine CSV file and return its components.
    
    Returns:
    A dictionary containing machine specifications and transitions
    """
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Parse header lines
        machine = {
            'name': next(reader)[0],
            'states': next(reader)[0].split(','),
            'input_alphabet': next(reader)[0].split(','),
            'tape_alphabet': next(reader)[0].split(','),
            'start_state': next(reader)[0],
            'accept_state': next(reader)[0],
            'reject_state': next(reader)[0],
            'transitions': {}
        }
        
        # Parse transitions
        for row in reader:
            if len(row) < 5:
                continue
            
            current_state, input_symbol = row[0], row[1]
            next_state, replace_symbol, move_direction = row[2], row[3], row[4]
            
            # Create transition key
            key = (current_state, input_symbol)
            
            # Add transition
            if key not in machine['transitions']:
                machine['transitions'][key] = []
            machine['transitions'][key].append((next_state, replace_symbol, move_direction))
    
    return machine

def get_transitions(machine, current_state, input_symbol):
    """
    Get possible transitions for a given state and input symbol.
    
    Returns list of possible transitions or an empty list (implying reject)
    """
    # Check for exact match
    if (current_state, input_symbol) in machine['transitions']:
        return machine['transitions'][(current_state, input_symbol)]
    
    # No transition found
    return []

def trace_tm(machine, input_string, print_path=True, stop_condition=1000):
    """
    Trace a Turing Machine through a given input string in a breadth-first manner.
    When an accept state is found, print the path taken to reach it.
    """
    # Each item in the queue is a tuple:
    # (left_tape, current_state, right_tape, path)
    # where path is a list of transitions leading to the current state
    queue = deque()
    initial_path = []
    queue.append(("", machine['start_state'], input_string, initial_path))
    depth = 0
    
    states_explored = 0
    
    while queue:
        left_tape, current_state, right_tape, path = queue.popleft()
        
        # Read the current input symbol; default to '_' if tape is empty
        input_symbol = right_tape[0] if right_tape else '_'
        
        # Get all possible transitions for the current state and input symbol
        possible_transitions = get_transitions(machine, current_state, input_symbol)
        
        # If no transitions are found, skip to the next item in the queue
        if not possible_transitions:
            continue
        
        for possible_transition in possible_transitions:
            states_explored += 1
            next_state, replace_symbol, move_direction = possible_transition
            
            # Update the tapes based on the move direction
            if move_direction == "R":
                new_left_tape = left_tape + replace_symbol
                new_right_tape = right_tape[1:] if len(right_tape) > 1 else "_"
            elif move_direction == "L":
                if not left_tape:
                    continue
                new_left_tape = left_tape[:-1]
                current_char = left_tape[-1] # if left_tape else '_'
                new_right_tape = current_char + replace_symbol + right_tape[1:] if right_tape else current_char + replace_symbol + "_"
            else:
                return "invalid move direction"
            
            # Update the path with the current transition
            new_path = path + [(current_state, input_symbol, next_state, replace_symbol, move_direction)]
            
            # Check if the next state is the accept state
            if next_state == machine['accept_state']:
                # print the results
                print("Accept!")
                print(f"Depth of tree: {len(new_path)}")
                print(f"Number of transitions simulated: {states_explored}")
                print(f"Average non-determinism per state: {states_explored / len(new_path)}")
                # print the path if the flag is set
                if print_path:
                    print("")
                    print("Path taken:")
                    for step_num, step in enumerate(new_path, start=1):
                        state_from, read_symbol, state_to, write_symbol, direction = step
                        print(f"Step {step_num}: ({state_from}, '{read_symbol}') -> ({state_to}, '{write_symbol}', {direction})")
                    print(f"Final Tape Configuration: {new_left_tape} | {new_right_tape}")
                return "accepted"
            
            # add new configuration to queue
            queue.append((new_left_tape, next_state, new_right_tape, new_path))

            # update depth, check stop condition
            depth = max(depth, len(new_path))
            if depth >= stop_condition:
                print("Reject!")
                print(f"Depth of tree: {depth}")
                print(f"Number of transitions simulated: {states_explored}")
                print(f"Average non-determinism per state: {states_explored / depth}")
                return "max depth exceeded"

    # if the accept state is not found, print the results
    print("Reject!")
    print(f"Depth of tree: {depth}")
    print(f"Number of transitions simulated: {states_explored}")
    print(f"Average non-determinism per state: {states_explored / depth}")
    return "not accepted"

def main():
    # Parse the NTM files
    # file = parse_tm_file('input_files/input_a_plus_tfriedma.csv')
    # file = parse_tm_file('input_files/input_a_plus_DTM_tfriedma.csv')
    file = parse_tm_file('input_files/input_equal_01s_tfriedma.csv')
    # file = parse_tm_file('input_files/input_equal_01s_DTM_tfriedma.csv')
    # file = parse_tm_file('input_files/input_abc_star_tfriedma.csv')
    # file = parse_tm_file('input_files/input_abc_star_DTM_tfriedma.csv')

    # Set inputs
    input_string = "001101010001111111100000111000101010101010101010110000000111110101010101010101010101011"
    stop_condition = 10000 # Tracing stops after a depth of 1000

    # Print machine details
    print(f"Machine: {file['name']}")
    print(f"Input String: {input_string}")
    
    # Trace the machine
    result = trace_tm(file, input_string, False, stop_condition)
    # print(f"Result: {result}")

if __name__ == "__main__":
    main()