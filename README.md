# 나만의 Python 퀴즈 게임

## 프로젝트 개요

Python으로 만드는 터미널 기반 퀴즈 게임입니다.

Python 기본 문법, 클래스, JSON 파일 저장, Git과 GitHub 사용법을 학습하는 프로젝트입니다.

메뉴, 퀴즈 플레이, 퀴즈 추가, 목록 조회, 최고 점수 관리를 구현했습니다.
퀴즈와 최고 기록을 프로젝트 루트의 state.json에 저장합니다.

Quiz와 QuizGame 클래스로 역할을 분리했으며, 파일 손상과 읽기·쓰기 오류를 처리합니다.


## Git 복제 및 동기화 실습

별도 로컬 폴더에 저장소를 복제한 뒤 README를 수정하여 commit과 push를 수행했습니다.
이후 원래 작업 폴더에서 pull로 변경을 가져와 반영 여부를 확인했습니다.

아래는 실제 터미널 실행 기록의 핵심 부분입니다.
객체 전송 진행률 등 일부 출력은 생략했습니다.

### 1. 별도 폴더에 저장소 복제

<details>
<summary>clone 실행 기록</summary>

```text
PS C:\Users\Austarthia> git clone https://github.com/Asheli1a/02-python-first-steps.git quiz-game-clone
Cloning into 'quiz-game-clone'...
```

객체 수신과 델타 처리가 완료된 뒤 복제 폴더로 이동했습니다.

```text
PS C:\Users\Austarthia> cd .\quiz-game-clone
PS C:\Users\Austarthia\quiz-game-clone> Get-Location

Path
----
C:\Users\Austarthia\quiz-game-clone

PS C:\Users\Austarthia\quiz-game-clone> git log --oneline -3
5ba620b (HEAD -> main, origin/main, origin/HEAD) Docs: 저장 파일과 저장 테스트를 README 파일 구조에 반영
f6c813a Feat: JSON 저장과 복원 및 손상 파일 백업과 오류 처리 구현
f34c485 Refactor: QuizGame으로 게임 상태와 메뉴 진행 관리
```

</details>

### 2. 복제본에서 README 수정 후 commit·push

<details>
<summary>복제본의 변경 기록</summary>

복제본에서 Git 작성자 설정을 완료하고 README를 수정했습니다.

```text
PS C:\Users\Austarthia\quiz-game-clone> git add README.md
PS C:\Users\Austarthia\quiz-game-clone> git commit -m "Docs: 복제 저장소에서 Git 동기화 실습 절차 추가"
[main 3dc8f67] Docs: 복제 저장소에서 Git 동기화 실습 절차 추가
 1 file changed, 8 insertions(+)
```

이어서 원격 main 브랜치에 업로드했습니다.
다음은 push 명령과 성공 결과입니다.

```text
PS C:\Users\Austarthia\quiz-game-clone> git push origin main
To https://github.com/Asheli1a/02-python-first-steps.git
   5ba620b..3dc8f67  main -> main
```

</details>

### 3. 원래 작업 폴더에서 pull

<details>
<summary>pull 실행 기록과 반영 확인</summary>

원래 작업 폴더로 돌아와 원격 변경을 가져왔습니다.
다음은 pull 명령과 주요 결과입니다.

```text
PS C:\Users\Austarthia\quiz-game-clone> cd C:\Users\Austarthia\quiz-game
PS C:\Users\Austarthia\quiz-game> git pull --ff-only origin main
```

```text
Updating 5ba620b..3dc8f67
Fast-forward
 README.md | 8 ++++++++
 1 file changed, 8 insertions(+)
```

원래 폴더의 이력에도 복제본에서 만든 커밋이 반영됐습니다.
당시 git log 출력의 첫 줄은 다음과 같습니다.

```text
* 3dc8f67 (HEAD -> main, origin/main) Docs: 복제 저장소에서 Git 동기화 실습 절차 추가
```

최종 작업 상태도 확인했습니다.

