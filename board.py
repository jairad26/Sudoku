from random import sample
base  = 3
side  = base*base

# pattern for a baseline valid solution
def pattern(row,col): 
	return (base*(row%base)+row//base+col)%side

# randomize rows, columns and numbers (of valid base pattern)

def shuffle(s): 
	return sample(s,len(s)) 
rBase = range(base) 
rows  = [ g*base + row for g in shuffle(rBase) for row in shuffle(rBase) ] 
cols  = [ g*base + col for g in shuffle(rBase) for col in shuffle(rBase) ]
nums  = shuffle(range(1,base*base+1))

# produce board using randomized baseline pattern
board2 = [ [nums[pattern(row,col)] for col in cols] for row in rows ]

squares = side*side
empties = squares * 2//4
for p in sample(range(squares),empties):
    board2[p//side][p%side] = 0
