
import os
import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

from DAWG.DAWG import dawg
from utils.utils import get_project_root
from automatos.conversion.conversor import conversor
from sklearn.metrics import *


if __name__ == '__main__':
    train_path = get_project_root() + '/Automatos-Bioinformatica/datasets/' + 'waltz.txt'
    train = pd.read_csv(train_path, header=None)

    test_path = get_project_root() + '/Automatos-Bioinformatica/datasets/' + 'waltzdb.csv'
    test = pd.read_csv(test_path)

    plus_words = []
    negative_words = []
    for i in range(len(train)):
        if '\t+' in train.iloc[i][0]:
            w = train.iloc[i][0]
            plus_words.append(w[:len(w) - len('\t+')])
        else:
            negative_words.append(train.iloc[i][0])

    print("Treino")
    dawg_alg = dawg()
    dawg_alg.create(plus_words, negative_words)


    target = 'amyloid'
    N, M = test.shape
    mean_time = 0

    expected_number_target = len(test[test['Classification'] == target])
    expected_number_non_target = N - expected_number_target
    result = {
        'amyloid': 0,
        'non-amyloid': 0
    }
    y_out = []
    for i in range(N):
        seguence = test.iloc[i]['Sequence']
        c = test.iloc[i]['Classification']

        seguence += '+'
        begin = datetime.datetime.now()
        token = dawg_alg.in_automato_language(seguence)
        finish = datetime.datetime.now()

        mean_time += (finish - begin).microseconds
        if token:
            if c == target:
                result[target] += 1
            y_out.append(target)
        elif not token:
            if c != target:
                result['non-amyloid'] += 1
            y_out.append('non-amyloid')
    print(result)
    print(expected_number_target)
    print(expected_number_non_target)
    print("mean Time per string in afnd: ", mean_time / N)

    y_test = test['Classification'].to_numpy()

    y_out = np.array(y_out)
    print('ACC:', str(accuracy_score(y_out, y_test)))
    print('R:', str(recall_score(y_out, y_test, average='binary', pos_label="amyloid")))
    print('P:', str(precision_score(y_out, y_test, average='binary', pos_label="amyloid")))
    print('AUC: ')