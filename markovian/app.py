import sys

from .models.markov import Markov

def identify_speaker(speech1, speech2, speech3, k):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "k-order"
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    Input:
        speech1(str): text from an identified speaker
        speech2(str): text from an identified speaker
        speech3(str): text from an unidentified speaker
        k(int): a positive value used for order
    Returns(str): speaker who is more likely
    """
    modelA = Markov(k, speech1)
    modelB = Markov(k, speech2)

    probA = modelA.log_probability(speech3) / len(speech3)
    probB = modelB.log_probability(speech3) / len(speech3)

    return probA, probB, "A" if probA > probB else "B"

import pathlib

def run():
    if len(sys.argv) != 5:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k>"
        )
        sys.exit(1)

    fileA = pathlib.Path(__file__).parent / "speeches" / sys.argv[0]
    fileB = pathlib.Path(__file__).parent / "speeches" / sys.argv[1]
    fileC = pathlib.Path(__file__).parent / "speeches" / sys.argv[2]
    k = int(sys.argv[3])

    actual = identify_speaker(
        fileA.read_text(), fileB.read_text(), fileC.read_text(), k
    )
    print('Speaker A: ' + actual[0])
    print('Speaker B: ' + actual[1])
    print('Conclusion: Speaker ' + actual[2] + ' is most likely')
