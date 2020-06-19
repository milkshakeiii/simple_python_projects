import sys, math, copy, time, functools, heapq

POD_EVAL = 20
WIN_EVAL = 9999999
PLATINUM_EVAL = 1
INCOME_EVAL = 10
ZONE_EVAL = 0.01

class Zone:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.platinum = 0

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)


class MoveEntry:
    def __init__(self, podsCount, zoneOrigin, zoneDestination):
        self.pods_count = podsCount
        self.zone_origin_id = zoneOrigin
        self.zone_destination_id = zoneDestination


class Move:
    def __init__(self, move_entries):
        self.move_entries = move_entries

    def move_string(self):
        if len(self.move_entries) == 0:
            return "WAIT"
        move_string = ""
        for move_entry in self.move_entries:
            for argument in (move_entry.pods_count, move_entry.zone_origin_id, move_entry.zone_destination_id):
                move_string += str(argument) + " "
        return move_string


class UnturnData:
    def __init__(self,
                 zones_changed_player_0,
                 zones_changed_player_1,
                 fighting_zones_added,
                 fighting_zones_removed,
                 player_0_platinum,
                 player_1_platinum,
                 player_0_income,
                 player_1_income,
                 owners,
                 evaluation):
        self.zones_changed_player_0 = zones_changed_player_0
        self.zones_changed_player_1 = zones_changed_player_1
        self.fighting_zones_added = fighting_zones_added
        self.fighting_zones_removed = fighting_zones_removed
        self.player_0_platinum = player_0_platinum
        self.player_1_platinum = player_1_platinum
        self.player_0_income = player_0_income
        self.player_1_income = player_1_income
        self.owners = owners
        self.evaluation = evaluation


