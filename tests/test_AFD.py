from unittest import TestCase
from automatos.deterministicos.AFD import deterministic_automato


class Testdeterministic_automato(TestCase):

    def test_create_automata(self):
        """

        :return:
        """

        afd = deterministic_automato()
        afd.add_alphabet(['0', '1'])
        afd.add_all_states(['q0', 'q1'])
        afd.add_initial_state('q0')
        afd.final_state(['q0'])

        afd.add_transition('q0', 'q1', '1')
        afd.add_transition('q1', 'q0', '1')

        afd.add_transition('q0', 'q0', '0')
        afd.add_transition('q1', 'q1', '0')

        self.assertEqual(['0', '1'], afd.alphabet, "Alphabet ok")
        self.assertEqual(['q0', 'q1'], afd.states, "states ok")
        self.assertEqual('q0', afd.initial_state, "initial state ok")
        self.assertEqual(['q0'], afd.final_states, "final states ok")
        self.assertListEqual([('q0', 'q1'), ('q0', 'q0'), ('q1', 'q0'), ('q1', 'q1')], list(afd.graph.edges), "transitions  ok")

    def test_case_1(self):
        """
        Linguagem onde so existem um numero par de 1's
        :return:
        """

        afd = deterministic_automato()
        afd.add_alphabet(['0', '1'])
        afd.add_all_states(['q0', 'q1'])
        afd.add_initial_state('q0')
        afd.final_state(['q0'])

        afd.add_transition('q0', 'q1', '1')
        afd.add_transition('q1', 'q0', '1')

        afd.add_transition('q0', 'q0', '0')
        afd.add_transition('q1', 'q1', '0')

        accepted_words = ["011", "101", "00101011", "1111"]
        not_accepted_words = ["1", "0001", "1011", "010101"]


        for ac_w, n_w in zip(accepted_words, not_accepted_words):
            self.assertEqual(afd.in_automato_language(ac_w), True, "in Language")
            self.assertEqual(afd.in_automato_language(n_w), False, "in Language")

    def test_case_02(self):
        """
        L ={w| w tem um numero impar de 0's}
        :return:
        """

        afd = deterministic_automato()
        afd.add_alphabet(['0', '1'])
        afd.add_all_states(['q1', 'q2', 'q3'])
        afd.add_initial_state('q1')
        afd.final_state(['q2'])

        afd.add_transition('q1', 'q2', '0')
        afd.add_transition('q1', 'q1', '1')

        afd.add_transition('q2', 'q3', '0')
        afd.add_transition('q2', 'q2', '1')

        afd.add_transition('q3', 'q2', '0')
        afd.add_transition('q3', 'q3', '1')

        accepted_words = ["011", "101", "001010011", "11101"]
        not_accepted_words = ["100", "001", "10011", "0101010"]

        for ac_w, n_w in zip(accepted_words, not_accepted_words):
            self.assertEqual(afd.in_automato_language(ac_w), True, "in Language")
            self.assertEqual(afd.in_automato_language(n_w), False, "in Language")