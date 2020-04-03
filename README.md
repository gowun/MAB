# Dynamic/Reactive AB Test 


## Multi-Armed Bandit(MAB) Algorithm

MAB 자체도 실시간 추천 알고리즘이고 오리지널 패키지 내에 구현된 알고리즘은 랜덤선택(Random), Thomson Sampling(TS), Upper Confidence Bound(UCB1), UCB1-tuned(UCBtune), Bayesian UCB(BayesUCB)가 있다. (자세한 알고리즘 설명은 http://wwiiiii.tistory.com/15)


## MAB 공통 클래스 변수 의미

* K: 가능한 아이템 개수

* L: 가능한 포지션 개수 (노출 아이템 개수)

* posProb: posProb[i]는 i번째 포지션을 유저가 관측할 확률, 가능한 인덱스는 [0, L-1]

* itemProb: itmeProb[i]는 i번째 아이템이 관측됐을 때 유저가 클릭할 확률, 가능한 인덱스는 [0, K-1]

* S: 크기 K의 1차원 배열 또는 K*L의 2차원 배열, S[k][l]은 k번째 아이템이 l번째 위치에 노출된 후 유저에게 클릭된 횟수

* N: 크기 K의 1차원 배열 또는 K*L의 2차원 배열, N[k][l]은 k번째 아이템이 l번째 위치에 노출시킨 횟수


## 클래스 구성

* MAB, TS, UCB1, UCBtune, BayesUCB 는 오리지널 패키지의 클래스 (README_org.md 참고)

* ***_wScore 클래스는 user 별 아이템 선호도를 예측한 스코어를 합성하여 추천할 수 있게 변형한 클래스

* ***.ipynb 는 각종 실험용 노트북



## Dyanmic and Reactive AB Test 실험

* MAB_Simulation.ipynb: 1명의 유저에게 총 5가지 MAB 알고리즘으로 아이템 1개를 추천했을 시 시간의 흐름에 따른 누적 regret 시뮬레이션

* BayesUCB_comparison1.ipynb: 10명의 유저에게 Bayesian UCB 기반으로 5개 아이템 중 2개 추천 시, 시간의 흐름에 따른 10명의 regret 총합의 변화(누적 regret) 시뮬레이션: comparison of without and with predited item scores 

* BayesUCB_comparison2.ipynb: 10명의 유저에게 Bayesian UCB 기반으로 8개 아이템 중 4개 추천 시, 시간의 흐름에 따른 10명의 regret 총합의 변화(누적 regret)시뮬레이션
