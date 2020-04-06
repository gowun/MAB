import numpy as np 


class Model_Simulator:
    def __init__(self, accuracy, nItem):
        self.accuracy = accuracy
        self.nItem = nItem

    def make_prediction(self, user):
        acc_tf = np.random.choice([0, 1], self.nItem, p=[1 - self.accuracy, self.accuracy])
        rand_score = np.random.standard_normal(self.nItem) 
        rand_score = rand_score + acc_tf * np.array(user.itemProb)
        score = (rand_score - min(rand_score)) / (max(rand_score) - min(rand_score))

        return score