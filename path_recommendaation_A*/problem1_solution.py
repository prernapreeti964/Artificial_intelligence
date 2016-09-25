#library for getting command line arguments
import sys
import heapq
from math import sin, cos, sqrt, atan2, radians

city_gps={}
road_segments={}
goal_cost = 9999999999
goal_path = ""
goal_time = 0.0
goal_dist = 0.0
goal_flag =0


def find_neighbor_closest_to_goal(highwayIntersection, fromCity):
        
        min_heuristic = 9999999
	min_neighbor = {}	
    	for child_key, child_value in road_segments.iteritems():
		childKeySplitList = key_split(child_key)
		if childKeySplitList[0] == highwayIntersection and childKeySplitList[1] != fromCity :
                	child_item = {child_key:child_value}
			euc_distance = calc_heuristic(childKeySplitList[1], endCityName)
			if euc_distance != None:
				heuristic = float(child_item[child_key]["distance"])+euc_distance
				if heuristic < min_heuristic:
					min_heuristic = heuristic
					min_neighbor = child_item
					
					
	
	return (min_heuristic, min_neighbor)

	
def calc_heuristic(src, dest):
	if src not in list(city_gps.keys()):
		 print "\nNo entry in City_Gps file for\t", src, "\n"	
		 return None
	#print "\nlatitude src = ", city_gps[src]["latitude"]
	distance = 0
	if routeOptionString == "distance":
		# approximate radius of earth in km
		R = 6373.0 * 0.621371
		lat1 = city_gps[src]["latitude"]
		lon1 = city_gps[src]["longitude"]
		lat2 = city_gps[dest]["latitude"]
		lon2 = city_gps[dest]["longitude"]
		
		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c
		
	return distance


def astar():
	fringe = []
	global goal_cost
	global goal_path
        global goal_time
        global goal_dist
	# iter on both keys and values
    	for key, value in road_segments.iteritems():
		key_tokens = key_split(key)
		if key_tokens[0] == startCityName:
			item  = {key:value}
			item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
			item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
			item[key]["costToNode"] = item[key][routeOptionString]    
			item[key]["timeToNode"] = item[key]["travelTime"]
                        item[key]["distToNode"] = float(item[key]["distance"])
                        g = calc_heuristic(key_tokens[1], endCityName)
			if g != None:
				f = item[key]["distToNode"]+g
                                heapq.heappush(fringe, (f,item))
			'''else:
				highway_neighbor_tuple = find_neighbor_closest_to_goal(key_tokens[1], key_tokens[0])
				print "\nhighway neighbor tuple entry",highway_neighbor_tuple[1]
				if highway_neighbor_tuple != None:
					heapq.heappush(fringe,highway_neighbor_tuple)'''
	
	while len(fringe) > 0:
		popped_item = heapq.heappop(fringe)[1]
		for s in successors(popped_item):
			keys = list(s.keys())
                        s_key = keys[0]
			if is_goal(s,endCityName):
                		float_val = float(s[s_key]["costToNode"])
                		if float_val < goal_cost:
                        		goal_cost = float(s[s_key]["costToNode"])
                        		goal_path = s[s_key]["pathToNode"]
                        		goal_time = float(s[s_key]["timeToNode"])
                        		goal_dist = float(s[s_key]["distToNode"])
                       	 		continue
            		if s not in fringe:
                		heapq.heappush(fringe,(s[s_key]["costToNode"],s))
		#print "\nheap entry = ", (heapq.heappop(fringe))[1]	
	return None

def key_split(key):
    keySplitList = key.split('|')
    return keySplitList
    
def is_goal(s, endCityName):
    keys = list(s.keys())
    key = keys[0]
    keySplitList = key.split('|')
    if keySplitList[1] == endCityName:
        s[key]["pathToNode"] = s[key]["pathToNode"] + "|"+endCityName
        return True
    
    return False


def successors(dict):
    
    global goal_path
    global goal_cost
    global goal_dist
    global goal_time

    if is_goal(dict,endCityName):
    	keys = list(dict.keys())
        s_key = keys[0]
        float_val = float(dict[s_key]["costToNode"])
        if float_val < goal_cost:
        	goal_cost = float(dict[s_key]["costToNode"])
                goal_path = dict[s_key]["pathToNode"]
		goal_time = float(dict[s_key]["timeToNode"])
		goal_dist = float(dict[s_key]["distToNode"])
                
    ret=[]
    #print "inside successors - ", routingAlgoString
    path = []
    keys = list(dict.keys())
    parent_key = keys[0]
    parent_value = dict[parent_key]
    parent_item = {parent_key: parent_value}
    parent_path= parent_item[parent_key]["pathToNode"]
    parentKeySplitList = parent_key.split('|')
    pathList = parent_path.split('|')
    for child_key, child_value in road_segments.iteritems():
        childKeySplitList = key_split(child_key)
        if childKeySplitList[0] == parentKeySplitList[1] and childKeySplitList[1] not in pathList:
            	child_item = {child_key:child_value}
            	child_item[child_key]["pathToNode"] = parent_path+ "|"+childKeySplitList[1]
            	child_item[child_key]["costToNode"] = float(dict[parent_key]["costToNode"]) +  float(child_item[child_key][routeOptionString]) 
		child_item[child_key]["distToNode"] = float(dict[parent_key]["distToNode"]) +  float(child_item[child_key]["distance"])
		child_item[child_key]["timeToNode"] = float(dict[parent_key]["timeToNode"]) +  float(child_item[child_key]["travelTime"])	
		if "bfs" in routingAlgorithm or "dfs" in routingAlgorithm or "idfs" in routingAlgorithm:
			if(child_item[child_key]["costToNode"]< goal_cost):
				ret.append({child_key:child_value})
		elif "astar" in routingAlgorithm:
			latLongDistance = calc_heuristic(childKeySplitList[0],endCityName)
			if latLongDistance != None:
				heuristic = child_item[child_key]["costToNode"] + latLongDistance
			else:
				heuristic = child_item[child_key]["costToNode"]  
			if heuristic < goal_cost:
				child_item[child_key]["costToNode"] = heuristic
				ret.append({child_key:child_value})
					
    return ret

