from collections import defaultdict, Counter

def group_anagrams(words):
    anagram_dict = defaultdict(list)
    for word in words:
        sorted_word = ''.join(sorted(word.lower()))
        anagram_dict[sorted_word].append(word)
    return anagram_dict

def calculate_frequency(word_list):
    frequency = Counter()
    for word in word_list:
        frequency.update(word.lower())
    return frequency

def main(words):
    anagrams = group_anagrams(words)
    sorted_anagrams = sorted(anagrams.keys(), key=lambda x: words.index(anagrams[x][0]))
    anagram_dict = {word: anagrams[word] for word in sorted_anagrams}

    max_freq_word = None
    max_freq = Counter()

    for word_list in anagram_dict.values():
        freq = calculate_frequency(word_list)
        if sum(freq.values()) > sum(max_freq.values()):
            max_freq = freq
            max_freq_word = word_list[0]

    print(f"words = {sorted(words, key=lambda x: words.index(x))}")
    print(f"Anagram Dictionary = {anagram_dict}")
    print(f"Group with highest total frequency: {max_freq_word} - {max_freq}")

words = ["listen", "silent", "enlist", "inlets", "google", "goolge", "cat", "tac", "act"]
main(words)