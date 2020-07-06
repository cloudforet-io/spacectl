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
    ```

- Set up spacectl endpoints
    ```commandline
    spacectl endpoint init
    ```

### Discovering builtin services:
The following commands listing all spacectl APIs. 
Run it like this:

```commandline
spacectl api-resources
```

## Examples
Case 1 - List Servers:
```commandline
spacectl ls server
```

Case 2 - Create Project Group:
```commandline
spacectl exec create project_group -p name=<project_group_name>
```

&nbsp;  

## Advanced Guides

## Configuration
- Namespace
- Config Settings

## Endpoint Settings
- Environment
- Manage Endpoints

### Command Details
- get: Show details of a specific resource
- list: Display one or many resources
- stat: Querying statistics for resources
- exec: Execute a method to resource
- template: Manage resource templates