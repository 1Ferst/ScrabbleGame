import bisect


def load_dictionary(filename='dictionary.txt'):
    with open(filename, 'r', encoding='utf-8') as file:
        word_list = sorted(word.strip().lower() for word in file)
    return word_list


polish_dictionary = load_dictionary()


def is_word_valid(word):
    index = bisect.bisect_left(polish_dictionary, word.lower()) #wyszukiwanie binarne,zlozonosc logarytmiczna,
    # dzielimy na pol liste, nasz slowo porownynawe jest z tym na srodku, a potem
    #algorytm decydje czy jest po prawej czy lewej, wybiera polowka itd.
    return index < len(polish_dictionary) and polish_dictionary[index] == word.lower()

