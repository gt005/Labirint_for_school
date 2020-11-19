# -2 - стена


def add_to_queue(cur, row, col):
    global matrix
    global m_path
    global m_row
    global m_col
    if not (0 <= row <= len(matrix) - 1) or\
        not (0 <= col <= len(matrix[0]) - 1) or\
        matrix[row][col] == -2:
            return
    if matrix[row][col] == -1 or\
        matrix[row][col] > matrix[cur[0]][cur[1]] + 1:
            matrix[row][col] = matrix[cur[0]][cur[1]] + 1
            queue.append((row, col))
    if (row == 0 or row == len(matrix) - 1 or \
        col == 0 or col == len(matrix[0]) - 1) and \
        (m_path == -1 or matrix[row][col] < m_path):
            m_path = matrix[row][col]
            m_row = row
            m_col = col


def reverse_path(row, col):
    global matrix
    global game_map

    game_map[row][col] = u"\U0001F422"
    if row == 0:
        row += 1
    elif col == 0:
        col += 1
    elif row == len(matrix) - 1:
        row -= 1
    else:
        col -= 1
    while matrix[row][col] != 1:
        game_map[row][col] = u"\U0001F422"
        if matrix[row + 1][col] == matrix[row][col] - 1:
            row += 1
        elif matrix[row - 1][col] == matrix[row][col] - 1:
            row -= 1
        elif matrix[row][col + 1] == matrix[row][col] - 1:
            col += 1
        elif matrix[row][col - 1] == matrix[row][col] - 1:
            col -= 1


matrix = """*** ***
*   * *
* ***  
*  A  *
**** **
*      
*******"""
tmp = matrix
matrix = list(map(list, matrix.split('\n')))
#game_map = [matrix[i][j] for i in matrix]
game_map = list(map(list, tmp.split('\n')))

turtle_coordinates = (0, 0)
m_path = -1
m_row = -1
m_col = -1

for row in range(len(matrix)):
    for col in range(len(matrix[row])):
        if matrix[row][col] == '*':
            matrix[row][col] = -2
        elif matrix[row][col] == ' ':
            matrix[row][col] = -1
        elif matrix[row][col] == 'A':
            game_map[row][col] = u"\U0001F422"
            matrix[row][col] = 1
            turtle_coordinates = (row, col)
        else:
            print("Неправильный символ")
            exit(1)

print(*matrix, sep='\n')

queue = [ turtle_coordinates ]
while queue:
    cur = queue.pop(0)
    add_to_queue(cur, cur[0] + 1, cur[1])
    add_to_queue(cur, cur[0] - 1, cur[1])
    add_to_queue(cur, cur[0], cur[1] + 1)
    add_to_queue(cur, cur[0], cur[1] - 1)

print()
for i in matrix:
    print(*i, sep='\t')

reverse_path(m_row, m_col)

print()
print(m_path)
print()
for i in game_map:
    print()
    print(*i, sep='\t')
