import sys, math, copy, time


class Zone:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.player_0_pods = 0
        self.player_1_pods = 0
        self.owner = -1
        self.visible = false
        self.platinum = 0

    def add_neighbor(neighbor):
        self.neighbors.add(neighbor)


class MoveEntry:
    def __init__(self, podsCount, zoneOrigin, zoneDestination):
        self.pods_count = podsCount
        self.zone_origin_id = zoneOrigin
        self.zone_destination_id = zoneDestination


class Move:
    def __init__(self, move_entries):
        self.move_entries = move_entries

    def move_string(self):
        move_string = ""
        for move_entry in self.move_entries:
            for argument in (move_entry.pods_count, move_entry.zone_origin_id, move_entry.zone_destination_id):
                movestring += str(argument) + " "
        

class Gamestate:
    def __init__(self, zones, player_0_home_id, player_0_home_id):
        self.zones = zones
        self.player_0_platinum = 0
        self.player_1_platinum = 1
        self.player_0_home_id = player_0_home_id
        self.player_1_home_id = player_1_home_id

    def legal_moves(self, player):
        legal_moves_by_zone = {}
        for zone in zones.values():
            player_pods = 0
            if (player == 0):
                player_pods = zone.player_0_pods
            if (player == 1):
                player_pods = zone.player_1_pods
            for target_id in zone.neighbors:
                fighting = zone.player_0_pods != 0 and zone.player_1_pods != 0
                enemy_owned = (player == 0 and zones[target_id].owner == 1) or (player == 1 and zones[target_id].owner == 0)
                if not (fighting and enemy_owned):
                    for i in range(1, player_pods+1):
                        legal_moves_by_zone.append(MoveEntry(i, zone.id, target_id))
        legal_moves = []
        zone_moves = []
        zone_moves_counts = []
        for move_list in legal_moves_by_zone:
            zone_moves.append(0)
            zone_moves_counts.append(len(move_list))
        while zone_moves != zone_moves_counts:
            legal_move = []
            for i in range(0, len(zone_moves)):
                legal_move.append(legal_moves_by_zone[i][zone_moves[i]])
            legal_moves.append(legal_move)
            for i in range(0, len(zone_moves)):
                zone_moves[i] += 1
                if zone_moves[i]%zone_moves_counts[i] != 0:
                    break
        return legal_moves

    def evaluation(self):
        evaluation = 0
        evaluation += player_0_platinum
        evaluation -= player_1_platinum
        for zone in zones.values():
            evaluation += zone.player_0_pods * 20
            evaluation -= zone.player_1_pods * 20
            if (zone.owner == 0):
                evaluation += zone.platinum
            if (zone.owner == 1):
                evaluation -= zone.platinum
            if zones[self.player_0_home_id].owner == 1:
                evaluation -= 9999999
            if zones[self.player_1_home_id].owner == 0:
                evaluation += 9999999
                        

def turn(gamestate, player0moves, player1moves):
    self = copy.deepcopy(gamestate)
    
    #moving
    for move in player0moves:
        self.zones[move.zone_origin].player_0_pods -= move.pods_count
        self.zones[move.zone_destination].player_0_pods += move.pods_count
    for move in player1moves:
        self.zones[move.zone_origin].player_1_pods -= move.pods_count
        self.zones[move.zone_destination].player_1_pods += move.pods_count

    #buying
    player_0_new_pods = player_0_platinum//20
    player_1_new_pods = player_1_platinum//20
    player_0_platinum -= player_0_new_pods * 20
    player_1_platinum -= player_1_new_pods * 20
    self.zones[player_0_home_id].player_0_pods += player_0_new_pods
    self.zones[player_1_home_id].player_1_pods += player_1_new_pods

    #distributing
    for zone in self.zones.values():
        if zone.owner == 0:
            self.player_0_platinum += zone.platinum
        if zone.owner == 1:
            self.player_1_platinum += zone.platinum

    #fighting
    for zone in self.zones.values():
        annihilate_no = min(3, zone.player0pods, zone.player1pods)
        zone.player0pods -= annihilate_no
        zone.player1pods -= annihilate_no

    #owning
    for zone in self.zones.values():
        if zone.player0pods == 0 and zone.player1pods != 0:
            zone.owner = 1
        if zone.player1pods == 0 and zone.player0pods != 0:
            zone.owner = 0

    return self


def bfs(gamestate, player, seconds):
    start_time = time.time()
    best_plan = (gamestate, [], gamestate.evaluation())
    frontier = [(gamestate, [], gamestate.evaluation())]
    while (time.time() - start_time < seconds):
        expand_me = frontier.pop(0)
        gamestate = expand_me[0]
        sequence = expand_me[1]
        legal_moves = gamestate.legal_moves(player)
        for move in legal_moves:
            resultant_gamestate = turn(gamestate, move, [])
            resultant_evaluation = resultant_gamestate.evaluation()
            this_plan = (resultant_gamestate, sequence + move, resultant_evaluation)
            frontier.append(this_plan)
            if resultant_evaluation > best_found[2]:
                best_plan = this_plan

    return best_plan[1][0]
    
            

# playerCount: the amount of players (always 2)
# myId: my player ID (0 or 1)
# zoneCount: the amount of zones on the map
# linkCount: the amount of links between all zones
playerCount, myId, zoneCount, linkCount = [int(i) for i in input().split()]
zones = {}
for i in range(zoneCount):
    # zoneId: this zone's ID (between 0 and zoneCount-1)
    # platinumSource: Because of the fog, will always be 0
    zoneId, platinumSource = [int(j) for j in input().split()]
    zones[zoneId] = Zone(zoneId)
for i in range(linkCount):
    zone1, zone2 = [int(j) for j in input().split()]
    zone1.add_neighbor(zone2)
    zone2.add_neighbor(zone1)


# game loop
first_turn = True
player_0_base_id = -1
player_1_base_id = -1
while 1:
    myPlatinum = int(input()) # your available Platinum
    for i in range(zoneCount):
        # zId: this zone's ID
        # ownerId: the player who owns this zone (-1 otherwise)
        # podsP0: player 0's PODs on this zone
        # podsP1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        zId, ownerId, podsP0, podsP1, visible, platinum = [int(j) for j in input().split()]
        zones[zId].owner = ownerId
        zones[zId].player0pods = podsP0
        zones[zId].player1pods = podsP1
        zones[zId].visible = visible
        zones[zId].platinum = platinum
        if (first_turn and zones[zId].owner == 0):
            player_0_base_id = zId
        if (first_turn and zones[zId].owner == 1):
            player_1_base_id = zId
    first_turn = False

    current_gamestate = Gamestate(zones, player_0_base_id, player_1_base_id)
    
    planned_move = bfs(current_gamestate, myId)    
    
    print(planned_move.move_string()) # first line for movement commands, second line no longer used (see the protocol in the statement for details)
    print("WAIT")
