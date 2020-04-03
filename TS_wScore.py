import numpy as np
import scipy as sp
import pickle
from scipy.stats import beta
from MABTest.MAB import MAB

class TS_wScore(MAB):
	def __init__(self, itemid, posProb, nModel=1):
		super().__init__(itemid, posProb)
		self.S = [0 for _ in range(self.K)]
		self.N = [0 for _ in range(self.K)]
		if nModel > 1:
			self.M = [0 for _ in range(nModel)]
		else:
			self.M = 0

	#return sorted list of item numbers using predicted item preference list(item score), with length require_num
	def select_items(self, required_num, item_score):
		self.turn += 1
		sample_val = [0.0] * self.K
		for k in range(self.K):
			sample_val[k] = np.random.beta(self.S[k] + 1, self.N[k] - self.S[k] + 1) * item_score[k]
		items = sorted([(sample_val[k], k) for k in range(self.K)], reverse=True)
		result = [items[i][1] for i in range(required_num)]
		return result

	def update(self, selected_items, feedback, ith_model=-1):
		assert len(selected_items) == len(feedback)
		for l in range(len(selected_items)):
			k = selected_items[l]
			self.N[k] += 1
			if feedback[l]:
				self.S[k] += 1
				if type(self.M) == list and ith_model > -1:
					self.M[ith_model] += 1