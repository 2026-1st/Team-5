# Team 5 - KNHANES 2022 PHQ8 기준 우울 위험군 선별 가능성 분석

## 프로젝트 개요

본 저장소는 **국민건강영양조사(KNHANES) 제9기 1차년도 2022년 자료**를 활용하여 수면시간, 청각 문제, 소음 노출 관련 자기보고 지표와 PHQ8 기준 우울 위험군 사이의 관계를 분석하고, 해당 지표들이 위험군 선별에 제공하는 정보를 탐색하는 머신러닝 팀 프로젝트입니다.

본 프로젝트의 목적은 우울증 확정 진단 모델을 개발하는 것이 아닙니다. PHQ-9/PHQ8은 자가보고식 우울 증상 선별도구이며, 본 연구에서는 수면시간 입력 변수와 타깃 간의 개념적 중복을 줄이기 위해 PHQ-9의 수면 문항을 제외한 PHQ8 기준 우울 위험군을 사용했습니다. 따라서 모델 출력은 의학적 진단이 아니라 추가 평가가 필요한 위험군을 넓게 포착하기 위한 탐색적 선별 결과로 해석해야 합니다.

프로젝트의 핵심 목적은 단순한 정확도 향상이 아니라, **PHQ8 기준 우울 위험군 선별 가능성 탐색**입니다. 따라서 최종 평가는 Accuracy보다 **Recall, F2-score, PR-AUC, False Negative 수**를 중심으로 해석합니다.

## 연구 주제

> KNHANES 2022 기반 수면·청각 지표와 PHQ8 기준 우울 위험군의 연관성 및 선별 가능성 분석

본 프로젝트는 다음 질문을 중심으로 진행되었습니다.

- 수면시간, 청각 문제, 소음 노출 관련 변수가 PHQ8 기준 우울 위험군 선별에 정보를 제공할 수 있는가?
- PHQ-9 문항 중 수면 문항을 제외한 PHQ8 기준으로 우울 위험군을 정의했을 때, 어떤 모델과 threshold 전략이 선별 목적에 적합한가?
- 클래스 불균형 상황에서 Accuracy보다 Recall, F2-score, PR-AUC, False Negative 수를 중심으로 평가하는 것이 왜 타당한가?

## 저장소 구조

```text
Team-5/
├── README.md
├── Team5_KNHANES2022_Project.ipynb
├── requirements.txt
├── figures/
│   ├── 01_target_dist.png
│   ├── 02_continuous.png
│   ├── 03_categorical.png
│   ├── 04_correlation.png
│   ├── 05_missing.png
│   └── 06_roc_pr_curves.png
├── docs/
│   └── meetings/
│       └── Noise_Sleep_and_Mental_Health_Prediction.pdf
├── .vscode/
│   └── settings.json
└── .gitignore
```

## 주요 파일 설명

| 파일/폴더 | 설명 |
|---|---|
| `Team5_KNHANES2022_Project.ipynb` | 데이터 불러오기, 전처리, EDA, 모델 학습, 성능 비교, 해석 과정을 포함한 최종 Jupyter Notebook |
| `requirements.txt` | 재현 실행을 위한 주요 Python 패키지와 로컬 환경 기준 고정 버전 |
| `figures/` | EDA 및 모델 평가 과정에서 생성된 주요 시각화 결과물 |
| `docs/meetings/` | 프로젝트 회의 및 발표 관련 문서 |
| `.vscode/settings.json` | Conda 기반 Python 환경 사용을 위한 VS Code 설정 |
| `.gitignore` | Python 캐시, 원시자료, 압축 파일, Excel 파일, 생성 산출물 등 제외 설정 |

## 데이터 안내

본 프로젝트는 국민건강영양조사(KNHANES) 제9기 1차년도(2022년) 원시자료를 사용합니다.

다만 KNHANES 원시자료 이용지침에 따라 자료의 무단 공유ㆍ복제 및 사전에 명시한 목적 외 재활용이 금지되어 있으므로, 본 저장소에는 원시자료 파일을 포함하지 않습니다.

