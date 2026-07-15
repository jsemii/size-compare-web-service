# 트러블슈팅 기록

개발 중 발생한 문제와 해결 과정을 기록합니다.
형식: 증상 → 원인 → 해결 → 배운 점

---

## 2026-07-15 (1일차: 환경 세팅 & 프로젝트 초기화)

### 1. conda base 환경 자동 활성화
- **증상**: 터미널 프롬프트 앞에 `(base)`가 항상 표시됨
- **원인**: 기존 설치된 Anaconda가 셸 시작 시 base 환경을 자동 활성화. pyenv와 파이썬 관리 주체가 충돌할 소지
- **해결**: `conda config --set auto_activate_base false`로 자동 활성화 비활성화
- **배운 점**: 파이썬 버전 관리 도구(conda, pyenv)를 혼용하면 어떤 파이썬이 우선되는지 모호해짐. 한 프로젝트에서는 관리 주체를 하나로 통일해야 함

### 2. `python` 명령어 인식 안 됨
- **증상**: `python -m venv .venv` 실행 시 `command not found: python`
- **원인**: macOS는 `python`(2.x 계열 명칭)을 기본 제공하지 않음. `python3`으로 호출해야 함
- **해결**: `python3 -m venv .venv`로 실행. 가상환경 활성화 후에는 내부에서 `python`도 사용 가능
- **배운 점**: macOS/Linux 기본 환경에서는 `python3`이 표준. 가상환경 내부에서만 `python` 별칭이 생성됨

### 3. pyenv 버전이 적용되지 않음 (python3이 시스템 3.9.6으로 실행됨)
- **증상**: `pyenv version`은 3.12.13을 가리키는데, `python3 --version`은 3.9.6(시스템 파이썬) 출력
- **원인**: `.zshrc`에 pyenv 초기화 코드가 등록되지 않아 pyenv shim이 PATH에 추가되지 않음. shim을 거치지 않으니 시스템 파이썬이 실행됨
- **해결**: `.zshrc`에 아래 세 줄 추가 후 `source ~/.zshrc`로 적용

      export PYENV_ROOT="$HOME/.pyenv"
      [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
      eval "$(pyenv init - zsh)"

- **배운 점**: pyenv는 shim(중계 실행 파일)을 PATH 최상단에 두어 파이썬 호출을 가로챈다. 초기화 코드가 셸 설정에 없으면 pyenv가 설치돼 있어도 버전 전환이 동작하지 않음. `pyenv version`(pyenv 내부 상태)과 실제 `python3` 실행 경로는 별개임

### 4. 로컬 브랜치 이름이 master로 만들어짐
- **증상**: `git status`를 치니 현재 브랜치가 `main`이 아니라 `master`로 나옴
- **배경 설명**: git에서 "브랜치"는 작업을 담는 가지(줄기). 예전에는 첫 브랜치 이름이 `master`가 기본이었는데, 요즘은 `main`을 표준으로 씀. GitHub 원격 저장소는 `main`을 쓰는데 내 컴퓨터(로컬)만 옛날 이름 `master`로 잡혀서 이름이 서로 어긋난 상황
- **원인**: 이 저장소가 처음 만들어질 때 기본 브랜치 이름이 `master`로 정해짐. 미리 `main`으로 바꾸는 설정을 해뒀어도, 이미 만들어진 저장소에는 그 설정이 적용되지 않음
- **해결**: `git branch -m master main` 실행 (`-m`은 이름 바꾸기(move/rename). "master를 main으로 바꿔라")
- **배운 점**: `git config --global init.defaultBranch main` 설정은 "앞으로 새로 만들 저장소"에만 적용되고, 이미 만들어진 저장소에는 소급 적용되지 않음

### 5. PR(코드 합치기 요청)이 만들어지지 않음
- **증상**: `gh pr create` 실행 시 "head branch is the same as base branch"(합칠 두 브랜치가 같다), 이어서 "could not find any commits between..."(두 브랜치 사이에 차이가 없다)는 에러
- **배경 설명**: PR(Pull Request)은 "이 브랜치의 변경 내용을 저 브랜치에 합쳐도 될까요?"라는 요청. 그래서 원래는 서로 다른 두 브랜치(예: 작업 브랜치 → main)가 있어야 하고, 둘 사이에 차이(변경된 내용)가 있어야 함
- **원인**: 작업 브랜치(feature/init-skeleton)를 GitHub에 먼저 올리는 바람에, GitHub이 그 브랜치를 저장소의 기본 브랜치로 자동 지정함. 그 후 main을 똑같은 지점에서 만들어서, 두 브랜치의 내용이 완전히 동일 → "합칠 차이가 없다"는 상황이 됨
- **해결**:
  1. `git push -u origin main` → main 브랜치를 GitHub에 올림
  2. `gh repo edit --default-branch main` → 저장소의 기본 브랜치를 main으로 변경
  3. 이번엔 첫 커밋이라 두 브랜치 차이가 없으므로 PR은 생략하고, 다 쓴 작업 브랜치는 삭제해서 정리
- **배운 점**: GitHub 저장소의 기본 브랜치는 "가장 먼저 올라온 브랜치"로 정해질 수 있음. 그래서 main을 먼저 올리고, 그다음에 작업 브랜치를 나누는 순서가 안전함. PR은 두 브랜치 사이에 실제 차이가 있어야만 만들 수 있음

