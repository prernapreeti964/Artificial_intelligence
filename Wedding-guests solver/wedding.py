import sys
#bi-directional friendship tuples
friends = []
#set containing all the guests
guests = set()
#reading data from file
input_file = open(sys.argv[1],'r')
seats_per_table = int(sys.argv[2])
for line in input_file:
	friend_list = line.split(' ')
	friend_list = map(lambda s: s.strip(), friend_list)
	guest = friend_list.pop(0)
	guests.add(guest)
	for f in friend_list:
		friends.append((guest,f))
		guests.add(f)

#return a set of people unknown to a particular guest
def get_unknown(guest):
	ug = set(guests)
	for guest1,guest2 in friends:
		if guest in (guest1,guest2):
			ug.discard(guest1)
			ug.discard(guest2)
	return ug

#check if the guest can be added to the table
def addable_guest(table,guest):
	#guest already present
	if guest in sel_guests:
		return False
	#empty table
	elif len(table) == 0:
		return True
	#add a guest who dosent know anyone already present on the table
	else:
		aml = unknown_to_guest[table[0]]
		for member in table:
			aml &= unknown_to_guest[member]
		if guest in aml:
			return True
		else:
			return False

#total number of guests present
no_of_guests = len(guests)
#dict contains a guest name and a set of people unknown to guest
unknown_to_guest = { guest: get_unknown(guest) for guest in guests }
#set containing arranged people
sel_guests = set()
#list containing arrangement of tables
tables = []

#Arrangement of guests on tables
while len(tables) < no_of_guests:
	table = []
	if len(sel_guests) >= len(guests):
		break
	for guest in guests:
		if addable_guest(table,guest) and len(table) < seats_per_table and len(sel_guests) < len(guests):
			table.append(guest)
			sel_guests.add(guest)
	tables.append(table)
#print arrangement of tables
print len(tables),
for table in tables:
	for i,member in enumerate(table):
		if i == (len(table) - 1):
			print member,
		else:
			print member + ',',
	print ' ',