원시자료는 **질병관리청 국민건강영양조사 홈페이지에서 별도 신청 후 다운로드**하십시오.

- 접속 경로: [질병관리청 국민건강영양조사](https://knhanes.kdca.go.kr/knhanes/main.do)
- 다운로드 경로: `원시자료` → `다운로드` → `2022년 검진조사, 건강설문조사, 영양조사` → `SAS`

다운로드한 `.sas7bdat` 데이터 파일은 `Team5_KNHANES2022_Project.ipynb`와 같은 위치에 배치한 뒤 실행하면 됩니다.

```text
Team-5/
├── Team5_KNHANES2022_Project.ipynb
└── hn22_all.sas7bdat
```

파일명이 다를 경우, 노트북 상단의 `file_path` 값을 실제 파일명에 맞게 수정해야 합니다.

```python
file_path = "hn22_all.sas7bdat"
df = pd.read_sas(file_path, format="sas7bdat", encoding="cp949")
```

## 분석 대상 및 변수 구성

### 입력 변수

수면시간, 청각 상태, 직업적 소음 노출, 이명, 이어폰 소음 노출, 청각 활동제한 등 수면·청각·소음 노출 관련 변수를 중심으로 사용했습니다.

### 타깃 변수

타깃 변수는 PHQ-9 문항 중 수면 문항을 제외한 PHQ8 총점을 기준으로 정의했습니다. PHQ-9에는 수면 관련 문항이 포함되어 있으므로, 수면시간 입력 변수와 타깃 간의 개념적 중복을 줄이기 위해 수면 문항 `phq_3`을 제외했습니다.

본 프로젝트에서는 PHQ8 총점 **7점 이상**을 우울 위험군으로 설정했습니다. 이 기준은 임상적 확정 진단이 아니라, 추가 평가가 필요할 가능성이 높은 선별 위험군을 정의하기 위한 연구용 기준입니다.

## 분석 흐름

1. **데이터 불러오기**
   - KNHANES 2022 SAS 데이터 로드
   - 데이터 크기 및 주요 변수 확인

2. **타깃 변수 생성**
   - PHQ-9 문항 확인
   - 수면 문항 제외 후 PHQ8 점수 계산
   - PHQ8 기준 우울 위험군 라벨 생성

3. **변수 선별 및 전처리**
   - 수면, 청각, 소음 노출 관련 변수 선택
   - 결측치 처리
   - 연속형/범주형 변수 분리
   - 스케일링 및 One-Hot Encoding 적용

4. **EDA**
   - 타깃 분포 확인
   - 연속형 변수 분포 확인
   - 범주형 변수와 타깃 간 관계 확인
   - 상관관계 및 결측 패턴 확인

5. **모델 학습 및 비교**
   - Logistic Regression
   - Random Forest
   - HistGradientBoosting
   - PyTorch 기반 Focal MLP

6. **불균형 데이터 대응**
   - `class_weight` 적용
   - UnderSampling 비교
   - threshold 조정
   - Focal Loss 기반 학습

7. **평가 및 해석**
   - Accuracy, Precision, Recall, F1-score, F2-score
   - ROC-AUC, PR-AUC
   - Confusion Matrix
   - False Negative 수
   - 변수 중요도 및 도메인 관점 해석

## 사용 기술

- Python
- Jupyter Notebook
- NumPy
- Pandas
- Matplotlib
- scikit-learn
- PyTorch
- SciPy
- SHAP

## 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/2026-1st/Team-5.git
cd Team-5
```

### 2. Conda 환경 생성

```bash
conda create -n team5-knhanes python=3.10
conda activate team5-knhanes
```

### 3. 필요한 패키지 설치

본 프로젝트는 재현성을 위해 `requirements.txt`를 제공합니다.

```bash
pip install -r requirements.txt
```

Conda 환경을 새로 만드는 경우:

```bash
conda create -n team5-knhanes python=3.10
conda activate team5-knhanes
pip install -r requirements.txt
```

### 4. 데이터 파일 준비

KNHANES 원시자료는 저장소에 포함되어 있지 않습니다. 질병관리청 국민건강영양조사 홈페이지에서 원시자료 이용 신청 후 데이터를 다운로드합니다.

다운로드한 `.sas7bdat` 파일을 노트북과 같은 위치에 둡니다.

```text
Team-5/
├── Team5_KNHANES2022_Project.ipynb
└── hn22_all.sas7bdat
```

파일명이 다르다면 노트북의 `file_path` 값을 실제 파일명으로 수정합니다.

### 5. Jupyter Notebook 실행

```bash
jupyter notebook Team5_KNHANES2022_Project.ipynb
```

또는 VS Code에서 해당 노트북을 열어 순서대로 실행할 수 있습니다.

### 재현성 관련 주의사항

- 원시자료 `hn22_all.sas7bdat`는 KNHANES 이용지침에 따라 저장소에 포함하지 않습니다.
- 노트북은 `hn22_all.sas7bdat` 파일이 프로젝트 루트 또는 노트북과 같은 폴더에 있다고 가정합니다.
- 주요 난수 기반 실험은 `random_state` 또는 seed를 고정하여 재현 가능성을 높였습니다.
- 데이터 전처리는 train/test split 이후 pipeline 내부에서 수행하여 test set 정보가 train 과정에 누수되지 않도록 구성했습니다.
- 원시자료 파일명이 다른 경우 노트북 상단의 `file_path` 값을 실제 파일명에 맞게 수정해야 합니다.

## 결과물

분석 과정에서 생성된 주요 시각화 결과는 `figures/` 폴더에 정리되어 있습니다.

- `01_target_dist.png`: 우울 위험군 타깃 분포
- `02_continuous.png`: 주요 연속형 변수 분포
- `03_categorical.png`: 주요 범주형 변수 분포 및 관계
- `04_correlation.png`: 변수 간 상관관계
- `05_missing.png`: 결측치 패턴
- `06_roc_pr_curves.png`: 모델별 ROC/PR 곡선

## 해석 시 주의사항

본 프로젝트는 우울증 확정 진단 모델을 개발한 것이 아닙니다. PHQ-9/PHQ8은 자가보고식 우울 증상 선별도구이며, 본 연구의 타깃인 PHQ8 기준 우울 위험군도 임상적 진단군이 아니라 연구용 선별 위험군입니다.

또한 KNHANES 2022 자료는 단면자료이므로, 본 분석 결과를 수면시간·청각 문제·소음 노출이 우울 위험을 인과적으로 유발한다는 의미로 해석할 수 없습니다. 본 연구에서의 “조기 선별”은 미래 우울증 발병을 예측한다는 의미가 아니라, 전문적 진단 또는 추가 평가 이전 단계에서 위험 신호를 넓게 포착한다는 의미입니다.

PHQ8 cutoff 7점 기준은 본 프로젝트에서 설정한 연구용 선별 기준입니다. 향후 연구에서는 PHQ8 8점, 9점, 10점 등 다양한 절단점에 대한 민감도 분석이 필요합니다.

Recall을 높이는 threshold 전략은 False Negative를 줄이는 데 도움이 될 수 있지만, False Positive 증가라는 trade-off를 동반합니다. 또한 threshold를 test set 기준으로 탐색하면 최종 성능이 다소 낙관적으로 추정될 수 있으므로, 향후에는 train/validation/test 분리 또는 교차검증 기반 threshold 탐색이 필요합니다.

설문 기반 데이터에는 응답자의 주관적 인식, 기억 오류, 사회적 바람직성 편향 등이 포함될 수 있습니다. 윤리 및 공정성 관점에서 모델 결과가 개인에 대한 낙인이나 차별적 판단으로 사용되어서는 안 됩니다. 따라서 본 모델은 단독 판단 도구가 아니라 PHQ 기반 평가, 상담, 전문가 면담 등 후속 절차로 연결하기 위한 1차 선별 보조 도구로 해석해야 합니다.

## 팀 정보

- 과목: 기계학습기초 팀 프로젝트
- 팀명: 5팀
- 주제: KNHANES 2022 기반 수면·청각 지표와 PHQ8 기준 우울 위험군 선별 가능성 분석
