import numpy as np
from pydoc import locate

class Mass_MAB():
    def __init__(self, nUser, itemid, posProb, mabName, nModel):
        self.massSize = nUser
        mab = locate(".".join(["MABTest", mabName, mabName]))
        self.mab = mab(itemid, posProb)
        self.nModel = nModel

    def recommend_items_batch(self, ui_score_matrix_per_model=[]):
        batch_items = []
        if self.nModel > 1:
            if sum(self.mab.M) == 0:
                pp = [1/self.nModel] * self.nModel
            else:
                pp = np.array(self.mab.M) / sum(self.mab.M)
            model_lst = np.random.choice(range(self.nModel), self.massSize, p=pp)

        for i in range(self.massSize):
            if self.nModel == 0:
                batch_items.append(self.mab.select_items(self.mab.L))
            elif self.nModel == 1:
                batch_items.append(self.mab.select_items(self.mab.L, ui_score_matrix_per_model[i]))
            elif self.nModel > 1:
                batch_items.append(self.mab.select_items(self.mab.L, ui_score_matrix_per_model[model_lst[i]][i]))

        if self.nModel > 1:
            return batch_items, model_lst
        else:
            return batch_items


    def update_batch(self, batch_items, batch_clicked, batch_models=[]):
        for i in range(len(batch_items)):
            if self.nModel == 0:
                self.mab.update(batch_items[i], batch_clicked[i])
            else:
                self.mab.update(batch_items[i], batch_clicked[i], batch_models[i])