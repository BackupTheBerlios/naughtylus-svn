
# from lfm
def perms2str(p):
    permis = ['x', 'w', 'r']
    perms = ['-'] * 9
    for i in range(9):
        if p & (0400 >> i):
            perms[i] = permis[(8-i) % 3]
    if p & 04000:
        perms[2] = 's'
    if p & 02000:
        perms[5] = 's'
    if p & 01000:
        perms[8] = 't'
    return "".join(perms)

