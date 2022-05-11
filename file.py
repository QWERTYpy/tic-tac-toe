f = open('text_XO.txt')
ff = open('txt_XO.txt', 'w')
mass = []
for line in f:
    ln = line[:-1]
    flag = False

    for ms in mass:
        if ln == ms:
            flag = True

    if not flag:
        mass.append(ln)
print(len(mass))
for ms in mass:
    ff.write(f'{ms}\n')