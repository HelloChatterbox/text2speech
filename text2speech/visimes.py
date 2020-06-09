# Mapping based on Jeffers phoneme to viseme map, seen in table 1 from:
# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.221.6377&rep=rep1&type=pdf
#
# Mycroft unit visemes based on images found at:
# http://www.web3.lu/wp-content/uploads/2014/09/visemes.jpg
#
# Mapping was created partially based on the "12 mouth shapes visuals seen at:
# https://wolfpaulus.com/journal/software/lipsynchronization/
import pronouncing


VISIMES = {
    # /A group
    'v': '5',
    'f': '5',
    # /B group
    'uh': '2',
    'w': '2',
    'uw': '2',
    'er': '2',
    'r': '2',
    'ow': '2',
    # /C group
    'b': '4',
    'p': '4',
    'm': '4',
    # /D group
    'aw': '1',
    # /E group
    'th': '3',
    'dh': '3',
    # /F group
    'zh': '3',
    'ch': '3',
    'sh': '3',
    'jh': '3',
    # /G group
    'oy': '6',
    'ao': '6',
    # /Hgroup
    'z': '3',
    's': '3',
    # /I group
    'ae': '0',
    'eh': '0',
    'ey': '0',
    'ah': '0',
    'ih': '0',
    'y': '0',
    'iy': '0',
    'aa': '0',
    'ay': '0',
    'ax': '0',
    'hh': '0',
    # /J group
    'n': '3',
    't': '3',
    'd': '3',
    'l': '3',
    # /K group
    'g': '3',
    'ng': '3',
    'k': '3',
    # blank mouth
    'pau': '4',
}

########################################################################
# ARPABET was invented for English.
# The standard dictionary written in ARPABET is the CMU dictionary.

arpabet2ipa = {
    'AA': 'ɑ',
    'AE': 'æ',
    'AH': 'ʌ',
    'AH0': 'ə',
    'AO': 'ɔ',
    'AW': 'aʊ',
    'AY': 'aɪ',
    'EH': 'ɛ',
    'ER': 'ɝ',
    'ER0': 'ɚ',
    'EY': 'eɪ',
    'IH': 'ɪ',
    'IH0': 'ɨ',
    'IY': 'i',
    'OW': 'oʊ',
    'OY': 'ɔɪ',
    'UH': 'ʊ',
    'UW': 'u',
    'B': 'b',
    'CH': 'tʃ',
    'D': 'd',
    'DH': 'ð',
    'EL': 'l̩ ',
    'EM': 'm̩',
    'EN': 'n̩',
    'F': 'f',
    'G': 'ɡ',
    'HH': 'h',
    'JH': 'dʒ',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NG': 'ŋ',
    'P': 'p',
    'Q': 'ʔ',
    'R': 'ɹ',
    'S': 's',
    'SH': 'ʃ',
    'T': 't',
    'TH': 'θ',
    'V': 'v',
    'W': 'w',
    'WH': 'ʍ',
    'Y': 'j',
    'Z': 'z',
    'ZH': 'ʒ'
}

ipa2arpabet = {v: k for k, v in arpabet2ipa.items()}


