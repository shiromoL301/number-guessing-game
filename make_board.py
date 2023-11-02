import numpy as np

from src.utils import into_speech_bubble
from src.code import NumberGuessingCode
from src.config import genres


#config.pyとgenres.json
C = NumberGuessingCode(genres[4])
C.make_board()