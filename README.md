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

The following commands run spacectl to set own configurations and endpoints. 
It handles setting the environments, authenticating and targets. 
Run it like this:

- Set up spacectl configuration
    ```commandline
    spacectl config init
    spacectl config set api_key <api_key>
    spacectl config set domain_id <your domain_id>
    spacectl config endpoint add <service> <endpoint>
    ```

- (OR) Import configuration file which was downloaded at SpaceONE console
    ```commandline
    spacectl config init -f <import_file>
    ```

The <import_file> looks like

```
api_key: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXQiOiJBUElfS0VZIiwidXNlcl90eXBlIjoiVVNFUiIsImRpZCI6ImRvbWFpbi1lOTFiNGY1ODY0M2UiLCJhdWQiOiJzdXBlcnZpc29yIiwiaWF0IjoxNTk3MTkwODg1LCJrZXkiOiI0YmVhMGMxOGEzZGM0NDUwYWM0ZGQ5ZDkxMWMxMzUyMCIsInZlciI6IjIwMjAtMDMtMDQifQ.P9a_ZGm3uPX9yaxg9WD2DXRoZGYLu5xnvkpXbnalTm63BMWO19F2rIM9DW3JRaIQxeT7qpy9eCtBzyGWmlfiFoYG9kQ6Wzj46Ml9IqhYGEfCIdyFDx4j_u6PHCB81fu9i0gPbRFhOvGVKlnueM6k4TPfB7m09o34NY0A1XtyFYqNnrfHES73p_NmasX41BDNCgPIVYjSV6Ts_qno24r7hPLsYbVwuXPs9exGtnl0uK9zEEol00XX2llIRx6OBWx5uJ-7kFAJMIZmFKXgNHulfp_BbBJZj2JjWFHkQJ47EWMZTZzdpjHS2QZyRXGXaU2Bx6Zd9MTeh9ojCGQsWSJYKw
domain_id: domain-e91b4f58643e
endpoints:
  identity: grpc://identity:50051
  inventory: grpc://inventory:50051
  plugin: grpc://plugin:50051
  repository: grpc://repository:50051
  secret: grpc://secret:50051
```

### Discovering builtin services:
The following commands listing all spacectl APIs. 
Run it like this:

```commandline
spacectl api-resources
```

# Examples
### Case 1: List Servers:
```commandline
spacectl list server
```

### Case 2: Create Project Group:
```commandline
spacectl exec create project_group -p name=<project_group_name>
```

# Advanced Guides

## Command Details and Guides
- get: Show details of a specific resource
- list: Display one or many resources

- [apply](https://github.com/spaceone-dev/spacectl/blob/master/docs/apply.md) : Get, list, create or update various resources and execute other tasks
- stat: Querying statistics for resources
- exec: Execute a method to resource
- template: Manage resource templates

## Configuration

- Config Settings
- Manage Endpoints
- Switch the Environment