def fallback_guess_phonemes(word, lang="en"):
    if not lang.startswith("en"):
        return ValueError("Unsupported language")
    word = word.lower()
    basic_pronunciations = {'a': ['AE'], 'b': ['B'], 'c': ['K'],
                           'd': ['D'],
                           'e': ['EH'], 'f': ['F'], 'g': ['G'],
                           'h': ['HH'],
                           'i': ['IH'],
                           'j': ['JH'], 'k': ['K'], 'l': ['L'],
                           'm': ['M'],
                           'n': ['N'], 'o': ['OW'], 'p': ['P'],
                           'qu': ['K', 'W'], 'r': ['R'],
                           's': ['S'], 't': ['T'], 'u': ['AH'],
                           'v': ['V'],
                           'w': ['W'], 'x': ['K', 'S'], 'y': ['Y'],
                           'z': ['Z'], 'ch': ['CH'],
                           'sh': ['SH'], 'th': ['TH'], 'dg': ['JH'],
                           'dge': ['JH'], 'psy': ['S', 'AY'],
                           'oi': ['OY'],
                           'ee': ['IY'],
                           'ao': ['AW'], 'ck': ['K'], 'tt': ['T'],
                           'nn': ['N'], 'ai': ['EY'], 'eu': ['Y', 'UW'],
                           'ue': ['UW'],
                           'ie': ['IY'], 'ei': ['IY'], 'ea': ['IY'],
                           'ght': ['T'], 'ph': ['F'], 'gn': ['N'],
                           'kn': ['N'], 'wh': ['W'],
                           'wr': ['R'], 'gg': ['G'], 'ff': ['F'],
                           'oo': ['UW'], 'ua': ['W', 'AO'], 'ng': ['NG'],
                           'bb': ['B'],
                           'tch': ['CH'], 'rr': ['R'], 'dd': ['D'],
                           'cc': ['K', 'S'], 'oe': ['OW'],
                           'igh': ['AY'], 'eigh': ['EY']}
    phones = []

    progress = len(word) - 1
    while progress >= 0:
        if word[0:3] in basic_pronunciations.keys():
            for phone in basic_pronunciations[word[0:3]]:
                phones.append(phone)
            word = word[3:]
            progress -= 3
        elif word[0:2] in basic_pronunciations.keys():
            for phone in basic_pronunciations[word[0:2]]:
                phones.append(phone)
            word = word[2:]
            progress -= 2
        elif word[0] in basic_pronunciations.keys():
            for phone in basic_pronunciations[word[0]]:
                phones.append(phone)
            word = word[1:]
            progress -= 1
        else:
            return None
    return phones


def fallback_get_phonemes(name, lang="en"):
    if not lang.startswith("en"):
        return ValueError("Unsupported language")
    name = name.lower()
    phonemes = None
    if " " in name:
        total_phonemes = []
        names = name.split(" ")
        for name in names:
            phon = fallback_get_phonemes(name)
            if phon is None:
                return None
            total_phonemes.extend(phon)
            total_phonemes.append(" . ")
        if total_phonemes[-1] == " . ":
            total_phonemes = total_phonemes[:-1]
        phonemes = "".join(total_phonemes)
    elif len(pronouncing.phones_for_word(name)):
        phonemes = "".join(pronouncing.phones_for_word(name)[0])
    else:
        guess = fallback_guess_phonemes(name)
        if guess is not None:
            phonemes = " ".join(guess)

    return phonemes


def get_phonemes(utterance, lang="en", arpabet=True, default_dur=0.4):
    try:
        #raise
        from voxpopuli import Voice
        voice = Voice(lang=lang)
        print(voice.to_phonemes(utterance))
        if arpabet:

            return [(ipa2arpabet[phoneme.name.replace("_", ".")],
                     phoneme.duration) for phoneme in
                    voice.to_phonemes(utterance)]
        else:
            return [(phoneme.name.replace("_", "pau"), phoneme.duration) for
                    phoneme in voice.to_phonemes(utterance)]
    except:
        phones = fallback_get_phonemes(utterance, lang).split()
        # some cleanup, remove digits
        phones = [pho.strip("0123456789") for pho in phones]
        if not arpabet:
            phones = [arpabet2ipa[pho.replace(".", "_")] for pho in phones]
        return [(pho, default_dur) for pho in phones]


if __name__ == "__main__":

    words = ["hey mycroft", "hey chatterbox", "alexa", "siri", "cortana"]
    for w in words:
        print(w, get_phonemes(w, arpabet=False))

    """
    hey mycroft HH EY1 . M Y K R OW F T
    hey chatterbox HH EY1 . CH AE T EH R B OW K S
    alexa AH0 L EH1 K S AH0
    siri S IH1 R IY0
    cortana K OW R T AE N AE
    """