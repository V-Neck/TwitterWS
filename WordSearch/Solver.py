from WordSearch import WordSearch
alphabet = "ETAOINSRHDLUCMFYWGPBVKXQJZ"[::-1].lower()
clusters = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr', 'sch', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
cluster_1 = ['b','c','d','f','g','p','s','t','w']

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def pos(seq, n):
	return [x for x in seq if x[0] >= 0 and x[1] >= 0 and x[0] < n and x[1] < n]

n = 5
board = WordSearch(n, True)
board.fill(10)
board.print_board()

wordlist = [i.upper() for i in board.get_wordlist()]

for i in wordlist:
	print i,
print '\n'

#board length
bl = len(board.board)
# length of wordlist
wl = len(wordlist)
#first letters
fl = []
#first letter locations (row,col)
floc = []
#surrounds locations (row,col, loc)
surfloc = []
#possible strings of first and second letters
slet = []
#actual strings (str, loc, floc)
aslet = []
#wordlist in char arrays
listlet = []
#length of words in wordlist
listlen = []
#possible char strings, and their orientation
posstr = []


for i in wordlist:
	listlet.append(list(i))
	listlen.append(len(i))

for word in wordlist:
	for letter in word:
		fl.append(letter)
		break

for row in range(0,bl):
	for col in range(0,bl):
		if board.board[row][col] in fl:
			floc.append( (row,col) )

for loc in floc:
	for i in range(-1,2):
		for j in range(-1,2):
			surfloc.append( (loc[0]+i, loc[1]+j, loc) )

surfloc = pos(unique(surfloc), n)

for i in floc:
	for j in surfloc:
		if i == j[2]:
			slet.append( (board.board[i[0]][i[1]] + board.board[j[0]][j[1]], i, j) )

for i in slet:
	for j in wordlist:
		if i[0] == j[0]+j[1]:
			aslet.append(i)

i = 0

while i < len(aslet):
	for j in wordlist:
		if j[0] == aslet[i][0][0]:
			w = ""
			try:
				for k in range(0,len(j)):
					w+=board.board[aslet[i][1][0] + k*(aslet[i][2][0]-aslet[i][1][0])][aslet[i][1][1] + k*(aslet[i][2][1]-aslet[i][1][1])]
				posstr.append( (w,(aslet[i][2][0]-aslet[i][1][0]),(aslet[i][2][1]-aslet[i][1][1]),aslet[i][1]) )
			except IndexError:
				pass
			
	i+=1

i = 0

posstr = [i for i in posstr if i[0] in wordlist]

for i in posstr:
	for k in range(0, len(i[0])):
		board.board[i[3][0] + k*(i[1])][i[3][1] + k*(i[2])] = board.board[i[3][0] + k*(i[1])][i[3][1] + k*(i[2])].lower()
board.print_board()

posstr = [i[0] for i in posstr]
