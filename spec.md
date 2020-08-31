## Syntax 간단 정리

${{  }} 기본적인 형태.  함수 동작은 지원하지 않고 값 치환만을 지원하며, 다른 플랫폼들처럼 .을 이용해 접근이 가능하다. 

사용가능한 변수명 - var, env, self, tasks

task는 array지만, task에 id를 부여하면 tasks.xxx와 같은 형식을 이용해 원하는 task에 접근할 수 있다.

위에서 아래로 sequential하게 작업한다. 위에서 ${{ ... }}} template을 이용해 값을 치환하여 업데이트한다. 또한 task 수행 후 output을 업데이트한다.

따라서 아랫 부분의  task에서는 윗 부분의 task에 ${{ ... }} 을 통해 접근할 수 있다.

## Root Depth.

* var
  * ${{ var.xxx }}로 사용하고자하는 variables
  * dict, list, str, int 가 가능하다.
  * 아직 override는 고려하지 않고 단순하게 tasks, env와 함께 하나의 yaml file에 정의
* env
  * host의 env에 없는 내용을 넣어주거나, 있는 내용을 오버라이드 함.
  * str만 가능하다.
  * 아직 spacectl apply -e 옵션은 고려하지 않음
* tasks
  * 현재 yaml file에서 수행하고자하는 작업들.
  * github action의 step과 유사.
  * ansible의 playbook과 유사
  * terraform의 하나의 resource나 data와 유사
  * name, id uses, spec

## Tasks

### 사용하는 field 정리

* name - 현재 task의 이름 및 설명
  e.g `name: Create Domain`

* id - 다른 task에서 이 task에 접근하기 위한 key. 
  e.g `id: ${{ tasks.root_domain }}`

* if - 현재 task를 수행할 지 말 지에 대한 condition 
  e.g. `if: ${{ tasks.my_domain.output.name }} == 'root'`

* uses - 어떤 python file 및 built-in module, 웹 api를 쓸 것인가

  e.g. `uses: "@modules/resources"`, `uses: ~/load_excel.py`, `uses: https://api.github.com`

* spec - 현재 task에서 사용하는 module에 대한 spec을 정의. spec은 사용하는 module에 따라 필드가 달라질 수 있다.

* output - 현재 task의 module을 수행 후 그 결과를 저장. 사용자가 수작업으로 정의하는 필드는 아님.

### spec 정리 - @module/resource 인 경우

> spec은 현재 task가 사용하는 module에 대한 spec이므로 module마다 사용할 field가 달라진다.

* resource_type - spaceone grpc 에서 사용하는 resource type
  e.g. `resource_type: identity.User`, `resource_type: plugin.Plugin`

* verb - 어떤 verb를 수행할 것인가.

  * 기본적으로는 read - read, create - create, update - update
  * read: null, create: get-endpoint, update: null

* data - spaceone grpc 에서 사용할 인자들

  ```
  spec:
    data:
    	name: admin
    	domain_id: domain-12341234
  ```

* matches - data의 어떤 field와 맞는 값을 쿼리하고 create or update 할 것인가.
  AND 연산을 할 것이고 사용할 data의 field들을 배열로서 선언한다. 
   현재는 단일 데이터에 대한 쿼리만 구상. string에 대한 배열만 구상.

  ```
  matches:
    - name
    - domain_id
  ```

### spec 정리 - @module/shell 인 경우

* run - 실행할 shell script

* ```
  tasks:
    - name: Update spacectl configure
      id: shell
      uses: "@modules/shell"
      spec:
      run: |
      	spacectl config set api_key ${{ tasks.my_domain_owner_token.output.access_token }}
  ```



### spec 정리 - @module/excel 인 경우

```
- uses: @module/excel
  spec:
    action: print
```

action: built-in module인 excel에 전달하고싶은 인자들에 대한 정의이다.

* action - excel 모듈이 어떤 작업을 수행하도록 할 것인지
  e.g. `action: print`,  `action: load`,  `action: append`
* file_path: 사용할 excel file path
  e.g.` file_path: ~/user_data.csv`



## Scenarios

### initialize

```yaml
var:
  my_domain_name: homeplus
  domain_owner_name: admin
  domain_owner_password: adminpassowrd

env:
  environment: dev

tasks:
  - name: Create Domain
    id: my_domain
    uses: "@modules/resource"
    spec:
      resource_type: identity.Domain
      data:
        name: ${{ var.my_domain_name }}
      matches:
        - name

  - name: Create Domain Owner
    id: my_domain_owner
    uses: "@modules/resource"
    spec:
      resource_type: identity.DomainOwner
      data:
        name: ${{ env.environment}}-${{ var.domain_owner_name }}
        password: ${{ env.environment}}-${{ var.domain_owner_password }}
        domain_id: ${{ tasks.my_domain.output.domain_id }}
      matches:
        - name
        - domain_id

  - name: Read user data from excel file
    id: excel_data
    uses: "@modules/excel" # 우리의 built-in의 modules/resource
    # uses: https://github.com/spaceone/dev ... .py 등등
    spec:
      action: load
      file_path: user_info.svc
      not_exists: error
      
  - name: Create admin user
    if: ${{ tasks.excel_data.user.type }} ) == 'admin'
    id: admin_user
    uses: "@modules/resource"
    spec:
      resource_type: identity.User
      data:
        name: stark
        domain_id: ${{ tasks.my_domain.output.domain_id }}
        description: my name is ${{ self.spec.data.name }}
        tags:
          created_by: ${{ self.name }}
      matches:
        - name
        - domain_id
```

### change phone

```yaml
tasks:
  - name: Update username
    if: normal_user
    uses: @modules/resource
    resource_type: identity.User
    spec:
      name: stark
      domain_id: domain-abcdefg
      phone: 010-1234-1234
      matches:
        - name
        - domain_id
```



## Issues

❓Read할 때와 Create할 때, Update 할 때 필드가 다른 애들은 어떻게 하는 지?

plugin.Plugin의 경우 list할 때에는 repository_id가 필요하지만, create할 때에는 repository_id가 필요없다.

list할 때에는 repository_id를 정의해야하는데, create할 때에는 repository_id 필드를 삭제해야한다.



❓update 시에 필드로 전할 것과 전하지 않을 것을 구별하는 방법은?

예를 들어 domain을 create 할 때에는 name이 필요한데, update할 때에는 name은 불가능하고, domain_id만 받는다.



⭕️list, create, update로는 작업할 수 없는 token issue나 supervisor publish 같은 것들은 어떻게 할 것인지?

resource의 spec에 verb 필드를 사용함으로써 override 하도록.



⭕️matches를 통해 parameter 자체로 전달될 것과, query parameter로 전달될 것의 분류는? => 다 그냥 parameter로

```
{
	"domain_id": task.spec["data"]["domain_id"],  # 이 필수 파라미터를 어떻게 설정할 것인가? query에 들어갈 지 root 파라미터로 들어갈 지?
	"query":{
		"filter": read_filter
	}
}
```



⭕️자신의 상황에 따라 self가 바뀜. 우리의 hierarchy와 완전 동일 하지는 않은 변수 접근

예를 들어 ${{ resources.excel_data }} 지만, manifest.resources.excel_data

${{ self.space.name }} 이지만, manifest.resources.admin_user.name

=>resource 단에서 check_value=> value가 ${{}}의형태가 존재하는지

=>${{}}가 존재한다면 다시 템플릿 적용

```python
get_dot_value({
	"self": self,
	"tasks": self.manifest.tasks,
	"env": self.manifest.env
	"var": self.manifest.var
})
```

