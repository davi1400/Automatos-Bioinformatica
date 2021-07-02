from itertools import combinations
from automatos.deterministicos.AFD import deterministic_automato


class conversor:
    def __init__(self):
        self.afd = deterministic_automato()
        self.afnd = None
        self.transtion_table_afnd = None
        self.transtion_table_afd = {}

    def create_alphabet(self, automata):
        self.afd.add_alphabet(automata.alphabet)

    def create_states(self):
        code = 'S'
        final_states = []
        for i in range(len(self.transtion_table_afd.keys())):
            self.afd.add_state(code + str(i))
            self.afd.set_state_attributes(code + str(i), 'old_name_state', list(self.transtion_table_afd.keys())[i])

            # verify if is the initial state
            if len(list(self.transtion_table_afd.keys())[i]) == 1 and list(self.transtion_table_afd.keys())[i][0] == self.afnd.initial_state:
                self.afd.add_initial_state(code + str(i))

            #
            if len(set(list(self.transtion_table_afd.keys())[i]).intersection(self.afnd.final_states)) > 0:
                final_states.append(code + str(i))

        self.afd.final_states(final_states)

    def create_transitions(self):
        pass

    def create_deterministic_automata(self):
        self.create_states()

    def is_reacheble(self, state, reachebles):
        """

        :param state:
        :param reachebles:
        :return:
        """
        if state in reachebles:
            return True
        else:
            return False

    def is_loop(self, state):
        """

        :param state:
        :return:
        """
        loop = True
        initial_verification = self.transtion_table_afd[state][self.afnd.alphabet[0]]

        for i in range(1, len(self.afnd.alphabet)):
            if self.afnd.alphabet[i] in self.transtion_table_afd[state].keys():
                if self.transtion_table_afd[state][self.afnd.alphabet[i]] != initial_verification:
                    loop = False

                initial_verification = self.transtion_table_afd[state][self.afnd.alphabet[i]]

        return loop

    def delete_nodes(self):

        reachebles = []
        for tuple_states in self.transtion_table_afd.keys():
            for symbol in self.transtion_table_afd[tuple_states].keys():
                reachebles.append(self.transtion_table_afd[tuple_states][symbol])

        copy_of_transtion_table_afd = self.transtion_table_afd.copy()
        for tuple_states in copy_of_transtion_table_afd.keys():
            reacheble = self.is_reacheble(reachebles, tuple_states)
            loop = self.is_loop(tuple_states)

            if not reacheble and loop:
                del self.transtion_table_afd[tuple_states]

    def _to_deterministic(self, automata):
        self.afnd = automata
        self.transtion_table_afnd = automata.transition_table

        for i in range(1, len(self.afnd.states)+1):
            comb = combinations(self.afnd.states, i)

            for tuple_state in list(comb):

                if tuple_state not in self.transtion_table_afd.keys():
                    self.transtion_table_afd.update({
                        tuple_state: {}
                    })

        for tuple_states in self.transtion_table_afd.keys():
            for state in tuple_states:
                for symbol in self.afnd.alphabet:
                    # print(self.transtion_table_afd)
                    if symbol not in self.transtion_table_afnd[state].keys():
                        break
                    else:
                        possible_state = self.transtion_table_afnd[state][symbol].copy()
                    if symbol not in self.transtion_table_afd[tuple_states].keys():
                        self.transtion_table_afd[tuple_states].update({
                            symbol: possible_state
                        })
                    else:
                        self.transtion_table_afd[tuple_states][symbol].update(possible_state)

        # Creating the AFD
        self.create_alphabet(automata)

        # deleting the not rechable states and the states that dont have any output to other state
        self.delete_nodes()

        # Creating the states
        self.create_deterministic_automata()


if __name__ == '__main__':
    import networkx as nx
    from automatos.naoDeterministicos.AFND import automato

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
    a.add_transition('q1', 'q2', 'a')
    a.add_transition('q2', 'q2', 'b')
    a.add_transition('q2', 'q2', 'a')

    print(str(a.transition_table))

    from itertools import combinations, permutations
    combinacoes = combinations(['q0', 'q1', 'q2'], 2)
    print(list(combinacoes))

    c = conversor()
    c._to_deterministic(a)