def dfs():
    
    fringe = []
    global goal_cost
    global goal_path
    global goal_time
    global goal_dist
    
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
            item[key]["costToNode"] = item[key][routeOptionString]
            item[key]["timeToNode"] = item[key]["travelTime"]
            item[key]["distToNode"] = item[key]["distance"]
  
            fringe.append(item)
    #count=0
    while len(fringe)>0:
       # pop_item=fringe.pop(count)
        for s in successors(fringe.pop()):
            #scount=successors(pop_item)
            #count=count+len(scount)
            if is_goal(s,endCityName):
		keys = list(s.keys())
		s_key = keys[0]
		float_val = float(s[s_key]["costToNode"])
		if float_val < goal_cost:
			goal_cost = float(s[s_key]["costToNode"])
			goal_path = s[s_key]["pathToNode"]
			goal_time = float(s[s_key]["timeToNode"])
			goal_dist = float(s[s_key]["distToNode"])
                        continue
            if s not in fringe:
                fringe.append(s)
           
                
    return False
	
def bfs():
    
    fringe = []
    global goal_cost
    global goal_path
    global goal_dist
    global goal_time
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
            item[key]["costToNode"] = item[key][routeOptionString]
	    item[key]["timeToNode"] = item[key]["travelTime"]
	    item[key]["distToNode"] = item[key]["distance"]    
            fringe.append(item)

    while len(fringe) > 0:
           for s in successors( fringe.pop(0)):
            if is_goal(s,endCityName):
		keys = list(s.keys())
		s_key = keys[0]
		float_val = float(s[s_key]["costToNode"])
		if float_val < goal_cost:
			goal_cost = float(s[s_key]["costToNode"])
			goal_path = s[s_key]["pathToNode"]
			goal_time = float(s[s_key]["timeToNode"])
			goal_dist = float(s[s_key]["distToNode"])
		continue
            
            
            if s not in fringe:
                fringe.append(s)
                
    return False

    
#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
    
    global startCityName, endCityName, routeOptionString, routingAlgoString
    
    startCityName = str(startCity).strip('[]')
    endCityName = str(endCity).strip('[]')
    routeOptionString = str(routingOption).strip('[]')
    routingAlgoString = str(routingAlgorithm).strip('[]')
    #print routingAlgoString
    
    if "bfs" in routingAlgorithm:
            bfs()
    if "dfs" in routingAlgorithm:
            dfs()
    if "ids" in routingAlgorithm:
            ids()
    if "astar" in routingAlgorithm:
            astar()
            
def get_successor(city):
    return None
    
def readFiles():
    # Parsing the file - 
    with open('city-gps.txt') as fin:
        for line in fin:
            lineSplit = line.split()
            city_gps.update({lineSplit[0]:{"latitude": float(lineSplit[1]), "longitude": float(lineSplit[2])}})
	#print city_gps
            
    # Parsing the file - 
    with open('road-segments.txt') as fin:
        for line in fin:
            lineSplit = line.split()
            if len(lineSplit) == 5 and int(lineSplit[2]) and int(lineSplit[3]):
                road_segments.update({lineSplit[0]+"|"+lineSplit[1]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
                    "isHighway":1 if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":"", "costToNode":0,\
			"timeToNode" : 0.0,"distToNode":0.0}}); 
                road_segments.update({lineSplit[1]+"|"+lineSplit[0]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
                    "isHighway":1 if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":"", "costToNode":0,
			"timeToNode":0.0, "distToNode":0.0}});
            
#read Text Files     
readFiles()
#Reac program run arguments
startCity=sys.argv[1]
endCity=sys.argv[2]
routingOption=sys.argv[3]
routingAlgorithm=sys.argv[4]
if startCity != endCity:
	get_driving_directions(startCity,endCity,routingOption,routingAlgorithm)
	print "\nLatLong Distance between Source and Destination is - ",calc_heuristic(startCityName, endCityName), "miles\n"
	print "\n[total-distance-in-miles:", goal_dist, "] [total-time-in-hours:", goal_time,"] ", goal_path
else: 
	print "\nStart City and End City are same ! Re-run the program with different set of arguments\n"


    
    