```text
PS C:\Users\Austarthia\quiz-game> git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

</details>

### 실습 결과

- clone으로 원격 저장소를 별도 폴더에 복제했습니다.
- 복제본에서 README를 수정하고 커밋 3dc8f67을 생성했습니다.
- push로 해당 커밋을 원격 main에 반영했습니다.
- 원래 폴더에서 pull하여 5ba620b에서 3dc8f67로 갱신했습니다.
- README 8줄의 반영과 원격 브랜치 동기화를 확인했습니다.

위 기록은 실습 당시의 상태이며, 이후 기능·문서 정리 커밋이 추가되었습니다.


## 퀴즈 주제와 선정 이유

주제: 컴퓨터 기초 및 Python·Git 학습 개념

선정 이유: 관심 있는 컴퓨터 기초 지식과 이번 미션에서 배운 Python·Git 개념을 퀴즈로 만들며 학습 내용을 복습하기 위해 선정했습니다.


## 개발 환경

- Python 3.10 이상
- Git
- VS Code
- 외부 라이브러리 사용 없음


## 실행 방법

프로젝트 폴더에서 다음 명령어를 실행합니다.

```bash
python main.py
```


## 기능 목록

- [x] 메뉴 표시 및 입력 처리
- [x] 퀴즈 풀기
- [x] 퀴즈 추가
- [x] 퀴즈 목록 확인
- [x] 최고 점수 확인
- [x] JSON 파일 저장 및 불러오기
- [x] 오류 처리 및 안전한 종료


## 파일 구조

```text
quiz-game/
├── .gitignore
├── README.md
├── docs/
│   └── screenshots/
├── main.py
├── state.json
├── test_quiz.py
├── test_play.py
├── test_add.py
├── test_list.py
├── test_score.py
├── test_game.py
└── test_storage.py
```


## 코드 구조

- Quiz: 문제 하나의 데이터, 출력, 정답 확인을 담당합니다.
- QuizGame: 퀴즈 목록과 최고 기록을 보관하고 메뉴와 게임 진행을 관리합니다.
- 공통 함수: 입력 검증과 개별 기능 처리를 담당하며 QuizGame에서 재사용합니다.


## 학습 목표와 구현 연결

이 프로젝트에서 사용한 Python과 Git 개념을 실제 코드와 연결해 정리했습니다.

### 1. 변수와 자료형

변수는 객체에 이름을 붙여 값을 참조하고 재사용하기 위한 수단입니다.
Python에서 이름은 객체를 참조하며, 자료형은 객체에 속합니다.

예를 들어 correct_count는 이번 게임의 정답 수를 관리합니다.

```python
correct_count = 0
correct_count += 1
```

주요 자료형의 용도는 다음과 같습니다.

| 자료형 | 의미 | 프로젝트 예시 |
|---|---|---|
| int | 정수 | 정답 번호, 정답 수 |
| str | 문자열 | 문제, 선택지, 사용자 입력 |
| bool | 참 또는 거짓 | 정답 판정, 저장 성공 여부 |
| list | 순서가 있고 수정 가능한 목록 | 퀴즈 목록, 선택지 목록 |
| dict | 키와 값으로 구성하는 자료구조 | 최고 기록, JSON 저장용 데이터 |

input()의 반환값은 문자열입니다.
따라서 숫자 비교가 필요한 곳에서는 int()로 변환합니다.

```python
text = input("정답: ").strip()
number = int(text)
```

변환할 수 없는 문자열이면 ValueError가 발생하므로 프로그램에서는 try/except로 처리합니다.

None은 bool이나 숫자 0과 다른 값이며, 이 프로젝트에서는 '아직 기록 없음' 또는 '게임을 진행하지 않음'을 나타냅니다.

```python
if correct_count is not None:
    # 0개 정답도 완료한 게임으로 기록합니다.
    ...
```

### 2. 조건문: if / elif / else

조건에 따라 서로 다른 코드를 실행할 때 사용합니다.
하나의 if/elif/else 묶음에서는 처음 참이 되는 분기를 실행합니다.

이 프로젝트에서는 선택한 메뉴에 따라 실행할 기능을 결정합니다.

```python
if choice == 1:
    self.play()
elif choice == 2:
    self.add_quiz()
else:
    ...
