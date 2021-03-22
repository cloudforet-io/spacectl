# Getting Start Guide

- Through this guide, you can manage basic components of SpaceONE (identity/inventory)

- To setup spacectl you need refer  [docs/configuration.md](docs/configuration.md)



## Project


### create project group

```bash
# Creating project group in root tree
$ spacectl exec create identity.ProjectGroup -p name=test-project-group-03
---
created_at: '2021-03-22T01:22:04.399611Z'
created_by: user1@example.com
domain_id: domain-xxxxxxxxx
name: test-project-group-03
project_group_id: pg-xxxxxxxx

# Creating project group in level2 branch, Need to add parent_project_group_id
$ spacectl exec create identity.ProjectGroup -p name=test-group-group-lv2-01 -p parent_project_group_id=pg-xxxxxx
---
created_at: '2021-03-22T01:24:26.295558Z'
created_by: user1@example.com
domain_id: domain-xxxxxxxxx
name: test-group-group-lv2-01
parent_project_group_info:
  name: test-project-group-03
  project_group_id: pg-xxxxxxxxx
project_group_id: pg-xxxxxxxxx
```


### create project

```bash
# Creating project
$ spacectl exec create identity.Project -p name=test-project-01 -p project_group_id=pg-xxxxxxxxx
---
created_at: '2021-03-22T01:27:25.351967Z'
created_by: user1@example.com
domain_id: domain-xxxxxxxxx
name: test-project-01
project_group_info:
  name: test-project-group-01
  project_group_id: pg-xxxxxxxxx
project_id: project-xxxxxxxxx


```


### list projects group

```bash
# List all project groups
$ spacectl list identity.ProjectGroup
 project_group_id   | name                    | parent_project_group_info                                                | domain_id           | created_by        | created_at
--------------------+-------------------------+--------------------------------------------------------------------------+---------------------+-------------------+--------------------------
 pg-xxxxxxxxx    | test-group-group-lv2-01 | {'project_group_id': 'pg-xxxxxxxxx', 'name': 'test-project-group-03'} | domain-xxxxxxxxx | user1@example.com | 2021-03-22T01:24:26.295Z
 pg-xxxxxxxxx    | test-project-group-01   |                                                                          | domain-xxxxxxxxx | user1@example.com | 2021-03-19T09:34:57.592Z
 pg-xxxxxxxxx    | test-project-group-02   |                                                                          | domain-xxxxxxxxx | user1@example.com | 2021-03-19T09:36:00.942Z
 pg-xxxxxxxxx    | test-project-group-03   |                                                                          | domain-xxxxxxxxx | user1@example.com | 2021-03-22T01:22:04.399Z

 Count: 4 / 4

```



### list project

```bash
# List all projects
$ spacectl list identity.Project
 project_id           | name            | project_group         | project_group_id   | tags   | created_at
----------------------+-----------------+-----------------------+--------------------+--------+--------------------------
 project-xxxxxxxxx | test-project-01 | test-project-group-01 | pg-xxxxxxxxx    |        | 2021-03-22T01:27:25.351Z
 project-xxxxxxxxx | test-project-02 | test-project-group-02 | pg-xxxxxxxxx    |        | 2021-03-22T01:29:57.075Z

 Count: 2 / 2

# List projects from specified project group
$ spacectl list identity.Project -p project_group_id=pg-e487432ec820
 project_id           | name            | project_group         | project_group_id   | tags   | created_at
----------------------+-----------------+-----------------------+--------------------+--------+--------------------------
 project-xxxxxxxxx | test-project-01 | test-project-group-01 | pg-xxxxxxxxx    |        | 2021-03-22T01:27:25.351Z

 Count: 1 / 1
```



## User

- After creating user, role need to be binded to each user.
- Role should be existed before creating user.

### Create User

```bash
# Create LOCAL type user
$ spacectl exec create identity.User -p user_id=user2@example.com -p password=xxxxxxx -p name=williams -p backend=LOCAL
---
backend: LOCAL
created_at: '2021-03-22T01:45:24.582896Z'
domain_id: domain-xxxxxxx
language: en
name: williams
state: ENABLED
timezone: UTC
user_id: user2@example.com
user_type: USER
```


### List Role

```bash
# List all roles in domain
$ spacectl list identity.Role
 role_id           | name          | role_type   | policies                                                         | domain_id           | created_at
-------------------+---------------+-------------+------------------------------------------------------------------+---------------------+--------------------------
 role-xxxxxxxx | Domain Admin  | DOMAIN      | [{'policy_type': 'MANAGED', 'policy_id': 'policy-xxxxxxxx'}] | domain-xxxxxxxx | 2021-03-19T04:57:02.221Z
 role-xxxxxxxx | Project Admin | PROJECT     | [{'policy_type': 'MANAGED', 'policy_id': 'policy-xxxxxxxx'}] | domain-xxxxxxxx | 2021-03-19T04:57:02.107Z

 Count: 2 / 2

```

