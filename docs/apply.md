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
| `<Task>.if`     | the conditional statement if the task will be executed or not. | `${{ var.my_name | quote }} == “SpaceONE”`                 | X            |
| `<Task>.id`     | The ID of the task.                                          | `my_domain`, `test_user`, `issued_token`                     | X            |
| `<Task>.uses`   | This determines what operation the task execution. If this use spacectl-built-in module, you can use @modules/MODULE_NAME annotation. | `@modules/resource`, `@modules/shell`                        | O            |
| `<Task>.spec`   | This is whole configuration of the operation, not the task itself,  mentioned in uses. | a dictionary                                                 | O            |
| `<Task>.output` | The output of the task. How to set output can be differ depending on which operation the task executed. | a dictionary or a list                                       | X            |


| :point_up:    | **if** evaluates statement, use jinja filter to make string |
|---------------|:------------------------|

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
| `<Task\>.spec.resource_type`    | Which resource type you’re applying                          | identity.User, repsitory.Repository             | O            |
| `<Task\>.spec.data`             | A dictionary which will be used as parameters when you create or update resources. | a dictionary                                    | X            |
| `<Task\>.spec.matches`          | Fields which will be used as parameters when you read resources. | a list. [“domain_id”, “name”]                   | X            |
| `<Task\>.spec.verb`             | Overrides default verbs to customize the execution.          | a dictionary. {“read”: None, “create”: "issue"} | X            |
| `<Task\>.spec.mode`             | How your apply process will be executed.                     | `DEFAULT`, `READ_ONLY`, `NO_UPDATE`, `EXEC`     | X            |
| `<Task\>.spec.output.template`          | Defines the format for the execution result. Supports `metadata` and `file` type. <br> In the `metadta` in the options, Get the metadata value of the specified `cloud service type` output using the value specified in table as it is. <br> If `file` is specified, If file is specified, the template yaml file in the path of  specified in options is read. | `metadata`<br>`file`    | X            |
| `<Task\>.spec.output.options.file`      | If `file` is specified in `output.template`, set the path to the yaml file to be used as template in file in options.                     |  template.yaml   | X            |
| `<Task\>.spec.output.options.metadata`  | If `metadata` is specified in `output.template`, Specifies the cloud service type with metadata to use as a template. The format is `<provider>`.`<cloud_service_group>`.`<cloud_service_type>` |  `aws.EC2.Volume` <br> `aws.DocumentDB.Cluster`   | X            |

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


## @modules/export-google-sheets

You can export the execution results to google sheets with @modules/export-google-sheets. How to use is as follows.

| **field**         | **description**                 | **examples**            | **is required** |
| ----------------- | ------------------------------- | ----------------------- | --------------- |
| `<Task>.spec.service_account_json` | This is a google account json file for accessing google sheets. The json file is available at https://console.cloud.google.com. | /Users/xx/google_account/service_account.json | O               |
| `<Task>.spec.sheet_id`             | The ID of google sheet to export | 1xk0wZHxfW9crcyOAJse_nY_Nd_30M5tlwP56wcwSD1A | O               |
| `<Task>.spec.data[].input`      | The list of data to be exported to the specified worksheet. This is a list of data to be exported to the specified sheet. <br> The data format is a list of the dictionary, the key of the dictionary is the header of data, and the value is recorded in the column. |  | O               |

### Example cases

This example is the YAML file was be used @module/resource to get EBS Volume data through the SpaceONE inventory API and export it to Google Sheets.

```yaml
var:
  service_account_json_path: '/Users/user/google_cloud/service_account.json'
  sheet_id: '1xk0wZHxfW9crcyOAJse_nY_Nd_30M5tlwP56wcwSD1A'
tasks:
  - name: EBS Volume
    id: ebs_volume
    uses: "@modules/resource"
    spec:
      resource_type: inventory.CloudService
      data:
        cloud_service_group: EC2
        cloud_service_type: Volume
      mode: EXEC
      verb:
        exec: list
      output:
        template: metadata
        options:
          metadata: "aws.EC2.Volume"
  - name: Export EBS Volume to Spread Sheets
    id: ebs_vol_export
    uses: "@modules/export-google-sheets"
    spec:
      service_account_json: ${{ var.service_account_json_path }}
      sheet_id: ${{ var.sheet_id }}
      data:
        - input: ${{ tasks.ebs_volume.output }}
```



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

