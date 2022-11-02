import numpy as np
from nptyping import NDArray, Shape, Int

import json

from src.config import genre, assets_path, genre_filename

class NumberGuessingCode:
    def __init__(self):
        # 単位行列
        I4 = np.eye(4, dtype=int)
        I3 = np.eye(3, dtype=int)

        # パリティ検査行列の右側
        P = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ], dtype=int)

        # 生成行列
        G = np.hstack((I4, P))
        self.__generator_matrix = G

        # パリティ検査行列
        H = np.hstack((P.T, I3))
        self.__parity_check_matrix = H

        # 符号語
        self.num2codeword = dict()
        self.codeword2num = dict()
        self.denumerate_codewords()

        with open(f"{assets_path}{genre_filename}") as f:
            genres_dict = json.load(f)
        self.character_names = genres_dict[genre]

    def __iter__(self):
        G = self.generator_matrix
        for i in range(len(self)):
            coeffs = tuple(map(int, list(bin(i)[2:].zfill(4))))
            codeword = np.array([0, 0, 0, 0, 0, 0, 0])
            for loc in range(3, -1, -1):
                if int(coeffs[loc]):
                    codeword += G[loc]
                    codeword = np.fmod(codeword, 2)
            yield codeword

    def __len__(self) -> int:
        return 16

    @property
    def dimension(self) -> int:
        return 4

    @property
    def codimension(self) -> int:
        return 3

    @property
    def length(self) -> int:
        return 7

    @property
    def generator_matrix(self) -> NDArray[Shape["4, 7"], Int]:
        return self.__generator_matrix

    @property
    def parity_check_matrix(self) -> NDArray[Shape["3, 7"], Int]:
        return self.__parity_check_matrix

    def parity_check(self, r_code: NDArray[Shape["1, 7"], Int]) -> tuple[NDArray[Shape["1, 3"], Int], NDArray[Shape["1, 7"], Int], list[int]]:
        """パリティ検査を行う

        Args:
            r_code (NDArray[Shape["1, 7"], Int]): 受信語

        Returns:
            tuple[NDArray[Shape["1, 3"], Int], NDArray[Shape["1, 7"], Int], list[int]]: シンドローム、誤りベクトル、誤り位置の三つ組
        """
        H = self.parity_check_matrix
        syndrome = np.fmod(r_code@(H.T), 2)
        err_vec = np.array([int((syndrome == col).all()) for col in H.T])
        err_locs = [i for i, ei in enumerate(err_vec) if ei]

        return (syndrome, err_vec, err_locs)

    def decode(self, r_code: NDArray[Shape["1, 7"], Int]) -> NDArray[Shape["1, 7"], Int]:
        """受信語を復号する

        Args:
            r_code (NDArray[Shape["1, 7"], Int]): 受信語

        Returns:
            NDArray[Shape["1, 7"], Int]: 復号および誤り訂正した符号語
        """
        err_vec = self.parity_check(r_code)[1]

        return np.fmod(err_vec + r_code, 2)

    def codeword_to_character(self, codeword: NDArray[Shape["1, 7"], Int]) -> str:
        """符号語からキャラクター名を取得する

        Args:
            codeword (NDArray[Shape["1, 7"], Int]): 符号語

        Returns:
            str: キャラクター名
        """
        return self.character_names[self.codeword2num[tuple(codeword)]-1]

    def denumerate_codewords(self) -> tuple[dict, dict]:
        """符号語を生成し、番号づける

        Returns:
            tuple[dict, dict]: 番号->符号語の辞書、符号語->番号の辞書
        """
        G = self.generator_matrix
        for i in range(1, len(self)):
            b = bin(i)[2:].zfill(4)

            s = np.array([0, 0, 0, 0, 0, 0, 0])
            for loc in range(3, -1, -1):
                if int(b[loc]):
                    s += G[loc]
                    s = np.fmod(s, 2)

            self.num2codeword[i] = s
            self.codeword2num[tuple(s)] = i
        return (self.num2codeword, self.codeword2num)

    def make_board(self) -> None:
        L = [[] for _ in range(7)]
        for key in self.num2codeword.keys():
            for i in range(7):
                if self.num2codeword[key][i] and (key-1) < len(self.character_names):
                    L[i].append(self.character_names[key-1])

        [print(f"{i} 枚目: {row}") for i, row in enumerate(L, start=1)]
