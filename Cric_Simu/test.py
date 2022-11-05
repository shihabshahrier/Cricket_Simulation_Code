balling_team = {'A1':"Bat", 'A2':"Bat", 'A3':"Bat", 'A4':"Bat", 'A5':"Bat", 'A6':"All", 'A7':"ball", 'A8':"ball", 'A9':"ball", 'A10':"ball", 'A11':"ball"}

balling_lineup = [key for key in balling_team.keys() if balling_team[key] == 'ball' or balling_team[key] == 'All']
print(balling_lineup)