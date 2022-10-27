import numpy as np

I4 = np.eye(4, dtype = int)
I3 = np.eye(3, dtype= int)

P = np.array([
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
], dtype= int)

G = np.hstack((I4,P))
H = np.hstack((P.T, I3))


dic = dict()
for i in range(1,16):
    b = bin(i)[2:].zfill(4)

    s = np.array([0,0,0,0,0,0,0])
    for loc in range(3,-1,-1):
        if int(b[loc]):
            s = s + G[loc]
            s = np.fmod(s,2)

    dic[i] = s

def parity_check(r_code:np.array) -> np.array:
    syndrome = np.fmod(r_code@(H.T), 2)
    err_vec = np.array([int((syndrome == col).all()) for col in H.T])
    err_locs = [i for i,ei in enumerate(err_vec) if ei]

    return (syndrome, err_vec, err_locs)

def decode(r_code:np.array) -> np.array:
    err_vec = parity_check(r_code)[1]

    return np.fmod(err_vec + r_code, 2)

def main():
    while True:
        r_code = np.array([int(input(f"{i}番目")) for i in range(1,8)])

        _ , err_vec, err_locs = parity_check(r_code)
        d_code = decode(r_code)
        print("受信語")
        print(r_code)
        print("復号語")
        print(d_code)
        print("誤り位置")
        err_loc = f"{err_locs[0] + 1} 番目" if err_locs else "なし"
        print(err_loc)
        print("続けますか？(y/n)")

        INPUT = input()
        if INPUT in {"n", "N"}:
            break


L = [[] for _ in range(7)]
for key in dic.keys():
    for i in range(7):
        if dic[key][i]:
            L[i].append(key)

[print(f"{i+1} 枚目 : {row}") for i, row in enumerate(L)]
