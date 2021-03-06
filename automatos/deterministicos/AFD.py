import networkx as nx
import matplotlib.pyplot as plt
from utils.utils import drawing_nodes_params


class deterministic_automato:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.states = []
        self.alphabet = []
        self.initial_state = None
        self.final_states = []

    def add_initial_state(self, state):
        self.initial_state = state
        self.add_state(state)
        self.graph.nodes[state].update({'initial state': True})
        self.graph.nodes[state]['color'] = {'r': 247, 'g': 41, 'b': 41}

    def final_state(self, states):
        for state in states:
            if self.is_state(state) and (state not in self.final_states):
                self.final_states.append(state)
                self.graph.nodes[state].update({'final state': True})
                self.graph.nodes[state]['color'] = {'r': 41, 'g': 247, 'b': 96}

    def add_alphabet(self, alphabet):
        if isinstance(alphabet, list):
            self.alphabet = alphabet
        elif isinstance(alphabet, (str, int, float)):
            self.alphabet.append(alphabet)


    def is_state(self, state):
        return self.graph.has_node(state)

    def set_state_attributes(self, state, attribute_name, value):
        """

        :param state:
        :param attribute_name:
        :param value:
        :return:
        """
        print(self.graph.nodes)
        self.graph.nodes[state].update({attribute_name: value})

    def add_all_states(self, states):
        for state in states:
            self.add_state(state)

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)
            self.graph.add_node(state)
            self.graph.nodes[state].update({'color': {'r': 0, 'g': 0, 'b': 0}})

    def add_transition(self, original_state, destine_state, symbol):
        self.graph.add_edge(original_state, destine_state)
        used_symbols = []
        for state in self.graph[original_state].keys():
            if 'transition symbol' in self.graph[original_state][state].keys():
                used_symbols.append(self.graph[original_state][state]['transition symbol'])

        if used_symbols == self.alphabet:
            print("all transtitions used")
            raise Exception

        if symbol in self.alphabet:
            if 'transition symbol' in list(self.graph.edges[original_state, destine_state].keys()):
                self.graph.edges[original_state, destine_state]['transition symbol'].append(symbol)
            else:
                self.graph.edges[original_state, destine_state].update({'transition symbol': [symbol]})
        else:
            print('this symbol is not in alphabet, add')

    def next_state(self, current_state, symbol):

        transitions = dict(self.graph[current_state])
        for state in transitions:
            if isinstance(transitions[state]['transition symbol'], list):
                aux = transitions[state]['transition symbol'][0]
            else:
                aux = transitions[state]['transition symbol']
            if aux == symbol:
                current_state = state

        return current_state

    def is_deterministic(self):
        """
        Verifica se o automato ?? deterministico
        :return:
        """
        is_deterministic = True
        for node in self.graph.nodes:
            transitions_symbols_for_state = []

            transitions = dict(self.graph[node])
            for state in transitions:
                if transitions[state]['transition symbol'] not in transitions_symbols_for_state:
                    if isinstance(transitions[state]['transition symbol'], list):
                        transitions_symbols_for_state.append(transitions[state]['transition symbol'][0])
                    else:
                        transitions_symbols_for_state.append(transitions[state]['transition symbol'])

            if set(transitions_symbols_for_state) != set(self.alphabet):
                is_deterministic = False
                return is_deterministic

        return is_deterministic

    def in_automato_language(self, string):
        N = string.__len__()
        current_state = self.initial_state

        if not self.is_deterministic():
            print("this is not a deterministic automata")
            return

        for i in range(N):
            current_state = self.next_state(current_state, string[i])


        if current_state in self.final_states:
            # print('string accepted')
            return True
        else:
            # print('string not accepted')
            return False

    def draw_automato(self):
        params = drawing_nodes_params(self.graph)
        print(params)
        plt.figure(figsize=(13, 7))
        nx.draw_networkx(**params)
        plt.show()


if __name__ == '__main__':
    # some testing
    a = automato()
    a.add_state('q0')
    a.add_state('q1')
    a.add_transition('q0', 'q1', '1')
    print(a.graph.edges)
