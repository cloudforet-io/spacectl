# Execute any spaceone api with `exec`

You can execute any spaceone grpc api with `exec`. The arguemtns are like these. If you call spacectl built-in API like `get`, `list`and  `stat`, you can just use those command. However, you should use `exec` command to call other API.

* verb - an api name to execute. (e.g `get`, `issue`, `get_versions`, `Check`)
* resource - the type of resource to execute the verb. This can be full name resources or its alias. (e.g. `identity.User`, `inventory.Server`, `identity.Health`)
* options - options for the command `exec`
  * `-p`: text parameter, `-j`: json parameter, `-f`: yaml file parameter
  * `-v`: api version to execute
  * `o`: output format (e.g. `table`, `json`, `yaml`)

## Quick Start

### Health check

SpaceONE has a health check feature. You can find its details out with `spacectl api_resources`.

```bash
$ spacectl exec Check identity.Health
---
status: SERVING
```

### spacectl built-in API

you can call built-in api by either its command or `exec`. But the default output format of `exec` command is `yaml`.

```bash
# these 2 ways are similar
$ spacectl exec list identity.Domain -o yaml
$ spacectl list identity.Domain -o yaml
```

### Other API

If you want to call API which is not a spacectl built-in API, you should use `exec` command.

```bash
# example: create a project_group
$ spacectl exec create identity.ProjectGroup -p name=foobar -p domain_id=domain-123abc123
---
name: foobar
project_group_id: pg-123abc123
...

# example: call list_plugins of plugin.Supervisor
$ spacectl exec list_plugins plugin.Supervisor -p domain_id=domain-123abc123
---
results:
- endpoint: grpc://xxx.xxx.svc.cluster.local:50051
  endpoints:
  - grpc://xxx.xxx.svc.cluster.local:50051
  plugin_id: plugin-123abc123
  state: ACTIVE
  supervisor_id: supervisor-123abc123
  ...

# example: you can also use json parameter
$ spacectl exec list_plugins plugin.Supervisor -j '{"domain_id":"domain-123abc123"}'
---
results:
- endpoint: grpc://xxx.xxx.svc.cluster.local:50051
  endpoints:
  - grpc://xxx.xxx.svc.cluster.local:50051
  plugin_id: plugin-123abc123
  state: ACTIVE
  supervisor_id: supervisor-123abc123
  ...
  
# example: you can also print in json format or table format
$ spacectl exec list_plugins plugin.Supervisor -j '{"domain_id":"domain-123abc123"}' -o json
$ spacectl exec list_plugins plugin.Supervisor -j '{"domain_id":"domain-123abc123"}' -o table
```

