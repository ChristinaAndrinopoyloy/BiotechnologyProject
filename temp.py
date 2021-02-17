for i in range(10):
    print(f'---------------------i={i}')
    for j in range(12):
        if j == 2 or j ==4 or j == 6:
            continue
        else:
            print(f'j={j}')