class Gamestate:
    def __init__(self,
                 player_0_pods,
                 player_1_pods,
                 owners,
                 visibles,
                 player_0_home_id,
                 player_1_home_id,
                 player_0_income,
                 player_1_income):
        self.player_0_pods = player_0_pods
        self.player_1_pods = player_1_pods
        self.owners = owners
        self.visibles = visibles
        self.player_0_platinum = 0
        self.player_1_platinum = 0
        self.player_0_home_id = player_0_home_id
        self.player_1_home_id = player_1_home_id
        self.player_0_income = player_0_income
        self.player_1_income = player_1_income
        self.fighting_zones = {}
        self.evaluation = None

    def legal_moves_generator(self, player, zones):
        legal_moves_by_zone = []
        player_pods_dict = None
        if (player == 0):
            player_pods_dict = self.player_0_pods
        if (player == 1):
            player_pods_dict = self.player_1_pods
        for zone_id in player_pods_dict.keys():
            zone = zones[zone_id]
            player_pods = 0
            player_0_pods = self.player_0_pods.get(zone.id, 0)
            player_1_pods = self.player_1_pods.get(zone.id, 0)
            player_pods = player_pods_dict.get(zone.id, 0)
            has_pods = player_pods > 0
            fighting = player_0_pods != 0 and player_1_pods != 0
            if (has_pods):
                move_list = []
                for target in zone.neighbors:
                    target_id = target.id
                    owner = self.owners.get(target_id, -1)
                    enemy_owned = (owner != player and owner !=  -1)
                    if not (fighting and enemy_owned):
                        for i in range(1, player_pods+1):
                            move_list.append((MoveEntry(i, zone.id, target_id)))
                legal_moves_by_zone.append(move_list)
        zone_moves = []
        zone_moves_counts = []
        for move_list in legal_moves_by_zone:
            zone_moves.append(0)
            zone_moves_counts.append(len(move_list))
        product = functools.reduce((lambda x, y: x * y), zone_moves_counts)
        print(str(product) + " turns available.", file=sys.stderr)
        for iteration in range(product):
            legal_move = []
            for i in range(0, len(zone_moves)):
                move_list = legal_moves_by_zone[i]
                index = zone_moves[i]
                legal_move.append(move_list[index])
            return_move = Move(legal_move)
            yield return_move
            for i in range(0, len(zone_moves)):
                zone_moves[i] = (zone_moves[i] + 1)%zone_moves_counts[i]
                if zone_moves[i] != 0:
                    break

    def evaluate(self):
        start_time=time.time()

        evaluation = 0
        evaluation += self.player_0_platinum * PLATINUM_EVAL
        evaluation -= self.player_1_platinum * PLATINUM_EVAL
        for zone_id in self.owners.keys():
            zone = zones[zone_id]
            player_0_pods = self.player_0_pods.get(zone_id, 0)
            player_1_pods = self.player_1_pods.get(zone_id, 0)
            evaluation += player_0_pods * POD_EVAL
            evaluation -= player_1_pods * POD_EVAL
            if (self.owners[zone_id] == 0):
                evaluation += (zone.platinum * INCOME_EVAL + ZONE_EVAL)
            if (self.owners[zone_id] == 1):
                evaluation -= (zone.platinum * INCOME_EVAL + ZONE_EVAL)
            if self.owners[self.player_0_home_id] == 1:
                evaluation -= WIN_EVAL
            if self.owners[self.player_1_home_id] == 0:
                evaluation += WIN_EVAL

        #print("evaluation runtime: " + str(time.time() - start_time), file=sys.stderr)
        self.evaluation = evaluation

    def unturn(self, unturn_data):
        for zone in unturn_data.fighting_zones_added:
            del self.fighting_zones[zone]
        for zone in unturn_data.fighting_zones_removed:
            self.fighting_zones[zone] = True
        for zone in unturn_data.zones_changed_player_0.keys():
            self.player_0_pods[zone] = unturn_data.zones_changed_player_0[zone]
        for zone in unturn_data.zones_changed_player_1.keys():
            self.player_1_pods[zone] = unturn_data.zones_changed_player_1[zone]
        for zone in unturn_data.owners.keys():
            self.owners[zone] = unturn_data.owners[zone]
        self.player_0_platinum = unturn_data.player_0_platinum
        self.player_1_platinum = unturn_data.player_1_platinum
        self.player_0_income = unturn_data.player_0_income
        self.player_1_income = unturn_data.player_1_income
        self.evaluation = unturn_data.evaluation

    def turn(self, player0moves, player1moves, zones):
        start_time = time.time()

        zones_changed_player_0 = {}
        zones_changed_player_1 = {}
        fighting_zones_added = []
        fighting_zones_removed = []
        unturn_player_0_platinum = self.player_0_platinum
        unturn_player_1_platinum = self.player_1_platinum
        unturn_player_0_income = self.player_0_income
        unturn_player_1_income = self.player_1_income
        unturn_owners = {}
        unturn_evaluation = self.evaluation
        
        #moving
        for move in player0moves.move_entries:
            if move.zone_destination_id not in self.player_0_pods:
                self.player_0_pods[move.zone_destination_id] = 0
            zones_changed_player_0 [move.zone_origin_id] = self.player_0_pods[move.zone_origin_id]
            zones_changed_player_0 [move.zone_destination_id] = self.player_0_pods[move.zone_destination_id]
            self.player_0_pods[move.zone_origin_id] -= move.pods_count
            self.player_0_pods[move.zone_destination_id] += move.pods_count
            
        for move in player1moves.move_entries:
            if move.zone_destination_id not in self.player_1_pods:
                self.player_1_pods[move.zone_destination_id] = 0
            zones_changed_player_1[move.zone_origin_id] = self.player_1_pods[move.zone_origin_id]
            zones_changed_player_1[move.zone_destination_id] = self.player_1_pods[move.zone_destination_id]
            self.player_1_pods[move.zone_origin_id] -= move.pods_count
            self.player_1_pods[move.zone_destination_id] += move.pods_count

        #buying
        player_0_new_pods = self.player_0_platinum//20
        self.evaluation += player_0_new_pods * POD_EVAL
        player_1_new_pods = self.player_1_platinum//20
        self.evaluation -= player_0_new_pods * POD_EVAL
        self.player_0_platinum -= player_0_new_pods * 20
        self.evaluation -= 20 * player_0_new_pods * PLATINUM_EVAL
        self.player_1_platinum -= player_1_new_pods * 20
        self.evaluation += 20 * player_1_new_pods * PLATINUM_EVAL
        if (player_0_new_pods != 0):
            if (self.player_0_home_id not in self.player_0_pods):
                self.player_0_pods[self.player_0_home_id] = 0
            zones_changed_player_0[self.player_0_home_id] = self.player_0_pods[self.player_0_home_id]
            self.player_0_pods[self.player_0_home_id] += player_0_new_pods
        if (player_1_new_pods != 0):
            if (self.player_1_home_id not in self.player_1_pods):
                self.player_1_pods[self.player_1_home_id] = 0
            zones_changed_player_1[self.player_1_home_id] = self.player_1_pods[self.player_1_home_id]
            self.player_1_pods[self.player_1_home_id] += player_1_new_pods
        
        #distributing
        self.player_0_platinum += self.player_0_income
        self.evaluation += self.player_0_income * PLATINUM_EVAL
        self.player_1_platinum += self.player_1_income
        self.evaluation -= self.player_1_income * PLATINUM_EVAL

        #fighting
        for zone_id in list(zones_changed_player_0.keys()) + list(zones_changed_player_1.keys()):
            has_p0_pods = zone_id in self.player_0_pods and self.player_0_pods[zone_id] != 0
            has_p1_pods = zone_id in self.player_1_pods and self.player_1_pods[zone_id] != 0
            if has_p0_pods and has_p1_pods:
                fighting_zones_added.append(zone_id)
        for zone_id in self.fighting_zones.keys():
            player_0_pods = self.player_0_pods.get(zone_id, 0)
            player_1_pods = self.player_1_pods.get(zone_id, 0)
            annihilate_no = min(3, player_0_pods, player_1_pods)
            if (annihilate_no != 0):
                zones_changed_player_0[zone_id] = self.player_0_pods[zone_id]
                zones_changed_player_1[zone_id] = self.player_1_pods[zone_id]
                self.player_0_pods[zone_id] -= annihilate_no
                self.evaluation -= annihilate_no * POD_EVAL
                self.player_1_pods[zone_id] -= annihilate_no
                self.evaluation += annihilate_no * POD_EVAL
            if (self.player_0_pods[zone_id] == 0 or self.player_1_pods[zone_id] == 0):
                fighting_zones_removed.append(zone_id)
        for zone_id in fighting_zones_removed:
            del self.fighting_zones[zone_id]
        for zone_id in fighting_zones_added:
            self.fighting_zones[zone_id] = True

        #owning
        for zone_id in list(zones_changed_player_0.keys()) + list(zones_changed_player_1.keys()):
            platinum = zones[zone_id].platinum
            player_0_pods = self.player_0_pods.get(zone_id, 0)
            player_1_pods = self.player_1_pods.get(zone_id, 0)
            if player_0_pods == 0 and player_1_pods != 0:
                if zone_id in self.owners and (self.owners[zone_id]) == 0:
                    self.player_0_income -= platinum
                    self.evaluation -= platinum * INCOME_EVAL
                    self.evaluation -= ZONE_EVAL
                if (not (zone_id in self.owners)) or (self.owners[zone_id] != 1):
                    unturn_owners[zone_id] = self.owners.get(zone_id, -1)
                    self.owners[zone_id] = 1
                    self.player_1_income += platinum
                    self.evaluation -= platinum * INCOME_EVAL
                    self.evaluation -= ZONE_EVAL
            if player_1_pods == 0 and player_0_pods != 0:
                if zone_id in self.owners and (self.owners[zone_id]) == 1:
                    self.player_1_income -= platinum
                    self.evaluation += platinum * INCOME_EVAL
                    self.evaluation += ZONE_EVAL
                if (not (zone_id in self.owners)) or (self.owners[zone_id] != 0):
                    unturn_owners[zone_id] = self.owners.get(zone_id, -1)
                    self.owners[zone_id] = 0
                    self.player_0_income += platinum
                    self.evaluation += platinum * INCOME_EVAL
                    self.evaluation += ZONE_EVAL
        if self.owners[self.player_0_home_id] == 1:
            self.evaluation -= WIN_EVAL
        if self.owners[self.player_1_home_id] == 0:
            self.evaluation += WIN_EVAL
    
        #print("turn runtime: " + str(time.time() - start_time), file=sys.stderr)
        return UnturnData(zones_changed_player_0,
                          zones_changed_player_1,
                          fighting_zones_added,
                          fighting_zones_removed,
                          unturn_player_0_platinum,
                          unturn_player_1_platinum,
                          unturn_player_0_income,
                          unturn_player_1_income,
                          unturn_owners,
                          unturn_evaluation)

