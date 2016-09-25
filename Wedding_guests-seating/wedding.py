#code after parsing
import sys, getopt
friends = []
guests = set()
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

def addable_guest(table,guest):
	if guest in sel_guests:
		#print guest, " may not be added into ",table
		return False
	elif len(table) == 0:
		#print guest, " may be added into ",table
		return True
	else:
		aml = unknown_to_guest[table[0]]
		for member in table:
			aml &= unknown_to_guest[member]
		if guest in aml:
			#print guest, " may be added into ",table
			return True
		else:
			#print guest, " may not be added into ",table
			return False

no_of_guests = len(guests)
#dict contains a guest name and a set of people unknown to guest
unknown_to_guest = { guest: get_unknown(guest) for guest in guests }
#list of tuples containing guest name and the number of people unknown to guest
guest_priority = [ (len(unknown_to_guest[guest]),guest) for guest in guests ]
guest_priority.sort()
#set containing arranged people
sel_guests = set()
#list containing arrangement of tables
tables = []

#print "Start arrangement"
while len(tables) < no_of_guests:
	table = []
	if len(sel_guests) >= len(guests):
		#print "Finished Arrangement"
		break
	for guest in guests:
		if addable_guest(table,guest) and len(table) < seats_per_table and len(sel_guests) < len(guests):
			table.append(guest)
			sel_guests.add(guest)
			#print guest, " added to ",table
	tables.append(table)
print len(tables),
for table in tables:
	for member in table:
		print member + ',',
	print ' ',
