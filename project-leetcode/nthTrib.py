def tribonacci( n: int) -> int:
    T = [0, 1, 1]

    for i in range(3, n+1):
        T.append(T[i-1] + T[i-2]+T[i-3])
    return T[n]

if __name__ == '__main__':
    print(tribonacci(25))