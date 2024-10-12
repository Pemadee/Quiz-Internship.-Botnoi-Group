def starPattern(star):
    for i in range(1, star + 1):
        print('*' * i)
    for i in range(star - 1, 0, -1):
        print('*' * i)

starPattern(5)