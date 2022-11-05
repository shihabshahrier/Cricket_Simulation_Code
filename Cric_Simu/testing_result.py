import random as rand
import pandas as pd
import time as T


class MatchDay:
    # def __init__(self, team_A, team_B, overs):
    #     self.team_a = team_A
    #     self.team_b = team_B
    #     self.overs = overs

    def toss(self):

        return rand.choice([1, 2]) # 1 -> team_A; 2 -> team_B;

    def choice(self):

        return rand.choice([0, 1]) # 0 -> Bat; 1 -> ball;
    
    def innings(self, batting_team, balling_team, overs, target = 0):

        batting_lineup = list(batting_team.keys())
        #print("Batting lineup: ", batting_lineup)

        balling_lineup = [key for key in balling_team.keys() if balling_team[key] == 'Ball' or balling_team[key] == 'All']
        #print("Balling lineup: ", balling_lineup)

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

        #iterating over overs
        over = 0

        while over < overs and up_coming_batsman < len(batting_lineup):
            if prev_baller is None:
                baller = rand.choice(balling_lineup)
            else:
                pid = balling_lineup.index(prev_baller) # prev_baller index
                baller = rand.choice(balling_lineup[:pid] + balling_lineup[pid+1:]) # removing prev_baller since baller can't ball 2 consecutive overs
            j = 1
        
            #for j in range(1, 7): # j -> every ball
            while j < 7:

                if prev_delivery == None:
                    delivery = rand.choice([0, 1, 2, 3, 4, 5, 6, 'WD', 'NB', 'WKT']) # WD -> wide delivery; NB -> no ball; WKT -> wicket
                
                elif prev_delivery == 'NB':         # if prev_delivery is no ball then next delivery must be Free hit;
                    delivery = rand.choice([0, 1, 2, 3, 4, 5, 6, 'WD', 'NB'])
                    if delivery != 'NB' or delivery != 'WD':
                        prev_delivery = None
                #print(delivery)
                if delivery == 'WD':
                    j -= 1
                    extra_runs += 1
                    total_runs += 1


                elif delivery == 'NB':
                    j -= 1
                    extra_runs += 1
                    total_runs += 1
                    prev_delivery = 'NB'

                elif delivery == 'WKT':                              # Wicket
                    balling_team_timeline[baller][1] += 1
                    batting_team_timeline[strike][1] += 1
                    if up_coming_batsman < len(batting_lineup):
                        strike = batting_lineup[up_coming_batsman]
                        up_coming_batsman += 1
                    
                    else:
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

        return batting_team_timeline, balling_team_timeline, extra_runs, total_runs

    def result(self, team_A, team_B, overs, tname):

        toss = self.toss()
        choice = self.choice()

        #print(toss, choice)

        team_a_total_runs = 0
        team_b_total_runs = 0

        # if toss == 1:
        #     if choice == 0:
        #         #batting_team = team_A
        #         #balling_team = team_B
        #         team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs)
        #         team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs = self.innings(team_B, team_A, overs, team_a_total_runs+1)
        #     elif choice == 1:
        #         # batting_team = team_B
        #         # balling_team = team_A
        #         team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs = self.innings(team_B, team_A, overs)
        #         team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs, team_b_total_runs+1)
                
        # elif toss == 2:
        #     if choice == 0:
        #         # batting_team = team_B
        #         # balling_team = team_A
        #         team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs = self.innings(team_B, team_A, overs)
        #         team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs, team_b_total_runs+1)
        #     elif choice == 1:
        #         # batting_team = team_A
        #         # balling_team = team_B
        #         team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs)
        #         team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs = self.innings(team_B, team_A, overs, team_a_total_runs+1)

        print(f"{tname[toss-1]} won the toss and elected to {['bat', 'ball'][choice]} first")

        if (toss == 1 and choice == 0) or (toss == 2 and choice == 1):
            team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs)
            team_a_batting_showcase = pd.DataFrame(team_a_batting_timeline, index=['Runs', 'Balls'])

            print(f"After {overs} overs, {tname[0]} scored {team_a_total_runs}")
            print()
            print("Batting Timeline")
            print(team_a_batting_showcase.transpose())
            print()
            print("Balling Timeline")
            print(pd.DataFrame(team_b_balling_timeline, index=['Overs', 'Wickets']))
            target = team_a_total_runs + 1
            print(f"Now {tname[1]} needs {target} runs to win")
            print()
            team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs = self.innings(team_B, team_A, overs, target)
            team_b_balling_showcase = pd.DataFrame(team_b_balling_timeline, index=['Overs', 'Wickets'])
            print(f"After {overs} overs, {tname[1]} scored {team_b_total_runs}")
            print()
            print("Batting Timeline")
            print(team_b_batting_timeline)
            print()
            print("Balling Timeline")
            print(team_b_balling_showcase.transpose())

        else:
            team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs = self.innings(team_B, team_A, overs)
            team_b_batting_showcase = pd.DataFrame(team_b_batting_timeline, index=['Runs', 'Balls'])
            print(f"After {overs} overs, {tname[1]} scored {team_b_total_runs}")
            print()
            print("Batting Timeline")
            print(team_b_batting_showcase.transpose())
            print()
            print("Balling Timeline")
            print(pd.DataFrame(team_a_balling_timeline, index=['Overs', 'Wickets']))


            target = team_b_total_runs + 1
            print(f"Now {tname[0]} needs {target} runs to win")
            print()
            team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs, target)
            team_a_batting_showcase = pd.DataFrame(team_a_batting_timeline, index=['Runs', 'Balls'])
            print(f"After {overs} overs, {tname[0]} scored {team_a_total_runs}")
            print()
            print("Batting Timeline")
            print(team_a_batting_showcase.transpose())
            print()
            print("Balling Timeline")
            print(pd.DataFrame(team_b_balling_timeline, index=['Overs', 'Wickets']))


            team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs = self.innings(team_A, team_B, overs, team_b_total_runs+1)
            team_a_balling_showcase = pd.DataFrame(team_a_balling_timeline, index=['Overs', 'Wickets'])
            
            

        #print('Batting team: ', batting_team)
        #print('Balling team: ', balling_team)
        # team_a_total_runs = 0
        # team_b_total_runs = 0

        # if batting_team == team_A:
        #     team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs, w1 = self.innings(batting_team, balling_team, overs)
        # elif batting_team == team_B:
        #     team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs, w2 = self.innings(batting_team, balling_team, overs)
        
        # if balling_team == team_A:
        #     team_a_batting_timeline, team_b_balling_timeline, team_a_extra_runs, team_a_total_runs, w1 = self.innings(batting_team, balling_team, overs, team_a_total_runs+1)
        # elif balling_team == team_B:
        #     team_b_batting_timeline, team_a_balling_timeline, team_b_extra_runs, team_b_total_runs, w2 = self.innings(batting_team, balling_team, overs, team_b_total_runs+1)
        
        # print('Team A batting timeline: ', team_a_batting_timeline)
        # c = 0
        # for i in team_a_batting_timeline:
        #     c += team_a_batting_timeline[i][1]
        # print("Team A total balls: ", c)
        #print("team A balling timeline: ", team_a_balling_timeline)
        #print("team B batting timeline: ", team_b_batting_timeline)
        #print('Team B balling timeline: ', team_b_balling_timeline)

        


        # team_b_batting_showcase = pd.DataFrame(team_b_batting_timeline, index = ["Runs", "Balls"])
        # team_a_balling_showcase = pd.DataFrame(team_a_balling_timeline, index = ["Overs", "Wickets"])

        # print(team_a_batting_showcase.transpose())
        # print()
        # print(team_a_balling_showcase)
        # print()
        # print(team_b_batting_showcase.transpose())
        # print()
        # print(team_b_balling_showcase)
        # print()



        print()
        # print("Team A total runs: ", team_a_total_runs)
        # print("Team B total runs: ", team_b_total_runs)
        print(f"# {'-'*20} Match result {'-'*20} #")
        print()
        if team_a_total_runs > team_b_total_runs:
            print(f"{tname[0]} won")
        elif team_a_total_runs < team_b_total_runs:
            print(f"{tname[1]} won")
        else:
            print(f"Match tied between {tname[0]} and {tname[1]}")
        print()

if __name__ == '__main__':
    team_A = {'A1':"Bat", 'A2':"Bat", 'A3':"Bat", 'A4':"Bat", 'A5':"Bat", 'A6':"All", 'A7':"Ball", 'A8':"Ball", 'A9':"Ball", 'A10':"Ball", 'A11':"Ball"}
    team_B = {'B1':"Bat", 'B2':"Bat", 'B3':"Bat", 'B4':"Bat", 'B5':"Bat", 'B6':"All", 'B7':"Ball", 'B8':"Ball", 'B9':"Ball", 'B10':"Ball", 'B11':"Ball"}
    t_name = ["Bangladesh", "India"]
    overs = 5
    match = MatchDay()#team_A, team_B, overs)
    match.result(team_A, team_B, overs, t_name)


                    
                    