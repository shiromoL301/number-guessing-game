# 必要なモジュールをインポートする
import numpy as np

from src.utils import into_speech_bubble
from src.code import NumberGuessingCode


def main():
    while True:
        r_code = np.array([int(input(f"{i}番目")) for i in range(1,8)])
        _, _, err_locs = C.parity_check(r_code)
        err_loc_str = f"{err_locs[0] + 1} 番目" if err_locs else "なし"
        d_code = C.decode(r_code)
        character_name = C.codeword_to_character(d_code)
        print(f"受信語: {r_code}")
        print(f"復号語: {d_code}")
        print(f"誤り位置: {err_loc_str}")
        print("あなたが思い浮かべたのは...")
        print("#もしかして:")
        print(into_speech_bubble(character_name))
        print("続けますか? (Y/n)")
        if input() in {"n", "N"}:
            break

if __name__ == "__main__":
    C = NumberGuessingCode()
    C.make_board()
    main()
