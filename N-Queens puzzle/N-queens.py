# nrooks.py : Solve the N-Rooks/N-Queens problem!
# Prerna, August 2016(Modified Dr. Crandall's code)
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.


# The N-Queens problem is: Given an empty NxN chessboard, place N rooks on the board so that no queens
# can take any other, i.e. such that no two queens share the same row or column or diagonal.
# This is N, the size of the board.
N=11

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )
    
# Count total # of pieces on both the diagonals of a point on board   
#Count total # of pieces on main diagonal of a point on board 
def count_on_main_diagonal(board,r,c):
	sum_main_diag=0
	for row in range(0,N):
		for col in range(0,N):
			if((row+col)==(r+c)):
				sum_main_diag+=board[row][col]
	return sum_main_diag

#Count total # of pieces on reverse diagonals of a point on board 	
def count_on_rev_diagonal(board,r,c):
	sum_rev_diag=0
	row=r
	col=c
	while((row>=1)&(col>=1)):
		row=row-1
		col=col-1
		sum_rev_diag+=board[row][col]
	row=r
	col=c
	while((row<N-1)&(col<N-1)):
		row=row+1
		col=col+1
		sum_rev_diag+=board[row][col]
	return sum_rev_diag+board[r][c]

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

#successors2 of given board state    
def successors2(board):
	succlist=[]
	for r in range(0 ,N):
		for c in range(0, N):
				if (board[r][c]!=1)&(count_pieces(board)<=N):
					succlist.append(add_piece(board,r,c))
	return succlist
	
#successors3 of given board state    
def successors3(board):
	succlist=[]
	for r in range(0 ,N):
		for c in range(0, N):
				if (board[r][c]!=1)&(count_pieces(board)<=N)&(count_on_row(board,r)<1)&(count_on_col(board,c)<1):
					succlist.append(add_piece(board,r,c))
	return succlist
	
#successors4 of given board state to solve N-queens
def successors4(board):
	succlist=[]
	for r in range(0 ,N):
		for c in range(0, N):
					#print count_on_row(board,r);
					if (board[r][c]!=1) &(count_on_row(board,r)<1)&(count_on_col(board,c)<1)&(count_on_main_diagonal(board,r,c)<1)&(count_on_rev_diagonal(board,r,c)<1)&(count_pieces(board)<=N):
						succlist.append(add_piece(board,r,c))
	
	return succlist
	
	
	
# check if board is a goal state for N-queens
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) and \
        all( [ count_on_main_diagonal(board,r,c) <=1 for r in range(0, N) for c in range(0, N)]) and \
        all( [ count_on_rev_diagonal(board,r,c) <=1 for r in range(0, N) for c in range(0, N)])
        
# check if board is a goal state for N-rookss
def is_goal_rook(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) 

# Solve n-queens!
def solve(initial_board):
    fringe = [initial_board]
    
    while len(fringe)>0:
        for s in successors4( fringe.pop()):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False
    
# Solve n-rooks!    
def solve1(initial_board):
    fringe = [initial_board]
    
    while len(fringe)>0:
        for s in successors3( fringe.pop()):
            if is_goal_rook(s):
                return(s)
            fringe.append(s)
    return False

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print "Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n"
solution = solve(initial_board)
print "N-Queens\n"
print printable_board(solution) if solution else "Sorry, no solution found. :("
print "\nN-Rooks\n"
solution2 = solve1(initial_board)
print printable_board(solution2) if solution2 else "Sorry, no solution found. :("
