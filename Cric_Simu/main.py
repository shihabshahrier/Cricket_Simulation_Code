import random as rand
import time as T


class MatchDay:
    def __init__(self, team_A, team_B, overs):
        self.team_a = team_A
        self.team_b = team_B
        self.overs = overs

    def toss(self):

        return rand.choice([1, 2]) # 1 -> team_A; 2 -> team_B;

    def choice(self):

        return rand.choice([0, 1]) # 0 -> Bat; 1 -> ball;
    
    def innings(self, batting_team, balling_team, overs, target = 0):

        det = - 1 # -1 -> 1st innings; 0 -> lost; 1 -> won;

        batting_lineup = list(batting_team.keys())

        balling_lineup = list(balling_team.keys())


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

        over = 0
        while over < overs or up_coming_batsman < len(batting_lineup):
            if prev_baller is None:
                baller = rand.choice(balling_lineup)
            else:
                pid = balling_lineup.index(prev_baller) # prev_baller index
                baller = rand.choice(balling_lineup[:pid] + balling_lineup[pid+1:]) # removing prev_baller since baller can't ball 2 consecutive overs

            for j in range(1, 7): # j -> every ball
                
                if prev_delivery is None:
                    delivery = rand.choice([0, 1, 2, 3, 4, 5, 6, 'WD', 'NB', 'WKT']) # WD -> wide delivery; NB -> no ball; WKT -> wicket
                
                elif prev_delivery == 'NB':         # if prev_delivery is no ball then next delivery must be Free hit;
                    delivery = rand.choice([0, 1, 2, 3, 4, 5, 6, 'WD', 'NB'])
                    prev_delivery = None

                if delivery == 'WD':
                    j -= 1
                    extra_runs += 1

                elif delivery == 'NB':
                    j -= 1
                    extra_runs += 1
                    prev_delivery = 'NB'

                elif delivery == 'WKT':                              # Wicket
                    balling_team_timeline[baller][1] += 1
                    if up_coming_batsman < len(batting_lineup):
                        strike = batting_lineup[up_coming_batsman]
                        up_coming_batsman += 1
                    else:
                        break

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
                    det = 1
                    return batting_team_timeline, balling_team_timeline, extra_runs, total_runs, det

            strike, non_strike = non_strike, strike # changing strike after every over
            balling_team_timeline[baller][0] += 1
            prev_baller = baller
            over += 1

        if target != 0 and total_runs < target:
            det = 0

        return batting_team_timeline, balling_team_timeline, extra_runs, total_runs, det

    def result(self, team_A, team_B, overs):

        toss = self.toss()
        choice = self.choice()

        if toss == 1:
            if choice == 0:
                batting_team = team_A
                balling_team = team_B
            else:
                batting_team = team_B
                balling_team = team_A
        else:
            if choice == 0:
                batting_team = team_B
                balling_team = team_A
            else:
                batting_team = team_A
                balling_team = team_B

        #print('Batting team: ', batting_team)
        #print('Balling team: ', balling_team)
        team_a_total_runs = 0
        team_b_total_runs = 0
        if batting_team == team_A:
            team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs, w1 = self.innings(batting_team, balling_team, overs)
        elif batting_team == team_B:
            team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs, w2 = self.innings(batting_team, balling_team, overs)
        
        if balling_team == team_A:
            team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs, w1 = self.innings(batting_team, balling_team, overs, team_a_total_runs+1)
        elif balling_team == team_B:
            team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs, w2 = self.innings(batting_team, balling_team, overs, team_b_total_runs+1)
        
        print('Team A batting timeline: ', team_a_batting_timeline)
        print("team A balling timeline: ", team_a_balling_timeline)
        print('Team B batting timeline: ', team_b_batting_timeline)
        print('Team B balling timeline: ', team_b_balling_timeline)
        if w1 == 1 or w2 == 0:
            print('Team A won')
        elif w1 == 0 or w2 == 1:
            print('Team B won')
        else:
            print('Match Drawn')


if __name__ == '__main__':
    team_A = {'A1': [0, 0], 'A2': [0, 0], 'A3': [0, 0], 'A4': [0, 0], 'A5': [0, 0], 'A6': [0, 0], 'A7': [0, 0], 'A8': [0, 0], 'A9': [0, 0], 'A10': [0, 0], 'A11': [0, 0]}
    team_B = {'B1': [0, 0], 'B2': [0, 0], 'B3': [0, 0], 'B4': [0, 0], 'B5': [0, 0], 'B6': [0, 0], 'B7': [0, 0], 'B8': [0, 0], 'B9': [0, 0], 'B10': [0, 0], 'B11': [0, 0]}
    overs = 5
    match = MatchDay(team_A, team_B, overs)
    match.result(team_A, team_B, overs)


                    
                    