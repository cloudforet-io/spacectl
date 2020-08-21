<h1 align="center">spacectl</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <img width="245" src="https://user-images.githubusercontent.com/35549653/76694897-de236300-66bb-11ea-9ace-b9edde9c12da.png">  
  <p> 
   <br>
    <img  alt="Version"  src="https://img.shields.io/badge/version-0.9.0-blue.svg?cacheSeconds=2592000"  />    
    <a  href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank">  
        <img  alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg"  />  
    </a> 
    </p> 
</div>    

# Getting Started with spacectl
The SpaceONE command-line tool, spacectl, allows you to run commands against resources managed by SpaceONE.     

API Reference: https://spaceone-dev.gitbook.io/spaceone-apis

# Install and Set Up spacectl
Install the latest release with the command from PyPI using pip:
```commandline
pip install spacectl
```

There are a few variants on getting helps. 
A list of global options and supported commands are available with --help:
```commandline
spacectl --help
```

## Accessing for the first time with spacectl:

The following commands run spacectl to set your own configurations and endpoints. 
It handles setting the environments, authenticating and targets. 
Run it like these:

- Set up spacectl configuration
    ```commandline
    spacectl config init # input environment on shell
    spacectl config set api_key <api_key>
    spacectl config endpoint add <service> <endpoint>
    ```
    
- (OR) Import a configuration file which you downloaded at SpaceONE console
    ```commandline
    spacectl config init -f <import_file>
    ```

The <import_file> looks like

```
api_key: xxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxx
domain_id: domain-123asd123
endpoints:
  ...
  identity: grpc://identity:50051
  inventory: grpc://inventory:50051
  plugin: grpc://plugin:50051
  repository: grpc://repository:50051
  secret: grpc://secret:50051
```

if you want to see a sample configuration file, try [examples/configuration.yaml](examples/configuration.yaml).

### Discovering builtin services:

The following commands list all available spacectl APIs. 
Run it like this:

```commandline
spacectl api-resources
```

# Examples
### Case 1: List Servers:
```commandline
spacectl list server -p domain_id=<domain_id>
```

### Case 2: Create Project Group:
```commandline
spacectl exec create project_group -p domain_id=<domain_id> -p name=<project_group_name>
```

# Advanced Guides

## Command Details and Guides
- get: Show details of a specific resource
- [list](docs/list.md): Display one or many resources

- [apply](docs/apply.md) : Get, list, create or update various resources and execute other tasks
- stat: Querying statistics for resources
- [exec](docs/exec.md): Execute a method to resource
- template: Manage resource templates

## Configuration Details

The following details are documented in [docs/configuration.md](docs/configuration.md)

- Config Concept
- Quick Start
- Manage Endpoints
- Switch the Environment