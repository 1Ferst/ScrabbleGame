def load_dictionary():
    with open('dictionary.txt', 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)

polish_dictionary = load_dictionary()

def is_word_valid(word):
    return word.lower() in polish_dictionary

