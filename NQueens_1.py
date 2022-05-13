import argparse

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

def rsolve(queens,n):
    """
    Recursively find solution for NQueens problem
    Args:
        queens (list): List of integers. Each int gives the row assignment for the queen in a column
        n (int): Board size
    Returns:
        (list) : NQueens assignment as a list of integers. If no assignment is possible, returns empty list
    """
    if n == len(queens):
        # complete assignment
        return queens
    else:
        global num_assign
        for i in range(n):
            if not under_attack(i,queens):            
                num_assign += 1 # When there is no conflict now, the number of assignments is increased by 1
                newqueens = rsolve(queens+[i],n)  # recursive call with new assignment
                if newqueens != []:
                    return newqueens
        return []  # FAIL

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
    ans = rsolve([], n) 
    print_board(ans)
    print_num_assign(n, num_assign)

if __name__ =='__main__':
    main()