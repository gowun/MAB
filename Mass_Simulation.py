import numpy as np
from pydoc import locate

from MABTest.model_simulator import Model_Simulator

class Mass_Simulation:
    def __init__(self, massMab, userList, lenSimulation, nSimulation=1, modelAccs=[]):
        self.massMab = massMab
        self.users = userList
        self.lenSim = lenSimulation
        self.nSim = nSimulation
        if len(modelAccs) > 0:
            self.predModels = [Model_Simulator(acc, self.massMab.mab.K) for acc in modelAccs]
        else:
            self.predModels = None

    def compute_rec_item_distribution(self, items):
        dist = [0] * self.massMab.mab.K
        for it in items:
            for i in it:
                dist[i] += 1
        return dist

    def compute_regrets(self, users, items, feedbacks):
        if len(users) > 0:
            return sum(map(lambda x: sum(np.array(x[0].posProb) * np.array(list(map(lambda y: x[0].itemProb[y], x[1])))) - sum(x[2]), zip(users, items, feedbacks)))
        else:
            return 0


    def one_step(self, ui_score_matrix_per_model=[]):
        rec = self.massMab.recommend_items_batch(ui_score_matrix_per_model)
        if len(rec) == 2:
            items = rec[0]
            models = rec[1]
        else:
            items = rec
            models = []
        feedbacks = [u.react(items[i]) for i, u in enumerate(self.users)]
        self.massMab.update_batch(items, feedbacks, models)

        if self.massMab.nModel > 1:
            rec_item_dist_per_model = []
            regrets_per_model = []
            for i in range(self.massMab.nModel):
                i_users, i_items, i_feedbacks = [], [], []
                for j in range(len(self.users)):
                    if i == models[j]:
                        i_users.append(self.users[j])
                        i_items.append(items[j])
                        i_feedbacks.append(feedbacks[j])
                rec_item_dist_per_model.append(self.compute_rec_item_distribution(i_items))
                regrets_per_model.append(self.compute_regrets(i_users, i_items, i_feedbacks))
            return rec_item_dist_per_model, regrets_per_model, self.massMab.mab.M
        else:
            return self.compute_rec_item_distribution(items), self.compute_regrets(self.users, items, feedbacks), []

    def single_simulation(self):
        rec_item_dist = []
        regrets = []
        hist_M = []

        for i in range(self.lenSim):
            ui_score_matrix_per_model = []
            if self.predModels is not None:
                for pm in self.predModels:
                    tmp = list(map(lambda x: pm.make_prediction(x), self.users))
                    ui_score_matrix_per_model.append(tmp)
                if len(ui_score_matrix_per_model) == 1:
                    ui_score_matrix_per_model = ui_score_matrix_per_model[0]
            dist, reg, mm = self.one_step(ui_score_matrix_per_model)
            if self.predModels is not None and len(self.predModels) > 1:
                if i == 0:
                    rec_item_dist = [[d] for d in dist]
                    regrets = [[r] for r in reg]
                    hist_M = [[m] for m in mm]
                else:
                    for j, d in enumerate(dist):
                        rec_item_dist[j].append(d)
                        regrets[j].append(reg[j])
                        hist_M[j].append(mm[j])
            else:
                rec_item_dist.append(dist)
                regrets.append(reg)
        
        if self.predModels is not None and len(self.predModels) > 1:
            cum_regrets = np.cumsum(np.sum(regrets, axis=0))
        else:
            cum_regrets = np.cumsum(regrets)
        #print(hist_M)
        return rec_item_dist, regrets, cum_regrets, hist_M

    def mean_simulation(self):
        list_rec_item_dist = []
        list_regrets = []
        list_cum_regrets = []
        list_hist_M = []

        for i in range(self.nSim):
            tmp = self.single_simulation()
            list_rec_item_dist.append(tmp[0])
            if self.predModels is not None and len(self.predModels) > 1:
                if i == 0:
                    list_regrets = [[l] for l in tmp[1]]
                    list_hist_M = [[m] for m in tmp[3]]
                else:
                    for j, l in enumerate(tmp[1]):
                        list_regrets[j].append(l)
                        list_hist_M[j].append(tmp[3][j])
            else:
                list_regrets.append(tmp[1])
            list_cum_regrets.append(tmp[2])
        
        if self.predModels is not None and len(self.predModels) > 1:
            mean_regrets = [np.mean(r, axis=0) for r in list_regrets]
            mean_hist_M = [np.mean(m, axis=0) for m in list_hist_M]
        else:
            mean_regrets = np.mean(list_regrets, axis=0)
            mean_hist_M = []
        mean_cum_regrets = np.mean(list_cum_regrets, axis=0)

        return mean_regrets, mean_cum_regrets, mean_hist_M, list_rec_item_dist