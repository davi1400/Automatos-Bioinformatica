from unittest import TestCase
from automatos.naoDeterministicos.AFND import automato
from automatos.conversion.conversor import conversor


class Testconversor(TestCase):

    def test_convert_afnd_to_afd(self):
        """

        :return:
        """

        afnd = automato()
        afnd.add_alphabet(['0', '1'])
        afnd.add_all_states(['q1', 'q2', 'q3'])
        afnd.add_initial_state('q1')
        afnd.final_state(['q3'])

        afnd.add_transition('q1', 'q1', '0')
        afnd.add_transition('q1', 'q1', '1')

        afnd.add_transition('q1', 'q2', '0')
        afnd.add_transition('q2', 'q3', '1')

        afnd.add_transition('q3', 'q3', '0')
        afnd.add_transition('q3', 'q3', '1')


        self.assertEqual(['0', '1'], afnd.alphabet, "Alphabet ok")
        self.assertEqual(['q1', 'q2', 'q3'], afnd.states, "states ok")
        self.assertEqual('q1', afnd.initial_state, "initial state ok")
        self.assertEqual(['q3'], afnd.final_states, "final states ok")

        accepted_words = ["011", "101", "00101011", "11101"]
        not_accepted_words = ["1", "0000", "1111", "0"]


        for ac_w, n_w in zip(accepted_words, not_accepted_words):
            self.assertEqual(afnd.in_automato_language(ac_w), True, "in Language")
            self.assertEqual(afnd.in_automato_language(n_w), False, "in Language")


        conv = conversor()
        conv._to_deterministic(afnd)
        afd = conv.afd

        for ac_w, n_w in zip(accepted_words, not_accepted_words):
            self.assertEqual(afd.in_automato_language(ac_w), True, "in Language")
            self.assertEqual(afd.in_automato_language(n_w), False, "in Language")