### Role binding to user

```bash
# To grand user domain admin permission
$ spacectl exec create identity.RoleBinding -p resource_type=identity.User -p resource_id=user2@example.com -p role_id=role-xxxxxxxx
---
created_at: '2021-03-22T02:04:58.376098Z'
domain_id: domain-4c23f4f97c8c
resource_id: user2@example.com
resource_type: identity.User
role_binding_id: rb-xxxxxxxx
role_info:
  name: Domain Admin
  role_id: role-xxxxxxxx
  role_type: DOMAIN

# To list user role binding status
$ spacectl list identity.RoleBinding
 role_binding_id   | resource_type   | resource_id       | role_info                                                                       | domain_id           | created_at
-------------------+-----------------+-------------------+---------------------------------------------------------------------------------+---------------------+--------------------------
 rb-xxxxxxxx   | identity.User   | user1@example.com | {'role_id': 'role-xxxxxxxx', 'name': 'Domain Admin', 'role_type': 'DOMAIN'} | domain-xxxxxxxx | 2021-03-19T04:57:02.314Z
 rb-xxxxxxxx   | identity.User   | user2@example.com | {'role_id': 'role-xxxxxxxx', 'name': 'Domain Admin', 'role_type': 'DOMAIN'} | domain-xxxxxxxx | 2021-03-22T02:04:58.376Z

 Count: 2 / 2
```

### List User

```bash
$ spacectl list identity.User
 user_id           | state   | user_type   | backend   | language   | timezone   | created_at               | domain_id           | name
-------------------+---------+-------------+-----------+------------+------------+--------------------------+---------------------+----------
 user1@example.com | ENABLED | USER        | LOCAL     | en         | UTC        | 2021-03-19T04:57:01.087Z | domain-xxxxxxxx |
 user2@example.com | ENABLED | USER        | LOCAL     | en         | UTC        | 2021-03-22T01:45:24.582Z | domain-xxxxxxxx | williams

 Count: 2 / 2
```


## Service Account

### Create Service Account & Secret

- Service Account & Secret need to create together

```bash
# Create service account
$ spacectl exec create service_account -p name=aws-service-test-account -j '{"data": {"account_id": "xxxxxxxx"}}' -p project_id=project-xxxxxxxx -p provider=aws
---
created_at: '2021-03-22T03:17:44.041313Z'
data:
  account_id: 'xxxxxxxx'
domain_id: domain-xxxxxxxx
name: aws-service-test-account
project_info:
  name: test-project-02
  project_id: project-xxxxxxxx
provider: aws
service_account_id: sa-xxxxxxxx


# Create Secret
$ spacectl exec create secret.Secret -p name=aws-service-test-account -p schema=aws_access_key -p project_id=project-xxxxxxxx -p secret_type=CREDENTIALS -p service_account_id=sa-xxxxxxxx -j '{"data": {"provider":"aws", "aws_access_key_id": "xxxxxxxx","aws_secret_access_key":"xxxxxxxx"}}'

---
created_at: '2021-03-22T03:31:08.888473Z'
domain_id: domain-xxxxxxxx
name: aws-service-test-account
project_id: project-xxxxxxxx
provider: aws
schema: aws_access_key
secret_id: secret-xxxxxxxx
secret_type: CREDENTIALS
service_account_id: sa-xxxxxxxx
```

### List Service Account & Secrets

```bash
# List all secret in domain
$ spacectl list secret
 secret_id           | name                     | secret_type   | schema         | provider   | service_account_id   | project_id           | domain_id           | created_at
---------------------+--------------------------+---------------+----------------+------------+----------------------+----------------------+---------------------+--------------------------
 secret-xxxxxxxx | aws-service-test-account | CREDENTIALS   | aws_access_key | aws        | sa-xxxxxxxx      | project-xxxxxxxx | domain-xxxxxxxx | 2021-03-22T03:31:08.888Z

 Count: 1 / 1
 # List all service account in domain
$ spacectl list service_account
 service_account_id   | name                     | data                           | provider   | project_info                                                      | domain_id           | created_at
----------------------+--------------------------+--------------------------------+------------+-------------------------------------------------------------------+---------------------+--------------------------
 sa-xxxxxxxx      | aws-service-test-account | {'account_id': 'xxxxxxxx'} | aws        | {'project_id': 'project-xxxxxxxx', 'name': 'test-project-02'} | domain-xxxxxxxx | 2021-03-22T03:17:44.041Z

 Count: 1 / 1
```



## Plugins(Collector)


### Create Plugins




### List Plugins





## Cloud Services





