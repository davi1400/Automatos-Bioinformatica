import networkx as nx
from automatos.naoDeterministicos.AFND import automato
from automatos.conversion.conversor import conversor

__all__ = ['DAWG']


class dawg(automato):
    def __init__(self):
        super(dawg, self).__init__()
        self.root = 'Sroot'
        self.add_state('Sroot')
        self.add_initial_state('Sroot')
        self.set_state_attributes('Sroot', 'recheables', [])

        self.word = None
        self.__last_id = 1
        self.__prev_word = ''
        self.__prev_node = 'Sroot'
        self.__words_count = {}

    def __commom_prefixe_in_words(self, words):
        # Initialising string
        ini_strlist = words

        # Finding common prefix using Naive Approach
        res = ''
        prefix = ini_strlist[0]

        for string in ini_strlist[1:]:
            while string[:len(prefix)] != prefix and prefix:
                prefix = prefix[:len(prefix) - 1]
            if not prefix:
                break

        return prefix

    def __add(self, word):

        if word < self.__prev_word:
            raise ValueError("Words should be inserted in Alphabetical order"
                             "<Previous word - %s>, <Current word - %s>" % (self.__prev_word, word))

        elif word == self.__prev_word:
            if word not in self.__words_count.keys():
                self.__words_count.update({word: 1})
            else:
                self.__words_count[word] += 1

        else:
            common_prefix_index = 0
            for i, letters in enumerate(zip(word, self.__prev_word), start=1):
                if letters[0] != letters[1]:
                    break
                common_prefix_index = i

            state = 'S' + word[:common_prefix_index].lower()
            if state != 'S':
                self.__prev_node = state
            elif state == 'S':
                self.__prev_node = 'Sroot'

            for letter in word[common_prefix_index:]:
                state += letter.lower()
                if letter not in self.alphabet:
                    self.add_alphabet(letter)
                self.add_transition(self.__prev_node, state, letter)
                self.__prev_node = state

            self.final_states.append(self.__prev_node)
            self.__prev_word = word

    def __terminal(self):
        self.add_alphabet('+')
        for final_state in self.final_states:
            self.add_transition(final_state, 'Sterminal', '+')

        self.final_states = ['Sterminal']

    def __negative_in_language(self, words):
        for word in words:
            word += '+'
            if self.in_automato_language(word):
                return True
        return False

    def __extend(self, words):
        # sort the edges acording to decrease potencies
        all_edges = list(self.graph.edges())
        potencies = []
        for e in all_edges:
            p = self.__potencie(e[0], e[1])
            potencies.append((e[0], e[1], p))

        potencies = sorted(potencies, key=lambda x: x[2], reverse=False)

        for u, v, p in potencies:
            for a in self.alphabet:
                if a != '+':
                    symbol = self.graph.edges[u, v]['transition symbol']
                    if a.upper() not in symbol:
                        self.graph.edges[u, v]['transition symbol'].append(a)
                        if self.__negative_in_language(words):
                            self.graph.edges[u, v]['transition symbol'].remove(a)
                        else:
                            print('added')

    def has_prefixe(self, word):
        pass

    def get_previus_word(self):
        return self.__prev_word

    def get_previus_node(self):
        return self.__prev_node

    def create(self, plus_words, negative_words):
        if isinstance(plus_words, list) and isinstance(negative_words, list):
            plus_words = sorted(plus_words)
            for word in plus_words:
                self.__add(word)

            self.__terminal()
            self.__extend(negative_words)
        else:
            print("Only accpty list type")

    def __potencie(self, source, target):
        len_paths = 0
        if target == 'Sterminal':
            return 1
        for _ in nx.all_simple_paths(self.graph, source=target, target='Sterminal'):
            len_paths += 1

        return len_paths


if __name__ == '__main__':
    import pandas as pd
    from utils.utils import get_project_root

    path = get_project_root() + '/Automatos-Bioinformatica/datasets/' + 'waltz.txt'
    words = pd.read_csv(path, header=None)

    plus_words = []
    negative_words = []
    for i in range(len(words)):
        if '\t+' in words.iloc[i][0]:
            w = words.iloc[i][0]
            plus_words.append(w[:len(w) - len('\t+')])
        else:
            negative_words.append(words.iloc[i][0])

    dawg_alg = dawg()
    dawg_alg.create(plus_words, negative_words)

    # ------------------------------------------------------------------------------------------------------------------
    # internal test
    # plus_words = sorted(plus_words)
    # print("internal test")
    # count = 0
    # for word in plus_words:
    #     word += '+'
    #     if dawg_alg.in_automato_language(word):
    #         count += 1
    #
    # print("count positive")
    # print(count, len(plus_words))
    #
    # # internal test
    # negative_words = sorted(negative_words)
    # print("internal test")
    #
    # count = 0
    # for word in negative_words:
    #     word += '+'
    #     if dawg_alg.in_automato_language(word):
    #         count += 1
    #
    # print("count negative")
    # print(count, len(negative_words))
    #
    # # -----------------------------------------------------------------------------------------------------------------
    #
    # # output test
    # path = get_project_root() + '/Automatos-Bioinformatica/datasets/' + 'waltzdb.csv'
    # df = pd.read_csv(path)
    # target = 'amyloid'
    # N, M = df.shape
    #
    # expected_number_target = len(df[df['Classification'] == target])
    # expected_number_non_target = N - expected_number_target
    # result = {
    #     'amyloid': 0,
    #     'non-amyloid': 0
    # }
    # for i in range(N):
    #     seguence = df.iloc[i]['Sequence']
    #     c = df.iloc[i]['Classification']
    #
    #     seguence += '+'
    #     token = dawg_alg.in_automato_language(seguence)
    #     if token:
    #         if c == target:
    #             result[target] += 1
    #     elif not token:
    #         if c != target:
    #             result['non-amyloid'] += 1
    #
    # print(result)
    # print(expected_number_target)
    # print(expected_number_non_target)

    # ------------------------------------------------------------------------------------------------------------------

    conv = conversor()
    conv._to_deterministic(dawg_alg)
    dawg_alg_afd = conv.afd
