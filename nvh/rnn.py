import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from rnn_util import ALL_LETTERS, N_LETTERS
from rnn_util import load_data, letter_to_tensor, line_to_tensor, random_training_example

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.hidden_size = hidden_size
        # input to hidden
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        # input to output
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        # softmax
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input_tensor, hidden_tensor):
        combined = torch.cat((input_tensor, hidden_tensor), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)
    
category_lines, all_categories = load_data()
n_categories = len(all_categories)
print(n_categories)

n_hidden = 128
rnn = RNN(N_LETTERS, 128, n_categories)

# one step
input_tensor = letter_to_tensor('A')
hidden_tensor = rnn.init_hidden()

output, next_hidden = rnn(input_tensor, hidden_tensor)