```

정답 판정과 빈 목록 확인에도 조건문을 사용합니다.

### 3. 반복문: for와 while

for는 목록 등 반복 가능한 대상의 항목을 순서대로 처리할 때 사용합니다.
while은 조건이 참인 동안 계속 반복할 때 사용합니다.

- for: 퀴즈 출제, 선택지 출력, 선택지 4개 입력
- while: 메뉴 반복, 올바른 입력을 받을 때까지 재입력

```python
for quiz in quizzes:
    quiz.display()
```

```python
while True:
    # 입력을 검사하고 필요하면 다시 입력받습니다.
    ...
```

break는 가장 가까운 반복문을 끝냅니다.
continue는 현재 반복의 남은 부분을 건너뛰고 다음 반복으로 이동합니다.

### 4. 함수·매개변수·반환값

함수는 반복해서 사용할 동작에 이름을 붙인 것입니다.
동작을 나누면 재사용과 테스트가 쉬워집니다.

매개변수는 함수 정의에서 입력을 받는 이름이고, 인자는 함수를 호출할 때 전달하는 실제 값입니다.
return은 결과를 돌려주고 해당 함수 실행을 끝냅니다.

```python
def input_int(prompt, minimum, maximum):
    ...
    return number

choice = input_int("선택: ", 1, 5)
```

위 코드에서 prompt, minimum, maximum은 매개변수이고, "선택: ", 1, 5는 전달한 인자입니다.
반환된 정수는 choice가 참조합니다.

명시적으로 값을 반환하지 않는 함수의 반환값은 None입니다.

### 5. 클래스와 객체

클래스는 관련 데이터와 동작을 묶는 정의입니다.
객체는 그 클래스를 사용해 만든 개별 인스턴스입니다.

- Quiz: 문제 하나의 데이터와 동작
- QuizGame: 퀴즈 목록, 최고 기록, 메뉴와 진행 흐름

```python
quiz = Quiz(
    question="두 번째 선택지를 고르세요.",
    choices=["A", "B", "C", "D"],
    answer=2,
)
```

Quiz는 클래스이고, quiz가 참조하는 값은 Quiz의 객체입니다.

여러 Quiz 객체는 같은 메서드 정의를 사용하지만, 각자의 문제·선택지·정답을 보관합니다.

### 6. __init__, self, 속성과 메서드

__init__은 일반적인 객체 생성 과정에서 초기 상태를 설정하는 메서드입니다.
객체 자체를 생성하는 역할과 초기화하는 역할은 엄밀히 구분됩니다.

self는 인스턴스 메서드가 전달받는 해당 객체 자신입니다.
self라는 이름은 Python의 관례입니다.

```python
def __init__(self, question, choices, answer):
    self.question = question
    self.choices = choices
    self.answer = answer
```

속성은 객체가 보관하는 데이터이고, 메서드는 객체에 연결된 함수입니다.

- 속성: quiz.question, quiz.answer
- 메서드: quiz.display(), quiz.check_answer(2)

```python
quiz.display()
is_correct = quiz.check_answer(2)
```

QuizGame의 self.quizzes와 self.best_score도 인스턴스 속성입니다.
각 게임 객체는 독립된 상태를 보관합니다.

### 7. 파일 열기·읽기·쓰기

파일은 경로, 모드, 인코딩을 지정해 엽니다.

- r: 읽기
- w: 쓰기. 기존 파일이 있으면 내용을 비우므로 주의해야 합니다.
- encoding="utf-8": 한글을 일관된 인코딩으로 처리

with 문을 사용하면 해당 구역을 벗어날 때 파일을 닫습니다.

```python
with self.state_path.open("r", encoding="utf-8") as file:
    data = json.load(file)
