import numpy as np
import scipy as sp
import pickle
from scipy.stats import beta
from MABTest.MAB import MAB

class BayesUCB_wScore(MAB):
	def __init__(self, itemid, posProb, nModel=1):
		super().__init__(itemid, posProb)
		self.S = [[1 for _ in range(self.L)] for __ in range(self.K)]
		self.N = [[2 for _ in range(self.L)] for __ in range(self.K)]
		if nModel > 1:
			self.M = [0 for _ in range(nModel)]
		else:
			self.M = 0
	
	#return sorted list of item numbers using predicted item preference list(item score), with length require_num
	def select_items(self, required_num, item_score):
		self.turn += 1
		sample_val = [0.0] * self.K
		for k in range(self.K):
			z0 = beta.ppf(1.0 - 1.0 / self.turn, sum(self.S[k]), sum(self.N[k]) - sum(self.S[k]))
			sample_val[k] = z0 * item_score[k]
		items = sorted([(sample_val[k], k) for k in range(self.K)], reverse=True)
		result = [items[i][1] for i in range(required_num)]
		return result

	def update(self, selected_items, feedback, ith_model=-1):
		assert len(selected_items) == len(feedback)
		for l in range(len(selected_items)):
			k = selected_items[l]
			self.N[k][l] += 1
			if feedback[l]:
				self.S[k][l] += 1
                if type(self.M) == list and ith_model > -1:
					self.M[ith_model] += 1