def bfs(gamestate, player, seconds, zones):
    start_time = time.time()
    entry_counter = 0
    gamestate.evaluate()
    best_plan = (gamestate.evaluation, -1, None, [])
    frontier = [best_plan]
    loop_count = 0
    small_loop_count = 0
    longest_loop = 0
    if True:
        loop_count += 1
        #expand_me = heapq.heappop(frontier)
        expand_me = frontier.pop(0)
        sequence = expand_me[3]
        for move in gamestate.legal_moves_generator(player, zones):
            loop_start = time.time()
            small_loop_count += 1
            if player == 0:
                unturn_data = gamestate.turn(move, Move([]), zones)
            else:
                unturn_data = gamestate.turn(Move([]), move, zones)
            this_plan = (gamestate.evaluation, entry_counter, None, sequence + [move])
            entry_counter += 1
            #heapq.heappush(frontier, this_plan)
            frontier.append(this_plan)
            if (gamestate.evaluation > best_plan[0] and player == 0) or (gamestate.evaluation < best_plan[0] and player == 1):
                best_plan = this_plan
                print([m.move_string() for m in best_plan[3]], file=sys.stderr)
                print(best_plan[0], file=sys.stderr)
            loop_end = time.time()
            loop_time = loop_end - loop_start
            longest_loop = max(longest_loop, loop_time)
            gamestate.unturn(unturn_data)
            if ((time.time() - start_time) > seconds):
                break
    print(time.time() - start_time, file=sys.stderr)
    print("small loops: " + str(small_loop_count), file=sys.stderr)
    print("evaluation: " + str(best_plan[0]), file=sys.stderr)
    print("longest loop: " + str(longest_loop), file=sys.stderr)
    if len(best_plan[3]) == 0:
        return Move([])
    return best_plan[3][0]
    
