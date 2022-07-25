# Import libraries
from typing import List
import numpy as np
import random as rd
import os
import torch
import torch.cuda
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

class NeuralNetwork(nn.Module):
    def __init__(self, input_size:int, nb_actions:int) -> None:
        super(NeuralNetwork, self).__init__()
        self.input_size:int = input_size
        self.nb_actions:int = nb_actions
        self.fc1 = nn.Linear(in_features=input_size, out_features=input_size*4)
        self.fc2 = nn.Linear(in_features=input_size*4, out_features=input_size*8)
        #self.fc3 = nn.Linear(in_features=input_size*2, out_features=input_size*2) # First hidden layer
        self.fc3 = nn.Linear(in_features=input_size*8, out_features=nb_actions) # Second hidden layer
    
    def forward(self, state:List[int]):
        """It is the forward propagation of the neural network

        Args:
            state (List[int]): it is the input layer it contain the state of the agent

        Returns:
            _type_: it return the q_values
        """
        x = F.relu(self.fc1(state))
        x2 = F.relu(self.fc2(x))
        #x3 = F.relu(self.fc3(x2))
        q_values = self.fc3(x2)
        return q_values

class ReplayMemory(object):
    def __init__(self, capacity:int) -> None:
        self.capacity:int = capacity
        self.memory:list = []
    
    def push(self, event) -> None:
        """push event to memory"""
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]
    
    def sample(self, batch_size) -> map:
        """Random choose sample in memory

        Args:
            batch_size (int): size of batch

        Returns:
            map: organize map of samples
        """
        samples = zip(*rd.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)

class Dqn():
    def __init__(self, input_size:int, nb_action:int, gamma:float) -> None:
        self.input_size = input_size
        self.model = NeuralNetwork(input_size, nb_action)
        self.gamma:float = gamma
        self.reward_window:list = []
        self.memory = ReplayMemory(100000)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.003)
        self.last_action:int= 0
        self.last_reward:int = 0
    
    def select_action(self, state):
        """select an action

        Args:
            state (_type_): state of the agent

        Returns:
            _type_: action
        """
        T = 80
        probs = F.softmax(self.model(state) * T, dim=1)
        action = probs.multinomial(num_samples=1)
        return action.data[0, 0]
    
    def learn(self, batch_state, batch_next_state, batch_reward, batch_action) -> None:
        """train the IA

        Args:
            batch_state (_type_): _description_
            batch_next_state (_type_): _description_
            batch_reward (_type_): _description_
            batch_action (_type_): _description_
        """
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        targets = batch_reward + self.gamma * next_outputs
        td_loss = F.smooth_l1_loss(outputs, targets)
        self.optimizer.zero_grad()
        td_loss.backward()
        self.optimizer.step()
    
    def update(self, reward, new_signal) -> int:
        new_state = torch.Tensor(new_signal).float().unsqueeze(0)
        self.memory.push((
                self.last_state,
                new_state,
                torch.LongTensor([int(self.last_action)]),
                torch.Tensor([self.last_reward])
            )
        )
        action = self.select_action(new_state)
        if len(self.memory.memory) > 100:
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(100)
            self.learn(batch_state, batch_next_state, batch_reward, batch_action)
        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.reward_window.append(reward)
        if len(self.reward_window) > 1000:
            del self.reward_window[0]
        return action

    def score(self) -> float:
        """return the score

        Returns:
            float: score
        """
        return sum(self.reward_window) / (len(self.reward_window) + 1.0)
    
    def save(self):
        torch.save({
            "state_dict": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict()}, f"last_brain_inputs:{self.input_size}.pth")
    
    def load(self):
        if os.path.isfile("last_brain.pth"):
            print("=> loading checkpoint...")
            checkpoint = torch.load(f"last_brain_inputs:{self.input_size}.pth")
            self.model.load_state_dict(checkpoint["state_dict"])
            self.optimizer.load_state_dict(checkpoint["optimizer"])
            print("done !")
        else:
            print("checkpoint not found...")
