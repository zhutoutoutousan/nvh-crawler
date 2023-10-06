# Util Tutorial
import io
import os
import unicodedata
import string
import glob

import torch
import random

# ------------------------ Util
ALL_LETTERS = string.ascii_letters + ".,;"
N_LETTERS = len(ALL_LETTERS)

def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in ALL_LETTERS
    )

def load_data():
    category_lines = {}
    all_categories = []
    for filename in glob.glob('data/rnn/names/*.txt'):
        category = os.path.splitext(os.path.basename(filename))[0]
        all_categories.append(category)
        lines = io.open(filename, encoding='utf-8').read().strip().split('\n')
        category_lines[category] = [unicode_to_ascii(line) for line in lines]
    return category_lines, all_categories

def letter_to_index(letter):
    return ALL_LETTERS.find(letter)

def letter_to_tensor(letter):
    tensor = torch.zeros(1, N_LETTERS)
    tensor[0][letter_to_index(letter)] = 1
    return tensor

def line_to_tensor(line):
    tensor = torch.zeros(len(line), 1, N_LETTERS)
    for i, letter in enumerate(line):
        tensor[i][0][letter_to_index(letter)] = 1
    return tensor

def random_training_example(category_lines, all_categories):
    category = random.choice(all_categories)
    line = random.choice(category_lines[category])
    category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
    line_tensor = line_to_tensor(line)
    return category, line, category_tensor, line_tensor

if __name__ == '__main__':
    category_lines, all_categories = load_data()
    print(random_training_example(category_lines, all_categories))