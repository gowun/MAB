import numpy as np 


class Model_Simulator:
    def __init__(self, accuracy, nItem):
        self.accuracy = accuracy
        self.nItem = nItem

    def make_prediction(self, user):
        acc_tf = np.random.choice([0, 1], self.nItem, p=[1 - self.accuracy, self.accuracy])
        delta = np.random.standard_normal(self.nItem)
        score = []
        for i, d in enumerate(delta):
            if acc_tf[i]:
                tmp = user.itemProb[i] + d/10
            else:
                tmp = d
            score.append(max([0.0, min([1.0, tmp])]))

        return score