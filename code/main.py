from RSPgame import RSPgame

model = RSPgame()
model.KNN_init()
model.making_system_rps()
result = model.game()

print(result)
# {0:'rock', 1:'12scissors', 2:'paper', 3:'23-scissors'}