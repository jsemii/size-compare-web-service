# 트러블슈팅 기록

개발 중 발생한 문제와 해결 과정을 기록합니다.
형식: 증상 → 원인 → 해결 → 배운 점


---


## 2026-07-15 (환경 세팅 & 프로젝트 초기화)

### 1. conda base 환경 자동 활성화
- **증상**: 터미널 프롬프트 앞에 `(base)`가 항상 표시됨
- **원인**: 기존 설치된 Anaconda가 셸 시작 시 base 환경을 자동 활성화. pyenv와 파이썬 관리 주체가 충돌할 소지
- **해결**: `conda config --set auto_activate_base false`로 자동 활성화를 비활성화 상태로 전환
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



## 2026-07-16 (회원가입 API + MySQL 연동)

### 1. bcrypt '72바이트 초과' 에러
- **증상** : 회원가입 요청 시 에러 발생. 입력한 비밀번호는 '1234'처럼 짧지만 '72바이트를 넘을 수 없다'는 메세지 나옴
  'ValueError: password cannot be longer than 72 bytes, truncate manually if necessary'
- **원인** : bcrypt는 원래 비밀번호를 최대 72바이트까지 처리하는 특성 있음. 하지만 이번 에러는 실제 비밀번호가 길어서 발생한 것이 아님, 비밀번호 해싱에 쓰는 'passlib'과 최신 'bcrypt(4.1이상)' 버전 사이의 호환성 문제로 발생함. 두 라이브러리가 맞지 않아 짧은 비밀번호에도 에러가 발생함
- **해결** : bcrypt를 4.1 미만 버전으로 고정. 이후 requirements.txt에 버전 기록해 재현 가능하도록 함
  'pip install 'bcrypt<4.1''
- **배운 점** : 에러 메세지의 표면적 내용 (72바이트 초과)과 실제 원인(라이브러리 버전 충돌)이 다를 수 있음. 에러 메세지만 보고 문제를 해결하려고 했다면 한참 헤맸을 것임. 라이브러리 버전 충돌은 문제가 된 버전을 고정하는 것이 표준적인 해결방법. requirements.txt에 버전 명시해두면 다른 환경에서도 같은 문제 피할 수 있음

### 2. MySQL localhost와 127.0.0.1 접속 차이
- **증상** : 백엔드(appuser 계정)은 MySQL에 정상 접속해서 회원가입 데이터까지 저장됐는데 터미널에서 'docker exec'로 같은 appuser 계정 접속 시도하면 거부 당함
  'ERROR 1045 (28000): Access denied for user 'appuser'@'localhost' (using password: YES)'
- **원인** : MySQL은 접속 출처(host)에 따라 권한 다르게 취급함. 'localhost'로 접속하면 유닉스 소켓이라는 통로를 쓰고, '127.0.0.1'로 접속하면 TCP 네트워크 통로를 쓰는데, MySQL은 둘을 다른 접속으로 구분함. 백엔드는 컨테이너 외부에서 네트워크(TCP)로 접속해 성공했지만, 'docker exec'로 컨테이너 내부에서 'localhost'로 붙는 경로에 appuser 권한이 없어 거부됨. 
- **해결** : 데이터 확인이 목적이었으므로 모든 접속이 허용된 root 계정으로 조회해 데이터가 정상 작동된 것을 확인함
  'docker exec -it size-compare-mysql mysql -u root -prootpass size_compare -e "SELECT ... FROM users;"'
appuser에 localhost 권한을 추가하면 docker exec 접속도 가능하지만, 조치하지 않기로 판단함. 앱은 TCP(127.0.0.1)로 정상 접속하고, 거부된 localhost 소켓은 실제로 쓰지 않는 경로이며, 안 쓰는 경로를 위해 권한을 넓히는 것은 최소 권한 원칙에 어긋나기 때문. 버그가 아니라 MySQL의 정상적인 접속 구분 동작임.
- **배운 점** : localhost와 127.0.0.1(TCP)는 MySQL에서 다른 접속 경로임. 모든 이상 현상이 고쳐야 할 문제는 아니며, 실제 사용 경로와 보안 원칙을 근거로 조치하지 않는 것도 엔지니어링 판단임.
