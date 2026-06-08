# Team 5 - KNHANES 2022 Depression Risk Prediction

## 프로젝트 개요

본 저장소는 **국민건강영양조사(KNHANES) 제9기 1차년도 2022년 자료**를 활용하여 수면시간, 청각 문제, 소음 노출 관련 변수와 우울 위험군 사이의 관계를 분석하고, 우울 위험군 여부를 예측하는 머신러닝 팀 프로젝트입니다.

프로젝트의 핵심 목적은 단순한 정확도 향상이 아니라, **조기 선별 관점에서 우울 위험군을 놓치지 않는 예측 모델**을 비교·분석하는 것입니다. 따라서 최종 평가는 Accuracy보다 **Recall, F2-score, PR-AUC, false negative 수**를 중심으로 해석합니다.

## 연구 주제

> KNHANES 2022 기반 수면시간·청각 문제와 우울 위험군 예측

본 프로젝트는 다음 질문을 중심으로 진행되었습니다.

- 수면시간, 청각 문제, 소음 노출 관련 변수가 우울 위험군 예측에 기여할 수 있는가?
- PHQ-9 문항 중 수면 문항을 제외한 PHQ8 기준으로 우울 위험군을 정의했을 때, 어떤 모델이 조기 선별 목적에 적합한가?
- 클래스 불균형 상황에서 `class_weight`, UnderSampling, threshold 조정, Focal Loss 기반 신경망 접근이 어떤 차이를 보이는가?

## 저장소 구조

```text
Team-5/
├── README.md
├── Team5_KNHANES2022_Project.ipynb
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
| `figures/` | EDA 및 모델 평가 과정에서 생성된 주요 시각화 결과물 |
| `docs/meetings/` | 프로젝트 회의 및 발표 관련 문서 |
| `.vscode/settings.json` | Conda 기반 Python 환경 사용을 위한 VS Code 설정 |
| `.gitignore` | 대용량 원시 데이터, 생성 산출물, Python 캐시 파일 제외 설정 |

## 데이터 안내

본 프로젝트는 KNHANES 2022 원시자료 중 이미 하나의 파일로 병합된 단일 데이터셋을 사용합니다. 데이터 파일은 용량과 배포 제한을 고려하여 저장소에 포함하지 않았습니다.

실행 시 다음과 같이 로컬 환경에 데이터 파일을 준비해야 합니다.

```text
Team-5/
└── data/
    └── KNHANES_2022_merged.csv 또는 분석에 사용하는 병합 데이터 파일
```

노트북 내부의 `file_path` 값을 실제 데이터 파일 경로에 맞게 수정한 뒤 실행하면 됩니다.

## 분석 대상 및 변수 구성

### 입력 변수

수면시간, 청각 상태, 직업적 소음 노출, 이명, 이어폰 소음 노출, 청각 활동제한 등 수면·청각·소음 노출 관련 변수를 중심으로 사용했습니다.

### 타깃 변수

PHQ-9 총점 기반 우울 위험군 여부를 이진 분류 타깃으로 사용했습니다. 단, PHQ-9에는 수면 관련 문항이 포함되어 있으므로, 수면시간 변수와 타깃 간 개념적 중복을 줄이기 위해 **수면 문항을 제외한 PHQ8 총점**을 기준으로 우울 위험군을 정의했습니다.

본 프로젝트에서는 PHQ8 총점 **7점 이상**을 우울 위험군으로 설정했습니다.

## 분석 흐름

1. **데이터 불러오기**
   - KNHANES 2022 병합 데이터 로드
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

```bash
pip install numpy pandas matplotlib scikit-learn torch scipy shap jupyter
```

### 4. 데이터 파일 준비

`data/` 폴더를 생성한 뒤, KNHANES 2022 병합 데이터 파일을 넣습니다.

```bash
mkdir data
```

이후 노트북의 `file_path` 값을 실제 파일명에 맞게 수정합니다.

### 5. Jupyter Notebook 실행

```bash
jupyter notebook Team5_KNHANES2022_Project.ipynb
```

또는 VS Code에서 해당 노트북을 열어 순서대로 실행할 수 있습니다.

## 결과물

분석 과정에서 생성된 주요 시각화 결과는 `figures/` 폴더에 정리되어 있습니다.

- `01_target_dist.png`: 우울 위험군 타깃 분포
- `02_continuous.png`: 주요 연속형 변수 분포
- `03_categorical.png`: 주요 범주형 변수 분포 및 관계
- `04_correlation.png`: 변수 간 상관관계
- `05_missing.png`: 결측치 패턴
- `06_roc_pr_curves.png`: 모델별 ROC/PR 곡선

## 해석 시 주의사항

본 프로젝트는 설문 기반 공중보건 데이터를 활용한 머신러닝 분석입니다. 따라서 모델의 출력은 의학적 진단이 아니라, **우울 위험 가능성이 있는 집단을 조기에 선별하기 위한 탐색적 예측 결과**로 해석해야 합니다.

또한 KNHANES 자료는 자기보고식 문항을 포함하므로, 응답자의 주관적 인식과 보고 편향이 포함될 수 있습니다. 본 프로젝트에서는 이러한 한계를 고려하여 결과를 해석하며, 실제 임상적 판단에는 전문적인 진단 절차와 추가 평가가 필요합니다.

## 팀 정보

- 과목: 기계학습기초 팀 프로젝트
- 팀명: 5팀
- 주제: KNHANES 2022 기반 수면시간·청각 문제와 우울 위험군 예측