def zoney(gamestate, player, seconds, zones):
    

# playerCount: the amount of players (always 2)
# myId: my player ID (0 or 1)
# zoneCount: the amount of zones on the map
# linkCount: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
zones = {}
for i in range(zone_count):
    # zoneId: this zone's ID (between 0 and zoneCount-1)
    # platinumSource: Because of the fog, will always be 0
    zone_id, platinum_source = [int(j) for j in input().split()]
    zones[zone_id] = Zone(zone_id)
for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    zone_1 = zones[zone_1]
    zone_2 = zones[zone_2]
    zone_1.add_neighbor(zone_2)
    zone_2.add_neighbor(zone_1)


# game loop
first_turn = True
player_0_base_id = -1
player_1_base_id = -1
while True:
    my_platinum = int(input()) # your available Platinum
    player_0_pods, player_1_pods, owners, visibles = {}, {}, {}, {}
    player_0_income, player_1_income = 0, 0
    for i in range(zone_count):
        # zId: this zone's ID
        # ownerId: the player who owns this zone (-1 otherwise)
        # podsP0: player 0's PODs on this zone
        # podsP1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
        if owner_id != -1:
            owners[z_id] = owner_id
        if pods_p0 != 0:
            player_0_pods[z_id] = pods_p0
            player_0_income += platinum
        if pods_p1 != 0:
            player_1_pods[z_id] = pods_p1
            player_1_income += platinum
        if visible:
            visibles[z_id] = visible
        zones[z_id].platinum = platinum
        if (first_turn and owner_id == 0):
            player_0_base_id = z_id
        if (first_turn and owner_id == 1):
            player_1_base_id = z_id
    print("done reading inputs", file=sys.stderr)
    first_turn = False
    
    current_gamestate = Gamestate(player_0_pods,
                                  player_1_pods,
                                  owners,
                                  visibles,
                                  player_0_base_id,
                                  player_1_base_id,
                                  player_0_income,
                                  player_1_income)

    planned_move = zoney(current_gamestate, my_id, 0.08, zones)    

    print(planned_move.move_string()) # first line for movement commands, second line no longer used (see the protocol in the statement for details)
    print("WAIT")
