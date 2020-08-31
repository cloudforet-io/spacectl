# spacectl apply - Manage your spaceone resources easily.

## Quick start

After the initial configuration for spacectl, you can apply the below manifest.

```yaml
# quickstart.yaml
var:
  foo: bar
tasks:
  - name: Create or Update a domain
    id: foo_domain
    uses: "@modules/resource"
    spec:
      resource_type: identity.Domain
      data:
        name: ${{ var.foo }}-domain
      matches:
        - name
      mode: NO_UPDATE
  - name: Greet to the domain
    id: script
    uses: "@modules/shell"
    spec:
      run: |
        echo "There is a domain (${{ tasks.foos_domain.output.domain_id}})."
```

```bash
$ spacectl apply -f quickstart.yaml
```

You will create a new domain named `bar` and can see its `domain_id`.

## A simple structure

| **key** | **description**                                              |
| ------- | ------------------------------------------------------------ |
| `var`   | declare variables to use in manifests and tasks              |
| `env`   | like var, environment variables which includes host env and additional env which are inputed. |
| `tasks` | Tasks which will be executed in the manifest.Its structure is like github action manifest or ansible playbook.This covers the real process of the manifest. |



## Tasks

Tasks is a list which contains the configuration of each Task. Task is written as \<Task> in the following table.

| **field**       | **description**                                              | **examples**                                                 | **required** |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------ |
| `<Task>.name`   | The name of the task.                                        | `Create a Domain`, `Temporary Task`, …                       | X            |
| `<Task>.if`     | the conditional statement if the task will be executed or not. | `${{ var.my_name }} == “SpaceONE”`, `${{ tasks.example.output | len }}< 1` |              |
| `<Task>.id`     | The ID of the task.                                          | `my_domain`, `test_user`, `issued_token`                     | X            |
| `<Task>.uses`   | This determines what operation the task execution. If this use spacectl-built-in module, you can use @modules/MODULE_NAME annotation. | `@modules/resource`, `@modules/shell`                        | O            |
| `<Task>.spec`   | This is whole configuration of the operation, not the task itself,  mentioned in uses. | a dictionary                                                 | O            |
| `<Task>.output` | The output of the task. How to set output can be differ depending on which operation the task executed. | a dictionary or a list                                       | X            |



## @module/resource

you can use `@module/resource` for querying, creating, updating SpaceONE resources. 

By default, spacectl apply will execute list api to read, create api to create, update api to update. 

### Mode

Mode means how you will call APIs

* (Default) DEFAULT: Read => create or update
* READ_ONLY: Read and the `Task` will be completed.
* NO_UPDATE: Read then create a new resource if the resources doesn't exist.
* EXEC: Just execute an API configured in `<Task>.spec.verb.exec`.

### Verb types

- read - Query resources with the fields in \<Task\>.spec.data which are listed in \<Task\>.spec.matches.
- create - If there is no resources queried, spacectl will create a new resource.
- update - If there is a resource queried, spacectl will update the resource.
- exec - execute a configured API.

| **field**                    | **description**                                              | **examples**                                    | **required** |
| ---------------------------- | ------------------------------------------------------------ | ----------------------------------------------- | ------------ |
| `<Task\>.spec.resource_type` | Which resource type you’re applying                          | identity.User, repsitory.Repository             | O            |
| `<Task\>.spec.data`          | A dictionary which will be used as parameters when you create or update resources. | a dictionary                                    | X            |
| `<Task\>.spec.matches`       | Fields which will be used as parameters when you read resources. | a list. [“domain_id”, “name”]                   | X            |
| `<Task\>.spec.verb`          | Overrides default verbs to customize the execution.          | a dictionary. {“read”: None, “create”: "issue"} | X            |
| `<Task\>.spec.mode`          | How your apply process will be executed.                     | `DEFAULT`, `READ_ONLY`, `NO_UPDATE`, `EXEC`     | X            |

### Example cases

#### simple `DEFAULT` mode

```yaml
var:
  domain_name: foo
tasks:
  - name: Create or Update a Domain
    id: foo_user
    uses: "@modules/resource"
    spec:
      resource_type: identity.Domain
      data:
        name: ${{ var.domain_name }}
#      You can comment out mode because DEFAULT is the default value of mode.
#      mode: DEFAULT
      matches:
        - name
```

#### simple `READ_ONLY` mode - Read once.

```yaml
# same as DEFAULT mode execpt for tasks.<id>.spec.mode
...
tasks:
  - ...
    spec:
      mode: READ_ONLY
      ...
```

#### simple `NO_UPDATE` mode - Read then create or ignore updaing.

`NO_UPDATE` doesn't update if a resource exists.

```yaml
# same as DEFAULT mode execpt for tasks.<id>.spec.mode
...
tasks:
  - ...
    spec:
      mode: READ_ONLY
      ...
```

#### simple `EXEC` mode - Execute an API once.

Configure an API name in `tasks.<id>.spec.verb.exec` then `spacectl` will execute the api with data as params.

```yaml
var:
  domain_name: foo
tasks:
  - name: Execute a task to create a Domain
    id: foo_user
    uses: "@modules/resource"
    spec:
      resource_type: identity.Domain
      data:
        name: ${{ var.domain_name }}
      mode: EXEC
      verb:
        exec: create
```



## @modules/shell

You can run shell script with @modules/shell. This can look like Github action.

| **field**         | **description**                 | **examples**            | **is required** |
| ----------------- | ------------------------------- | ----------------------- | --------------- |
| `<Task>.spec.run` | Defines the script you will run | curl https://google.com | O               |



## Options

* `-f`, `--file-path` - Manifest file paths like `kubectl apply -f `
  * Multiple manifests are available and they will be overidden and appended by order.
  * examples
    * `spacectl apply -f manifest.yaml`
    * `spacectl apply -f env.yaml -f var.yaml -f manifest.yaml`
    * `spacectl apply -f manifest_1.yaml -f manifest_2.yaml`
* `-o`, `--output` - Output format (e.g. `json`,  `yaml` ). Output contains `var` and `tasks`.
* `-e`, -`--env` - Configure envrionmental. This can override `env` of manifests from the `-f` option.
*  `--set` - Configure variables. This can override `var` of manifests from the `-f` option.
* `--no-progress` - omit the output of each progress.