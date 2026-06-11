# Team 5 - KNHANES 2022 PHQ8 기준 우울 위험군 선별 가능성 탐색

## 프로젝트 개요

본 프로젝트는 국민건강영양조사(KNHANES) 제9기 1차년도 2022년 자료를 사용해 수면시간, 청각 문제, 소음 노출 관련 자기보고 지표가 **PHQ8 기준 우울 위험군 선별 가능성**에 어떤 정보를 제공하는지 탐색한다.

PHQ-9/PHQ8은 임상적 확정 진단도구가 아니라 자가보고식 우울 증상 선별도구다. 따라서 본 분석의 타깃인 PHQ8 기준 우울 위험군도 임상적 진단군이 아니라 연구용 선별 기준이다. 모델 출력은 전문적 진단이나 상담 이전 단계에서 추가 평가가 필요할 수 있는 위험 신호를 넓게 포착하기 위한 탐색적 결과로 해석해야 한다.

PHQ-9에는 수면 관련 문항이 포함되어 있다. 본 프로젝트는 수면시간을 입력 변수로 사용하므로, 입력 변수와 타깃 점수 사이의 개념적 중복을 줄이기 위해 수면 문항 `phq_3`을 타깃 점수에서 제외하고 PHQ8 점수를 사용했다. 우울 위험군 기준은 `depression_risk = phq8_score >= 7`로 유지한다.

본 프로젝트에서 머신러닝 모델은 PHQ-9/PHQ8을 대체하기 위한 실사용 예측 도구가 아니라, 수면시간·청각 문제·소음 노출과 같은 비정신건강 자기보고 지표들이 PHQ8 기준 우울 위험군과 어느 정도의 선별 신호를 공유하는지 확인하기 위한 분석 방법으로 사용되었다. 따라서 모델 성능은 개인을 진단하거나 판정하기 위한 기준이 아니라, 해당 변수군이 PHQ8 위험군 구분에 제공하는 정보량을 탐색하기 위한 보조적 근거로 해석한다.

## 연구 질문

- 수면시간, 청각 문제, 소음 노출 관련 변수가 PHQ8 기준 우울 위험군 선별에 정보를 제공하는가?
- 동일한 데이터 분할에서 각 모델과 threshold 전략이 수면·청각·소음 지표의 선별 신호를 어떻게 다르게 포착하는가?
- 클래스 불균형 상황에서 Accuracy보다 Recall, F2-score, PR-AUC, False Negative 수를 함께 보는 것이 왜 필요한가?

## 저장소 구조

```text
Team-5/
|-- README.md
|-- Team5_KNHANES2022_Project.ipynb
|-- requirements.txt
|-- figures/
|   |-- 01_target_dist.png
|   |-- 02_continuous.png
|   |-- 03_categorical.png
|   |-- 04_correlation.png
|   |-- 05_missing.png
|   |-- 06_validation_f2_confusion_matrix.png
|   |-- 07_validation_screening_confusion_matrix.png
|   |-- 08_roc_pr_curves.png
|   |-- 12_confusion_matrix_best_model.png
|   |-- 13_feature_importance.png
|   |-- 14_shap_summary_rf_validation.png
|   |-- 14b_shap_original_variable_rf_validation.png
|   |-- 14c_shap_sleep_direction_rf_validation.png
|   |-- 15_overfitting_check.png
|-- outputs/
|   |-- default_threshold_validation_results.csv
|   |-- model_comparison_test_results.csv
|   |-- model_comparison_screening_test_results.csv
|   |-- validation_screening_thresholds.csv
|   |-- validation_selected_thresholds.csv
|   |-- validation_threshold_grid_results.csv
|   |-- overfitting_check.csv
|   |-- figure_registry.csv
|-- docs/
|-- .gitignore
```

## 주요 파일

| 파일/폴더 | 설명 |
|---|---|
| `Team5_KNHANES2022_Project.ipynb` | 데이터 로드, 전처리, EDA, 모델 학습, validation 기반 threshold 선택, 최종 test 평가, 해석을 포함한 Jupyter Notebook |
| `requirements.txt` | 현재 로컬 실행 환경 기준 주요 Python 패키지 고정 버전 |
| `figures/` | EDA, 성능 평가, 변수 중요도, SHAP 관련 시각화 |
| `outputs/` | 모델 비교표, validation threshold 탐색 결과, overfitting 점검, figure registry 등 재현용 CSV |
| `.gitignore` | 원시자료, 캐시, 민감 파일 제외 설정 |

