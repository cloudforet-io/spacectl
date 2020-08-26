# How to configure spacectl

This doc covers how to configure spaceone api endpoints and environements of spacectl.

## Config Concept

* environment
  * each environment is isolated each other.
  * this is a unit of spaceconfig
  * this includes api_key, endpoints
* api_key - an API Key which spacectl will use
* endpoints - all endpoints which spacectl will use.

## Quick Start

### Sample - using `-f` option to import configuration from a file

This is just a sample for my local environment. I installed SpaceONE by helm3 on minikube and port-forwarded each service. So I can access eache microservice through its name and port number 50051. For example, if a microservice is `identity`, I can access it through `grpc://identity:50051`  on my local.

```yaml
# default.yml

# You should change the api_key. This is just a sample api_key
api_key: api_key: xxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx

endpoints:
  config: grpc://config:50051
  identity: grpc://identity:50051
  inventory: grpc://inventory:50051
  monitoring: grpc://monitoring:50051
  plugin: grpc://plugin:50051
  repository: grpc://repository:50051
  secret: grpc://secret:50051
  statistics: grpc://statistics:50051
```

```bash
$ spacectl config init -f default.yaml
Environment [default]:
```



### Sample - input values

```bash
$ spacectl config init
Environment [default]:

$ spacectl config set api_key api_key: xxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx

$ spacectl config endpoint add config grpc://config:50051
$ spacectl config endpoint add identity grpc://identity:50051
$ spacectl config endpoint add inventory grpc://inventory:50051

... # config other endpoints in the same way
```



### Let's check out if you configured well

```bash
# get the version of a microservice
$ spacectl exec get_version repository.ServerInfo
---
version: 1.2.1

# get all available apis
$ spacectl api_resources
... 
```



## Manage endpoints

We covered how to add endpoints. Let's edit endpoints now. We don't support edit command so you should delete an existing endpoint and create a new endpoint.

```bash
$ spacectl config endpoint show
 Service    | Endpoint
------------+-------------------------
 config     | grpc://config:50051
 identity   | grpc://identity:50051
 ...
 
$ spacectl config endpoint remove identity
$ spacectl config endpoint add identity grpc://spaceship:50051
$ spacectl config endpoint show
 Service    | Endpoint
------------+-------------------------
 config     | grpc://config:50051
 identity   | grpc://spacecship:50051
 ...
```

## Other details

### switch the environment

```bash
# You can see help message
$ spacectl config environment --help
$ spacectl config environment
default
helm-root (current)

$ spacectl config environment -s default
Switched to 'default' environment.
```

