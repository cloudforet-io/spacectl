# spacectl apply - Manage your spaceone resources easily.

## Quick start

After the initial configuration for spacectl, you can apply the below manifest.

```yaml
# quickstart.yaml
var:
  foo: bar
tasks:
  - name: Create a domain
    id: foos_domain
    uses: "@modules/resource"
    spec:
      resource_type: identity.Domain
      data:
        name: ${{ var.foo }}-domain
      matches:
        - name
      verb:  # skip updating
        update:
  - name: Greet to the domain
    id: script
    uses: "@modules/shell"
    spec:
      run: |
        echo "a domain (${{ tasks.foos_domain.output.domain_id}}) has been created!"
```

```bash
$ spacectl apply -f quickstart.yaml
```

You will create a new domain named `bar` and can see its `domain_id`.

## A simple structure

| **key** | **description**                                              |
| ------- | ------------------------------------------------------------ |
| var     | declare variables to use in manifests and tasks              |
| env     | like var, environment variables which includes host env and additional env which are inputed. |
| tasks   | Tasks which will be executed in the manifest.Its structure is like github action manifest or ansible playbook.This covers the real process of the manifest. |



## Tasks

Tasks is a list which contains the configuration of each Task. Task is written as <Task> in the following table.

| **field**     | **description**                                              | **examples**                                                 | **required** |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------ |
| <Task>.name   | The name of the task.                                        | Create a Domain, Temporary Task, …                           | X            |
| <Task>.if     | the conditional statement if the task will be executed or not. | ${{ var.my_name }} == “SpaceONE”, ${{ tasks.example.output.read_length < 1 |              |
| <Task>.id     | The ID of the task.                                          | my_domain, test_user, issued_token                           | X            |
| <Task>.uses   | This determines what operation the task execution. If this use spacectl-built-in module, you can use @modules/MODULE_NAME annotation. | @modules/resource, @modules/shell                            | O            |
| <Task>.spec   | This is whole configuration of the operation, not the task itself,  mentioned in uses. | a dictionary                                                 | O            |
| <Task>.output | The output of the task. How to set output can be differ depending on which operation the task executed. | a dictionary or a list                                       | X            |

## @module/resource

you can use @module/resource for querying, creating, updating SpaceONE resources. 

By default, spacectl apply will execute list api to read, create api to create, update api to update. 

### Verbs

- read - Query resources with the fields in <Task>.spec.data which are listed in <Task>.spec.matches.
- create - If there is no resources queried, spacectl will create a new resource.
- update - If there is a resource queried, spacectl will update the resource.

If you have some resources which should override those default apis( list,  create, update), you can configure those in <Task>.spec.verbs.

- case 1. set verb read as None - skips reading and creates resource. No update.
- case 2. set verb update as None - if there is a queried resource, skips updating. No create.
- case 3. set verb read as None and create as issue - if you’re applying an identity.Token , you will skip reading and execute issue as a create verb.

| **field**                 | **description**                                              | **examples**                                    | **required** |
| ------------------------- | ------------------------------------------------------------ | ----------------------------------------------- | ------------ |
| <Task>.spec.resource_type | Which resource type you’re applying                          | identity.User, repsitory.Repository             | O            |
| <Task>.spec.data          | A dictionary which will be used as parameters when you create or update resources. | a dictionary                                    | X            |
| <Task>.spec.matches       | Fields which will be used as parameters when you read resources. | a list. [“domain_id”, “name”]                   | X            |
| <Task>.spec.verb          | Overrides default verbs to customize the execution.          | a dictionary. {“read”: None, “create”: "issue"} | X            |

## @modules/shell

You can run shell script with @modules/shell. This can look like Github action.

| **field**       | **description**                 | **examples**            | **is required** |
| --------------- | ------------------------------- | ----------------------- | --------------- |
| <Task>.spec.run | Defines the script you will run | curl https://google.com | O               |