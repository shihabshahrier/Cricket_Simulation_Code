import random as rand

def innings(batting_team, balling_team, overs, target = 0):

    batting_lineup = list(batting_team.keys())
    # print("Batting lineup: ", batting_lineup)

    balling_lineup = [key for key in balling_team.keys() if balling_team[key] == 'Ball' or balling_team[key] == 'All']
    # print("Balling lineup: ", balling_lineup)

    # key -> bat's_man ; value -> [Run -> 0; Ball_faced -> 0]
    batting_team_timeline = {i: [0, 0] for i in batting_lineup}

    # key -> Boller ; value -> [over -> 0; wicket_taken-> 0]
    balling_team_timeline = {i: [0, 0] for i in balling_lineup}

    extra_runs = 0

    total_runs = 0 

    strike = batting_lineup[0]
    non_strike = batting_lineup[1]
    up_coming_batsman = 2
    prev_baller = None
    prev_delivery = None
    print("overs", overs)
    over = 0
    c = 0
    while over < overs and up_coming_batsman < len(batting_lineup):

        if prev_baller is None:
            baller = rand.choice(balling_lineup)
        else:
            pid = balling_lineup.index(prev_baller) # prev_baller index
            baller = rand.choice(balling_lineup[:pid] + balling_lineup[pid+1:]) # removing prev_baller since baller can't ball 2 consecutive overs
        j = 1
    
        #for j in range(1, 7): # j -> every ball
        while j < 7:

            if prev_delivery is None:
                delivery = rand.choice([0, 1, 2, 3, 4, 5, 6, 'WD', 'NB', 'WKT']) # WD -> wide delivery; NB -> no ball; WKT -> wicket
            
            elif prev_delivery == 'NB':         # if prev_delivery is no ball then next delivery must be Free hit;
                delivery = rand.choice([0, 1, 2, 3, 4, 5, 6, 'WD', 'NB'])
                if delivery != 'NB' and delivery != 'WD':
                    prev_delivery = None
            #print(delivery)
            if delivery == 'WD':
                j -= 1
                extra_runs += 1
                total_runs += 1
                c+=1

            elif delivery == 'NB':
                j -= 1
                extra_runs += 1
                total_runs += 1
                prev_delivery = 'NB'
                c+=1

            elif delivery == 'WKT':                              # Wicket
                balling_team_timeline[baller][1] += 1
                if up_coming_batsman < len(batting_lineup):
                    strike = batting_lineup[up_coming_batsman]
                    up_coming_batsman += 1
                else:
                    print(c)
                    return batting_team_timeline, balling_team_timeline, extra_runs, total_runs

            elif delivery % 2 != 0 and delivery != 5:            # odd runs
                batting_team_timeline[strike][0] += delivery
                batting_team_timeline[strike][1] += 1
                strike, non_strike = non_strike, strike
                total_runs += delivery
            else:
                batting_team_timeline[strike][0] += delivery
                batting_team_timeline[strike][1] += 1
                total_runs += delivery
            
            if target != 0 and total_runs >= target:

                return batting_team_timeline, balling_team_timeline, extra_runs, total_runs
            j += 1


        strike, non_strike = non_strike, strike # changing strike after every over
        balling_team_timeline[baller][0] += 1
        prev_baller = baller
        over += 1
    print("c",c)

    return batting_team_timeline, balling_team_timeline, extra_runs, total_runs

team_A = {'A1':"Bat", 'A2':"Bat", 'A3':"Bat", 'A4':"Bat", 'A5':"Bat", 'A6':"All", 'A7':"Ball", 'A8':"Ball", 'A9':"Ball", 'A10':"Ball", 'A11':"Ball"}
team_B = {'B1':"Bat", 'B2':"Bat", 'B3':"Bat", 'B4':"Bat", 'B5':"Bat", 'B6':"All", 'B7':"Ball", 'B8':"Ball", 'B9':"Ball", 'B10':"Ball", 'B11':"Ball"}
overs = 5
target = 0
batting_team_timeline, balling_team_timeline, extra_runs, total_runs = innings(team_A, team_B, overs, target)
print("Batting team timeline: ", batting_team_timeline)
print("Balling team timeline: ", balling_team_timeline)
print("Extra runs: ", extra_runs)
print("Total runs: ", total_runs)

print("#############################################")
balling_team_batting_timeline, balling_team_balling_timeline, balling_team_extra_runs, balling_team_total_runs = innings(team_B, team_A, overs, total_runs+1)
print("Batting team timeline: ", balling_team_batting_timeline)
print("Balling team timeline: ", balling_team_balling_timeline)
print("Extra runs: ", balling_team_extra_runs)
print("Total runs: ", balling_team_total_runs)