## 데이터 안내

본 프로젝트는 국민건강영양조사(KNHANES) 2022년 원시자료를 사용한다. KNHANES 원시자료는 이용지침에 따라 무단 공유, 재배포, 사전 명시 목적 외 활용이 제한될 수 있으므로 저장소에 포함하지 않는다.

원시자료는 질병관리청 국민건강영양조사 홈페이지에서 별도 신청 및 다운로드한다.

- 접속 경로: [질병관리청 국민건강영양조사](https://knhanes.kdca.go.kr/knhanes/main.do)
- 다운로드 예시: `원시자료` -> `다운로드` -> `2022년 검진조사, 건강설문조사, 영양조사` -> `SAS`

다운로드한 `.sas7bdat` 파일은 notebook과 같은 위치에 둔다.

```text
Team-5/
|-- Team5_KNHANES2022_Project.ipynb
|-- hn22_all.sas7bdat
```

파일명이 다르면 notebook 상단의 `file_path` 값을 실제 파일명에 맞게 수정한다.

```python
file_path = "hn22_all.sas7bdat"
df = pd.read_sas(file_path, format="sas7bdat", encoding="cp949")
```

## 분석 설계

### 타깃 변수

- PHQ-9 문항 중 수면 문항 `phq_3`을 제외해 PHQ8 점수를 계산한다.
- PHQ8 총점 7점 이상을 PHQ8 기준 우울 위험군으로 정의한다.
- 이 기준은 확정 진단이 아니라 연구용 선별 기준이다.
- 이번 작업 범위에서는 PHQ8 cutoff 민감도 분석을 추가하지 않는다.

### 입력 변수

수면시간, 청각 상태, 소음 노출, 청각 활동제한 등 수면·청각·소음 노출 관련 변수를 중심으로 사용한다. PHQ 문항과 PHQ 파생 점수는 타깃 누수를 막기 위해 모델 입력에서 제외한다.

### 데이터 분할과 threshold 선택

모든 모델은 동일한 stratified train/validation/test split을 사용한다.

- train: 모델 학습에만 사용
- validation: threshold 선택에만 사용
- test: validation에서 선택된 threshold를 고정한 뒤 최종 평가에만 사용

현재 notebook은 64% train, 16% validation, 20% test 구조를 사용한다. 현재 실행 기준 split 크기는 train 3,100명, validation 776명, test 970명이다. 전처리는 split 이후 pipeline 내부에서 학습되어 validation/test 정보가 train 과정에 유입되지 않도록 구성했다.

## 모델 및 평가

본 프로젝트에서 모델 비교의 목적은 실제 서비스에 사용할 최종 예측기를 선정하는 것보다, 제한된 수면·청각·소음 관련 변수만으로 PHQ8 기준 위험군을 어느 정도 구분할 수 있는지 확인하는 데 있다. 즉, 모델은 개인의 우울 위험을 단정하기 위한 도구가 아니라, 변수군의 선별 정보량과 threshold 변화에 따른 FN/FP trade-off를 확인하기 위한 탐색적 분석 도구로 사용된다.

비교 모델은 다음을 포함한다.

- Logistic Regression
- Random Forest
- Hist Gradient Boosting
- Logistic Regression + UnderSampling
- Random Forest + UnderSampling
- Focal MLP

클래스 불균형 데이터에서는 다수 클래스를 예측하는 것만으로도 Accuracy가 높게 보일 수 있다. 따라서 Accuracy보다 우울 위험군을 놓치는 정도를 반영하는 Recall, F2-score, PR-AUC, False Negative 수를 중점적으로 해석한다.

F2-score는 Precision보다 Recall에 더 큰 가중치를 두므로, 조기 선별 목적에서 False Negative를 줄이는 전략을 평가하는 데 적합하다. 다만 Recall을 높이면 False Positive가 증가할 수 있으므로, Precision과 confusion matrix를 함께 확인한다.

## SHAP 해석 기준

Notebook의 SHAP 분석은 Random Forest 기준이다. 현재 SHAP 값은 validation set 776명을 전처리한 `776 × 22` encoded feature matrix 기준으로 계산된다. 이는 최종 threshold 적용 모델 자체를 직접 설명하기 위한 분석이 아니라, 수면·청각·소음 관련 변수가 비선형 모델에서 PHQ8 기준 우울 위험군 분류에 어떤 방식으로 기여하는지 탐색하기 위한 보조 분석이다.

대표 모델의 해석은 validation 기반 threshold 선택 결과와 해당 모델 기준 permutation importance를 중심으로 본다. Random Forest SHAP 결과는 수면·청각·소음 관련 변수의 비선형 선별 신호를 보완적으로 살펴보기 위한 탐색 결과로만 라벨링하며, 인과관계로 해석하지 않는다.

## 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/2026-1st/Team-5.git
cd Team-5
```

### 2. Python 환경 준비

권장 Python 버전은 3.10 계열이다.

```bash
conda create -n team5-knhanes python=3.10
conda activate team5-knhanes
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 원시자료 준비

`hn22_all.sas7bdat` 파일을 프로젝트 루트 또는 notebook에서 지정한 경로에 둔다. 원시자료는 저장소에 commit/stage하지 않는다.

### 5. Notebook 실행

```bash
jupyter notebook Team5_KNHANES2022_Project.ipynb
```

또는 VS Code에서 notebook을 열어 위에서부터 순서대로 실행한다.

## 산출물

분석 실행 후 주요 시각화는 `figures/`, 표 형태 결과는 `outputs/`에 저장된다.

주요 CSV 산출물:

- `outputs/default_threshold_validation_results.csv`
- `outputs/validation_threshold_grid_results.csv`
- `outputs/validation_selected_thresholds.csv`
- `outputs/validation_screening_thresholds.csv`
- `outputs/model_comparison_test_results.csv`
- `outputs/model_comparison_screening_test_results.csv`
- `outputs/overfitting_check.csv`
- `outputs/figure_registry.csv`

## 해석상 주의사항

본 프로젝트는 임상적 우울증 진단을 수행하지 않는다. PHQ-9/PHQ8은 자가보고식 선별도구이며, PHQ8 기준 우울 위험군도 임상적 진단군이 아니라 연구용 선별 타깃이다.

KNHANES 2022 자료는 단면자료이므로 수면시간, 청각 문제, 소음 노출이 우울 위험을 인과적으로 유발한다고 해석할 수 없다. 또한 본 분석은 미래 우울증 발병 예측이 아니라 현재 설문 응답 기반 선별 가능성 탐색이다.

따라서 본 연구의 결론은 “수면 불균형이나 소음 노출이 우울 위험을 유발한다”는 인과적 주장으로 해석해서는 안 된다. 다만 수면 패턴이 불균형하거나 소음 노출·청각 불편감이 있는 집단에서 PHQ8 기준 우울 위험 신호가 함께 나타날 가능성을 탐색적으로 확인했다는 점에서, 이러한 생활·환경 지표가 정신건강 측면의 추가 관심이나 후속 평가 필요성을 시사할 수 있다.

PHQ8 cutoff 7점 기준은 본 프로젝트의 연구용 선별 기준이다. 이번 작업 범위에서는 cutoff 민감도 분석을 추가하지 않았으므로, 다른 cutoff에서의 안정성은 별도 검토가 필요하다.

Threshold는 validation set에서만 선택했지만 단일 split 기반 결과이므로 표본 분할에 따른 변동 가능성이 남아 있다. 향후에는 교차검증 또는 반복 holdout 기반 threshold 선택으로 안정성을 확인할 필요가 있다.

설문 기반 데이터에는 응답자의 주관적 인식, 기억 오류, 사회적 바람직성 편향이 포함될 수 있다. 윤리 및 공정성 관점에서 모델 결과는 개인에 대한 낙인, 차별, 배제의 근거로 사용되어서는 안 되며, PHQ 기반 평가, 상담, 전문가 면담 등 후속 절차로 연결하기 위한 보조적 선별 정보로만 해석해야 한다.

## 팀 정보

- 과목: 기계학습기초 팀 프로젝트
- 팀명: 5팀
- 주제: KNHANES 2022 기반 수면·청각 지표와 PHQ8 기준 우울 위험군 선별 가능성 탐색
