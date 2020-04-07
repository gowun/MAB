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

* (---_wScore 변수만) M: user-item score를 계산해 주는 모델 갯수만의 1차원 배열, M[i]는 i번째 모델이 추천한 아이템이 유저에게 클릭된 횟수 



## Mass_MAB 클래스 변수 의미

* nUser: 전체 사용자수, 배치추천수

* mabName: 사용할 MAB 알고리즘명

* nModel: (사용한다면) item score prediction model 개수


## Model_Simulator 클래스 변수 의미

* accuracy: 희망하는 모델의 정확도

* nItem: 아이템수 



## Mass_Simulation 클래스 변수 의미

* massMab: Mass_MAB 오브젝트

* userList: 전체 User 오브젝트 리스트

* lenSimulation: 시뮬레이션 길이

* nSimulation: 시뮬레이션을 행할 수

* modelAccs: item score prediction model의 정확도 성능 리스트


## 클래스 구성

* MAB, TS, UCB1, UCBtune, BayesUCB 는 오리지널 패키지의 클래스 (README_org.md 참고)

* ---_wScore, Mass_---, model_simulator, utils 클래스/패키지는 user 별 아이템 선호도를 예측한 스코어를 합성하여 추천할 수 있게 변형한 것

* ---.ipynb 는 각종 실험용 노트북



## Dyanmic and Reactive AB Test 실험

* MAB_Simulation.ipynb: 1명의 사용자에게 총 5가지 MAB 알고리즘으로 아이템 1개를 추천했을 시 시간의 흐름에 따른 누적 regret 시뮬레이션

* MAB_w/wt_comparison.ipynb: 100명의 사용자, 5개의 아이템 중 2개씩 추천하여 각 케이스 별 시간의 흐름에 따른 누적 regret 시뮬레이션(길이 12의 시뮬레이션, 50번 평균)

    1. 오직 각 mab 알고리즘만 적용했을 경우
    2. 각 mab 알고리즘 + 하나의 item score prediction model만 적용했을 경우
    3. 각 mab 알고리즘 + 두개의 item score prediction models를 적용하여 모델 경쟁을 하게 한 경우

