# 必要なモジュールをインポートする
import numpy as np
from nptyping import NDArray, Int, Shape

from src.utils import into_speech_bubble
import config


# 各パラメータを設定する
I4 = np.eye(4, dtype=int)
I3 = np.eye(3, dtype=int)
P = np.array([
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
], dtype=int)
G = np.hstack((I4, P))
H = np.hstack((P.T, I3))
code_dict = dict()
vec_info_dict = dict()


# 関数を定義する
def parity_check(r_code: NDArray[Shape["1, 7"], Int]) -> tuple[NDArray[Shape["1, 3"], Int], NDArray[Shape["1, 7"], Int], list[int]]:
    """パリティ検査を行う

    Args:
        r_code (NDArray[Shape["1, 7"], Int]): 受信語

    Returns:
        tuple[NDArray[Shape["1, 3"], Int], NDArray[Shape["1, 7"], Int], list[int]]: シンドローム、誤りベクトル、誤り位置の三つ組
    """
    syndrome = np.fmod(r_code@(H.T), 2)
    err_vec = np.array([int((syndrome == col).all()) for col in H.T])
    err_locs = [i for i, ei in enumerate(err_vec) if ei]

    return (syndrome, err_vec, err_locs)


def decode(r_code: NDArray[Shape["1, 7"], Int]) -> NDArray[Shape["1, 7"], Int]:
    """受信語を復号する

    Args:
        r_code (NDArray[Shape["1, 7"], Int]): 受信語

    Returns:
        NDArray[Shape["1, 7"], Int]: 復号および誤り訂正した符号語
    """
    err_vec = parity_check(r_code)[1]

    return np.fmod(err_vec + r_code, 2)


def codeword_to_character(d_code: NDArray[Shape["1, 7"], Int]) -> str:
    """復号した符号語からキャラクターを取得する

    Args:
        d_code (NDArray[Shape[&quot;1, 7&quot;], Int]): 復号した符号語

    Returns:
        str: キャラクター名
    """
    name_list = config.name_list

    return name_list[vec_info_dict[tuple(d_code)]-1]


# 符号語を生成して番号をつける
for i in range(1, 16):
    b = bin(i)[2:].zfill(4)

    s = np.array([0, 0, 0, 0, 0, 0, 0])
    for loc in range(3, -1, -1):
        if int(b[loc]):
            s += G[loc]
            s = np.fmod(s, 2)

    code_dict[i] = s
    vec_info_dict[tuple(s)] = i


def main():
    while True:
        r_code = np.array([int(input(f"{i}番目")) for i in range(1,8)])
        _, _, err_locs = parity_check(r_code)
        err_loc_str = f"{err_locs[0] + 1} 番目" if err_locs else "なし"
        d_code = decode(r_code)
        character_name = codeword_to_character(d_code)
        print(f"受信語: {r_code}")
        print(f"復号語: {d_code}")
        print(f"誤り位置: {err_loc_str}")
        print("あなたが思い浮かべていたのは......")
        print(into_speech_bubble(character_name))
        print("続けますか? (Y/n)")
        if input() in {"n", "N"}:
            break


def make_board():
    name_list = config.name_list
    L = [[] for _ in range(7)]
    for key in code_dict.keys():
        for i in range(7):
            if code_dict[key][i] and (key-1) < len(name_list):
                L[i].append(name_list[key-1])

    [print(f"{i+1} 枚目: {row}") for i, row in enumerate(L)]

make_board()
main()
