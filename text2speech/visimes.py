from ovos_utils.lang.phonemes import get_phonemes, ipa2arpabet, arpabet2ipa
from ovos_utils.lang.visimes import VISIMES


if __name__ == "__main__":

    words = ["hey mycroft", "hey chatterbox", "alexa", "siri", "cortana"]
    for w in words:
        print(w, get_phonemes(w))

    """
    hey mycroft HH EY1 . M Y K R OW F T
    hey chatterbox HH EY1 . CH AE T EH R B OW K S
    alexa AH0 L EH1 K S AH0
    siri S IH1 R IY0
    cortana K OW R T AE N AE
    """