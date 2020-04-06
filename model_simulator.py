import numpy as np 


class Model_Simulator:
    def __init__(self, accuracy, nItem):
        self.accuracy = accuracy
        self.nItem = nItem

    def make_prediction(self, user):
        acc_tf = np.random.choice([0, 1], self.nItem, p=[1 - self.accuracy, self.accuracy])
        sign = np.random.choice([-1, 1], self.nItem)
        delta = np.random.standard_normal(self.nItem)
        score = []
        for i, s in enumerate(sign):
            if acc_tf:
                score.append(max([0.0, min([1.0, user.itemProb[i] + s * delta[i]/10])]))
            else:
                score.append(delta)

        return score