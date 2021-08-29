# 23-2nd-caseT-Fany-backend

## caseT-fany Project Family

- F.E<br>
  [이정일]<br>
  [박태환]<br>
  [차예은]<br>
  [박정우]<br>
  <br>
- B.E<br>
  [김훈태]<br>
  [한승훈]<br> 
  <br>

## What is caseT-fany Project?
### 개발 인원 및 기간

- 개발기간 : 2021/8/17 ~ 2021/8/27
- 개발 인원 : 프론트엔드 4명, 백엔드 2명
- 프론트엔드 github link : https://github.com/wecode-bootcamp-korea/23-2nd-caseT-Fany-frontend

### 프로젝트 선정이유
짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 클론했습니다.
개발은 초기 세팅부터 전부 직접 구현했으며, 모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.

### 협업 도구

- Slack / Git + GitHub / Trello, Notion를 이용해 일정관리, 현황을 관리
<img width="1399" alt="스크린샷 2021-08-29 오후 1 22 21" src="https://user-images.githubusercontent.com/76812640/131238315-03fa8546-338f-4d21-a9fa-8291e462927f.png">


### 적용 기술

> -Front-End : javascript, React.js framwork, sass<br>
> -Back-End : Python, Django web framework, MySQL, Bcrypt, pyjwt, Docker<br>
> -Common : POSTMAN, RESTful API, aws

#### 구현기능

  #### 회원가입 / 로그인페이지 / 카카오로그인

- 회원가입 시 정규식을 통한 유효성 검사. (소문자, 대문자, 특수문자의 조합)
- 로그인을 이후 토큰 발행, 계정 활성화
- 카카오 api를 이용해 소셜로그인 기능 구현, 코드 및 토큰을 받아 유저정보 수령 및 저장

  #### 리스트 페이지

- 키워드(카테고리, 세부 카테고리, color, 디자이너등등...) 다중 필터
- 페이지네이션

  #### 상세페이지

- 티셔츠 커스텀 기능(컬러, 사이즈, 텍스트작성, 텍스트폰트, 텍스트컬러 등등...)
- 식당에 대한 리뷰 평점순으로 나열, 페이지네이션.
- 리뷰 생성, 수정, 삭제

<br>
소셜사이트의 기본적인 기능들을 다루며 전반적인 플로우와 소셜 로그인의 프로세스를 배울 수 있었습니다.
또한 query debugger로 ORM를 최적화했으며 unit test로 클린한 코드 작성을 위해 노력했습니다.
<br>

#### Google Spreadsheet(API정의서)
- API별 기능, Method, URI, Request 및 Response 정리
- https://docs.google.com/spreadsheets/d/1GoiUTmnslPovPwVa1ZrkR5dllhyQLWNN1SoYjFmx4A0/edit#gid=0

## Reference

- 이 프로젝트는 [CaseTify] https://www.casetify.com/?gclid=Cj0KCQjwvaeJBhCvARIsABgTDM62oVIoktKXduLFRiZFZ7gkB-rhTPz8UwQVrsFVddS90hIr5yUEuIoaAoOMEALw_wcB 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
