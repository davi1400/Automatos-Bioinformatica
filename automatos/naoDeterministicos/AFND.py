import networkx as nx
import matplotlib.pyplot as plt
from utils.utils import drawing_nodes_params


class automato:
    def __init__(self):
        """

        """
        self.graph = nx.DiGraph()
        self.states = []
        self.C = []
        self.alphabet = []
        self.initial_state = None
        self.final_states = []
        self.transition_table = {}

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
        self.alphabet = alphabet

    def is_state(self, state):
        return self.graph.has_node(state)

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)
            self.graph.add_node(state)
            self.graph.nodes[state].update({'color': {'r': 0, 'g': 0, 'b': 0}})

    def add_transition(self, original_state, destine_state, symbol):
        self.graph.add_edge(original_state, destine_state)
        if symbol in self.alphabet:
            if 'transition symbol' in self.graph.edges[original_state, destine_state]:
                self.graph.edges[original_state, destine_state]['transition symbol'].append(symbol)
            else:
                self.graph.edges[original_state, destine_state].update({'transition symbol': [symbol]})

            if original_state in self.transition_table.keys():
                if symbol in self.transition_table[original_state].keys():
                    self.transition_table[original_state][symbol].update({destine_state})
                else:
                    self.transition_table[original_state].update({
                        symbol: {destine_state}
                    })
            else:
                self.transition_table.update({
                    original_state: {
                        symbol: {destine_state}
                    }
                })

        else:
            print('this symbol is not in alphabet, add')


    def add_e_transition(self, original_state, destine_state):
        if not self.graph.has_edge(original_state, destine_state):
            self.graph.add_edge(original_state, destine_state)

        if 'transition symbol' in self.graph.edges[original_state, destine_state]:
            self.graph.edges[original_state, destine_state]['transition symbol'].append('E')
        else:
            self.graph.edges[original_state, destine_state].update({'transition symbol': ['E']})

    def next_state(self, current_states, symbol):

        delete_states = current_states.copy()

        for current_state in current_states.copy():
            transitions = dict(self.graph[current_state])
            for state in transitions:
                if symbol in transitions[state]['transition symbol'] or 'E' in transitions[state]['transition symbol']:
                    current_states.append(state)

        for state in delete_states:
            current_states.remove(state)

        return current_states

    def in_automato_language(self, string):
        N = string.__len__()
        current_states = [self.initial_state]

        for i in range(N):
            current_states = self.next_state(current_states, string[i])
            print(current_states)

        token = False
        for state in current_states:
            if state in self.final_states:
                token = True
                print('string accepted')

        if not token:
            print('string not accepted')

    def draw_automato(self):
        params = drawing_nodes_params(self.graph)
        print(params)
        plt.figure(figsize=(13, 7))
        nx.draw_networkx(**params)
        plt.show()


if __name__ == '__main__':
    import json

    # some testing
    a = automato()
    a.add_state('q0')
    a.add_state('q1')
    a.add_state('q2')

    a.add_initial_state('q0')
    a.final_state(['q2'])

    a.add_alphabet(['a', 'b'])

    a.add_transition('q0', 'q0', 'a')
    a.add_transition('q0', 'q0', 'b')
    a.add_transition('q0', 'q1', 'a')
    a.add_transition('q0', 'q2', 'E')

    a.add_transition('q1', 'q1', 'a')
    a.add_transition('q1', 'q1', 'b')
    a.add_transition('q1', 'q0', 'a')
    a.add_transition('q1', 'q2', 'b')

    a.add_transition('q2', 'q2', 'a')
    a.add_transition('q2', 'q1', 'b')

    print(str(a.transition_table))
