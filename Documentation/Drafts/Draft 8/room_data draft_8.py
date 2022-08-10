# Room Data

hell_doors = {
	'A' : {1:'F', 2:'B', 3:'D'},
	'B' : {1:'C', 2:'A'},
	'C' : {1:'B'},
	'D' : {1:'A', 2:'E'},
	'E' : {1:'G', 2:'D'},
	'F' : {1:'G', 2:'A'},
	'G': {1:'E', 2:'H'}
	}

hell_rooms = {
	'A' : 'maps/hell/hell1',
	'B' : 'maps/hell/hell2',
	'C' : 'maps/hell/hell3',
	'D' : 'maps/hell/hell4',
	'E' : 'maps/hell/hell5',
	'F' : 'maps/hell/hell6',
	'G' : 'maps/cave/cave1',
	}

cave_rooms = {
	'E' : 'maps/hell/hell5',
	'G': 'maps/cave/cave1',
	'H': 'maps/cave/cave2',
	'I': 'maps/cave/cave3'
}
cave_doors = {
	'E': {1:'G', 2:'D'},
	'G': {1:'E', 2:'H'},
	'H': {1:'I', 2:'G'},
	'I': {1:'J', 2:'H'}
}

# print(hell_doors['A'])
# for i in range(len(hell_doors['A'])):
# 	index = i+1
# 	if hell_doors['A'][index] == 'B':
# 		print(index)
# for i in hell_rooms:
# 	print(i)
