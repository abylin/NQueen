import argparse
import random
import sys
import numpy as np

def under_attack(col, queens):
    """
    Method to check if the current queens assignment leads to a conflict
    Args:
        col: new assignment to check
        queens: current queens assignment
    Returns:
         (bool): True if conflict / attack. False if not
    """
    return col in queens or \
           any(abs(col - x) == len(queens) - i for i, x in enumerate(queens))

def print_board(queens):
    """
    Method to print the board with NQueens assignment
    Args:
        queens (list): List of integers giving the row assignment for each queen
    Returns:
        None
    """
    n = len(queens)  # Assign board size
    for pos in queens:
        for i in range(pos):
            print('.', end=' ')
        print("Q", end = ' ')
        for i in range((n-pos)-1):
            print('.', end=' ')
        print()  # print new line for next row

def print_num_assign(n, num_assign):
    """
    Method to print answer for question 1
    Args:
        n (int): board size input
        num_assign (int): Number of assignments made
    Returns:
        None
    """
    print("Number of assignments for ", n, "queens =", num_assign)

# Update the three arrays that hold conflicting numbers when a new queen is placed
def put_on_a_queen(row, column, n):
    global COLUMN_CONFLICT
    COLUMN_CONFLICT[column] += 1
    global MAIN_DIAGONAL_CONFLICT
    MAIN_DIAGONAL_CONFLICT[n - 1 - row + column] += 1
    global COUNTER_DIAGONAL_CONFLICT
    COUNTER_DIAGONAL_CONFLICT[2 * n - 2 - row - column] += 1

# Update the three arrays that hold conflicting numbers when removing a queen
def take_away_a_queen(row, column, n):
    global COLUMN_CONFLICT
    COLUMN_CONFLICT[column] -= 1
    global MAIN_DIAGONAL_CONFLICT
    MAIN_DIAGONAL_CONFLICT[n - 1 - row + column] -= 1
    global COUNTER_DIAGONAL_CONFLICT
    COUNTER_DIAGONAL_CONFLICT[2 * n - 2 - row - column] -= 1

def check_is_answer(queens):
    # There is only one queen in each column.
	for column in range(len(COLUMN_CONFLICT)):
		if COLUMN_CONFLICT[column] != 1:
			return False
    # Each diagonal has only one queen.
	for i in range(len(MAIN_DIAGONAL_CONFLICT)):
		if MAIN_DIAGONAL_CONFLICT[i] > 1 or COUNTER_DIAGONAL_CONFLICT[i] > 1:
			return False
	return True 

def calculate_conflict_count(row, column, n):
    global columnConflict
    global mainDiaConflict
    global counterDiaConflict
    result = COLUMN_CONFLICT[column] + MAIN_DIAGONAL_CONFLICT[n - 1 - row + column] + COUNTER_DIAGONAL_CONFLICT[2 * n - 2 - row - column]
    return result

def rsolve(queens, n):
    """
    Recursively find solution for NQueens problem
    Args:
        queens (list): List of integers. Each int gives the row assignment for the queen in a column
        n (int): Board size
    Returns:
        (list) : NQueens assignment as a list of integers. If no assignment is possible, returns empty list
    """
    is_answer = check_is_answer(queens)
    max_steps = 10000 # Prevent after too many cycles has not appeared the result, judged as no result
    global num_assign
    while not is_answer:
        for row in range(n):
            min_conflict = sys.maxsize
            min_column = 0
            current_column = queens[row]
            take_away_a_queen(row, current_column, n)

            for column in range(n):
                current_conflict = calculate_conflict_count(row, column, n)
                if current_conflict < min_conflict:
                    min_conflict = current_conflict
                    min_column = column  
                elif current_conflict == min_conflict and random.uniform(0,1) > 0.5: # If the minimum conflict values are equal, there is a 50/50 chance of moving the queen, preventing it from falling into a local optimum instead of a global optimum
                    min_column = column
            queens[row] = min_column
            
            put_on_a_queen(row, min_column, n)
            num_assign +=1

            if check_is_answer(queens):
                return queens
            if num_assign > max_steps: 
                return [] # FAIL

def main():
    """
    Main function which calls other methods
    Args: None
    Returns : None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", action="store", help="board size")
    args = parser.parse_args()
    global num_assign 
    num_assign = 0 # Initial global variable num_assign
    n = int(args.size)

    global COLUMN_CONFLICT
    COLUMN_CONFLICT = np.zeros(n) # Conflict number mapping rules for column directions
    global MAIN_DIAGONAL_CONFLICT
    MAIN_DIAGONAL_CONFLICT = np.zeros(n * 2 -1) # Conflict number mapping rule for main diagonal direction. Such as: (i, j) --> n - 1 - i + j
    global COUNTER_DIAGONAL_CONFLICT
    COUNTER_DIAGONAL_CONFLICT = np.zeros(n * 2 -1) # Conflict number mapping rule for counter diagonal direction. Such as: (i, j) --> n - 1 - i + j

    queens = np.arange(0, n) # Initial queens
    np.random.shuffle(queens) # Randomly generate a permutation of queens
    for row in range(n) :
        put_on_a_queen(row, queens[row], n)

    ans = rsolve(queens, n)
    print_board(ans)
    print_num_assign(n, num_assign)

if __name__ =='__main__':
    main()