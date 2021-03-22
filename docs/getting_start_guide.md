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


### Create User




### List User






## Service Account



### Create Service Account






### List Service Account





## Plugins(Collector)


### Create Plugins




### List Plugins





## Cloud Services