```

이 프로젝트는 저장할 때 기존 state.json에 바로 쓰지 않고, 임시 파일에 작성한 뒤 교체합니다.
따라서 임시 파일 작성이나 교체가 실패하면 기존 파일을 보존할 수 있습니다.

강제 종료나 정전까지 저장 완료를 보장하는 것은 아닙니다.

### 8. JSON과 데이터 영속성

JSON은 객체, 배열, 문자열, 숫자 등을 표현하는 텍스트 기반 데이터 교환 형식입니다.

프로그램 메모리의 값은 종료 후 자동으로 복원되지 않으므로, 파일에 기록하고 다음 실행에서 읽어 데이터 영속성을 구현합니다.

- json.dump(): Python 데이터를 파일에 JSON으로 기록
- json.load(): 파일의 JSON을 Python 데이터로 읽기
- Python dict는 JSON 객체로, list는 JSON 배열로 표현
- Python None은 JSON null로 표현

Quiz 객체를 그대로 저장하는 대신 필요한 속성을 딕셔너리로 바꿔 저장합니다.

```python
{
    "question": quiz.question,
    "choices": quiz.choices,
    "answer": quiz.answer,
}
```

불러올 때는 parse_state()로 자료형과 값의 범위를 검사한 뒤 다시 Quiz 객체를 만듭니다.

JSON 문법이 맞는 것과 게임 데이터로 유효한 것은 다릅니다.
선택지 개수나 정답 범위도 별도로 검사해야 합니다.

### 9. try / except와 안전한 종료

try는 오류가 발생할 수 있는 코드를 실행하고, except는 지정한 예외가 발생했을 때 실행할 처리를 정의합니다.

이 프로젝트의 주요 처리 대상은 다음과 같습니다.

| 예외 | 발생 상황 | 처리 |
|---|---|---|
| ValueError | 숫자 변환 실패, 데이터 검증 실패 | 재입력 또는 손상 처리 |
| FileNotFoundError | 저장 파일 없음 | 기본 퀴즈 사용 |
| OSError | 파일 접근·저장 오류 | 안내와 원본 보호 |
| KeyboardInterrupt | Ctrl+C | 안내 후 종료 및 저장 시도 |
| EOFError | 입력 스트림 종료 | 안내 후 종료 및 저장 시도 |

JSONDecodeError는 ValueError의 하위 예외이므로 저장 파일을 읽는 코드의 ValueError 처리에 포함됩니다.

finally는 예외 발생 여부와 관계없이 정리 코드를 실행할 때 사용합니다.
이 프로젝트에서는 종료 시 가능한 범위에서 저장을 시도합니다.

### 10. Git과 GitHub

Git은 파일 변경 이력을 로컬 저장소에 기록하고 관리하는 분산 버전 관리 도구입니다.

GitHub는 Git 저장소를 원격으로 보관하고 공유·협업할 수 있게 하는 서비스입니다.

commit은 로컬 기록이며, GitHub 업로드는 push로 수행합니다.

| 명령 | 역할 | 이 프로젝트에서의 사용 |
|---|---|---|
| git init | 현재 폴더를 Git 저장소로 초기화 | 프로젝트 시작 |
| git add | 다음 커밋에 넣을 변경을 스테이징 | 기능별 변경 선택 |
| git commit | 스테이징된 변경을 로컬 이력으로 기록 | 기능별 작업 기록 |
| git push | 원격 저장소에 로컬 커밋 반영 | GitHub 업로드 |
| git pull | 원격 변경을 가져와 현재 브랜치에 통합 | 복제본의 수정 가져오기 |
| git checkout | 브랜치 전환 등 | main과 feature/play 전환 |
| git clone | 저장소와 이력을 새 폴더에 복제 | 별도 폴더 실습 |
| git merge | 다른 브랜치의 변경을 현재 브랜치에 통합 | 플레이 기능 병합 |

git add 이후 파일을 다시 수정하면, 그 수정은 다시 add해야 다음 커밋에 포함됩니다.

### 11. 브랜치 생성과 병합

브랜치는 독립된 작업 흐름을 관리하기 위한 수단입니다.
이 프로젝트에서는 플레이 기능을 별도 브랜치에서 구현했습니다.

```bash
git checkout -b feature/play
```

기능 완성과 커밋 후 main으로 돌아와 병합했습니다.

```bash
git checkout main
git merge --no-ff feature/play -m "Merge: 퀴즈 플레이 기능 브랜치 병합"
```

--no-ff는 fast-forward가 가능한 경우에도 병합 커밋을 만들어
분기와 병합 이력을 명확하게 남깁니다.

### 12. clone과 pull의 차이

clone은 저장소가 없는 위치에 새로운 로컬 복제본을 만드는 작업입니다.
pull은 이미 존재하는 로컬 저장소에 원격 변경을 가져와 통합하는 작업입니다.

이 실습에서는 복제본에서 생성한 3dc8f67 커밋을 push하고, 원래 작업 폴더에서 pull하여 같은 커밋이 반영되는지 확인했습니다.


## 점수 규칙

- 점수는 정답 수 / 전체 문제 수 × 100으로 계산합니다.
- 화면에는 소수점 없이 반올림하여 표시합니다.
- 최고 기록 비교에는 반올림하지 않은 정답률을 사용합니다.
- 같은 정답률이면 먼저 달성한 기록을 유지합니다.
- 최고 기록에는 당시 정답 수와 전체 문제 수를 보관합니다.
- 완료한 게임만 기록하며, 첫 게임이 0점이어도 기록합니다.
- 최고 기록은 state.json에 저장되어 재실행 후에도 유지됩니다.


## 테스트 방법

Quiz 클래스의 문제 출력과 정답 판정을 확인합니다.

기본 퀴즈 5개 이상의 데이터 형식도 검사합니다.
문제와 선택지의 빈 값, 선택지 개수, 정답 번호 범위를 확인합니다.

```bash
python test_quiz.py
```

플레이 테스트는 모두 정답, 모두 오답, 잘못된 입력,
퀴즈가 없는 경우를 확인합니다.

```bash
python test_play.py
```

퀴즈 추가 테스트는 정상 등록, 공백 제거, 잘못된 입력,
입력 중단 시 미완성 데이터 추가 방지를 확인합니다.

```bash
python test_add.py
```

퀴즈 목록 테스트는 기본 목록, 추가한 문제의 반영,
퀴즈가 없는 경우를 확인합니다.

```bash
python test_list.py
```

최고 점수 테스트는 미플레이 상태, 첫 0점 기록,
정답률 비교, 동점 유지, 기록 출력을 확인합니다.

```bash
python test_score.py
```

QuizGame 테스트는 초기 상태, 객체 간 상태 분리,
플레이 결과 반영, 입력 중단, 메뉴 연결을 확인합니다.

```bash
python test_game.py
```

저장 테스트는 임시 폴더에서 저장·복원, 손상 복구,
읽기·쓰기 오류와 원본 보호를 확인합니다.

```bash
python test_storage.py
```


## 데이터 파일 설명

- 경로: main.py와 같은 프로젝트 루트의 state.json
- 인코딩: UTF-8
- quizzes: 문제, 선택지 4개, 정답 번호로 구성한 목록
- best_score: 최고 기록. 미플레이 상태는 null
- 최고 기록에는 correct_count와 total을 저장합니다.

데이터 구조 예시:

```json
{
    "quizzes": [
        {
            "question": "테스트 문제",
            "choices": ["A", "B", "C", "D"],
            "answer": 2
        }
    ],
    "best_score": {
        "correct_count": 1,
        "total": 1
    }
}
```

- 파일이 없으면 기본 퀴즈로 시작합니다.
- 손상 파일은 state.json.corrupt-식별자.bak으로 백업한 뒤 초기화합니다.
- 읽기 또는 백업에 실패하면 원본 보호를 위해 해당 실행의 저장을 중지합니다.
- 저장은 임시 파일 작성 후 기존 파일 교체 순서로 수행합니다.
- 퀴즈 등록, 게임 완료, 정상 종료 및 처리된 입력 중단 시 저장을 시도합니다.
- 강제 프로세스 종료나 정전 시 저장 완료를 보장하지 않습니다.


## 개발 환경 및 Git 이력

### 개발 환경
![개발 환경](docs/screenshots/environment.png)

### 커밋과 브랜치 병합 이력
![Git 이력](docs/screenshots/git_log.png)

## 실행 화면

### 메뉴
![메뉴](docs/screenshots/menu.png)

### 퀴즈 추가
![퀴즈 추가](docs/screenshots/add_quiz.png)

### 퀴즈 목록
![퀴즈 목록](docs/screenshots/list.png)

### 플레이 결과
![플레이 결과](docs/screenshots/play.png)

### 최고 점수
![최고 점수](docs/screenshots/score.png)
이번 게임은 8문제 중 4개 정답으로 50점이며,
기존 최고 기록인 6문제 중 4개 정답·67점은 유지됩니다.

### 재실행 후 데이터 유지
![데이터 유지](docs/screenshots/persistence.png)