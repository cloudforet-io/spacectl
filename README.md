# Install and Set Up spacectl
The SpaceONE command-line tool, spacectl, allows you to run commands against resources managed by SpaceONE.     

API Reference: https://spaceone-dev.gitbook.io/spaceone-apis

## Getting Started
spacectl can be installed from PyPI using pip:
```commandline
pip install spacectl
```

There are a few variants on getting help. A list of global options and supported commands is shown with --help:
```commandline
spacectl --help
```

Following steps for first time user:
```commandline
spacectl config init
```

```commandline
spacectl endpoint init
```

Type following commands if you want to check API spec:
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

## Advanced Guides
### Configuration
- Namespace
- Config Settings

### Endpoint Settings
- Environment
- Manage Endpoints

### Command Details
- get: Show details of a specific resource
- list: Display one or many resources
- stat: Querying statistics for resources
- exec: Execute a method to resource
- template: Manage resource templates

