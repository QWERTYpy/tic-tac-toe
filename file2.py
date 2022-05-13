f = open('txt_XO.txt')
ff = open('txt_XO_m.txt', 'w')
mass = []
for line in f:
    state, action, reward, next_state, done, hod = line.split(',')
    hod = hod.strip()
    reward = reward.strip()
    if hod == 'Error_hod': # Если неправильный ход -10
        reward = '-1'
    if hod == 'Perebil':  # Если перебил ход 1
        reward = '1'
    if hod == 'Game_Over': # Если проигрыш на следующем ходу -1
        reward = '-1'
    if hod == 'Draw_X': # Если ничья на следующем ходу 1
        reward = '1'
    if hod == 'G_O': # Если проиграл -1
        reward = '-1'
    if hod == 'Win': # Если победил 2
        reward = '1'
    if hod == 'Draw_O':  # Если ничья 1
        reward = '1'
    if hod == 'Hod':  # Если простой ход 0.5
        reward = '0'
    ff.write(f'{state},{action}, {reward},{next_state}, {done}, {hod}\n')