# How to list resources with spacectl

> This guide assumes you set your spacectl configurations. If you didn't, we recommend you to read [docs/configuration.md](docs/configuration.md) and set your spacectl configurations.

You can list all resource which support `list` api. `table `, `json`, `yaml `, and `csv` are available as an output format. 

**Note**: If you have no resource in your SpaceONE domain, `list` can show nothing and you might feel like it doens't work.

## Usage Examples

### Quick Start

```bash
# example: 2 ways simply list inventory.Server

$ spaceclt list identity.Domain     # 1. Full name
 domain_id           | name   | state   | plugin_id  | ...
---------------------+--------+---------+------------+-----
 domain-123abc123    | umi0410| ENABLED |            | ...

$ spacectl list domain              # 2. alias
 domain_id           | name   | state   | plugin_id  ...
---------------------+--------+---------+-----------
 domain-123abc123    | umi0410| ENABLED |            ...
```

### Pass some parameters

You can pass some parameters which are `text` or `json` or `yaml`. If you are in a case that you have to pass a `google.protobuf.Struct` parameter, you can use `-j` and pass json data.

```bash
# 1. text parameter
$ spacectl list server -p project_id=project-123abc123
 server_id         | name    | provider | ...
-------------------+---------+----------+----
 server-123abc123  | foo     | aws      | ...
 ...
 
# 2. json parameter like curl
$ spacectl list server -j '{"project_id":"project-123abc123"}'
 server_id         | name    | provider | ...
-------------------+---------+----------+----
 server-123abc123  | foo     | aws      | ...
 ...

# 3. parameter from yaml file
$ spacectl list server -f <yaml_file>
 server_id         | name    | provider | ...
-------------------+---------+----------+----
 server-123abc123  | foo     | aws      | ...
 ...
```

**yaml example**
```yaml
---
project_id: project-123abc123
```


### Various Output Format

**table** - the default output format. This is introduced above.

**json**

```bash
$ spacectl list domain -o json
{
    "results": [
        {
            "domain_id": "domain-123abc123",
           	...
        }
    ],
    "total_count": 1
}
```

**yaml** 

```bash
$ spacectl list domain -o yaml
---
results:
- domain_id: domain-123abc123
  ...
total_count: 1
```

**csv**

```bash
$ spacectl list domain -o csv
domain_id, ...
domain-123abc123, ...
```

**quiet** - You can get only the value of selected column. You should specify only one column. Also, you can pipe some commands.

```bash
$ spacectl list domain -p name=<YOUR_DOMAIN_NAME> -o quiet -c domain_id
domain-123abc123

# example to use quiet output as a parameter
$ spacectl list server -p domain_id=$(spacectl list domain -p name=<YOUR_DOMAIN_NAME> -o quiet -c domain_id)
```



### Specify columns

You can specify columns which you want to get in the api result with `-c`. Multiple columns are separated by comma(`,`) without space.

```bash
# single column
$ spacectl list domain -c domain_id
 domain_id
---------------------
 domain-123abc123

# multiple columns
$ spacectl list domain -c domain_id,name,state
 domain_id        | name       | state
------------------+------------+---------
 domain-123abc123 | umi0410    | ENABLED

# display data over 1 depth
$ spacectl list domain -c domain_id,name,plugin_info.plugin_id,plugin_info.version,plugin_info.options.auth_type
 domain_id        | name       | plugin_info.plugin_id | plugin_info.version | plugin_info.options.auth_type
------------------+------------+-----------------------+---------------------+--------------------------------
 domain-123abc123 | umi0410    | plugin-123abc123      | 1.1                 | google_oauth2

# column alias with Quotation Marks
$ spacectl list domain -c 'domain_id,name,plugin_info.plugin_id|Plugin ID,plugin_info.version|Version'
 domain_id        | name       | Plugin ID         | Version
------------------+------------+-------------------+-----------
 domain-123abc123 | umi0410    | plugin-123abc123  | 1.2

# minimal fields
$ spacectl list domain --minimal 
 domain_id        | name       | state
------------------+------------+---------
 domain-123abc123 | umi0410    | ENABLED

# all fields
$ spacectl list domain --all
domain_id         | name    | state    | config          | tags  | plugin_info | created_at | deleted_at
------------------+---------+----------+-----------------+-------+-------------+------------+-------------
 domain-123abc123 | umi0410 | ENABLED  | {}              | ...   | ...         | ...        | ...
 
```

### Sorting results
You can sort the results via the `-s [-]<key>` option.
```bash
# asending
$ spacectl list server -c server_id,data.hardware.core,data.hardware.memory -s data.hardware.core
 server_id     |   data.hardware.core |   data.hardware.memory
---------------+----------------------+------------------------
 server-123abc |                    1 |                  2
 server-456abc |                    1 |                  4
 server-789abc |                    2 |                  4
 server-123def |                    4 |                  8
 server-456def |                    4 |                  12
 server-789def |                    8 |                  16

# desending
$ spacectl list server -c server_id,data.hardware.core,data.hardware.memory -s -data.hardware.core
 server_id     |   data.hardware.core |   data.hardware.memory
---------------+----------------------+------------------------
 server-789def |                    8 |                  16
 server-456def |                    4 |                  12
 server-123def |                    4 |                  8
 server-789abc |                    2 |                  4
 server-456abc |                    1 |                  4 
 server-123abc |                    1 |                  2
```

### Pagination
You can specify the number of results with the `-l` option.
```bash
$ spacectl list server -l 5
 server_id     | name   | instance_type   |   core |   memory | az   
---------------+--------+-----------------+--------+----------+-----
 server-123abc |        | t3.small        |      2 |        2 | ...
 server-456abc |        | t3.small        |      2 |        2 | ...
 server-789abc |        | r5.large        |      2 |       16 | ...
 server-123def |        | t2.micro        |      1 |        1 | ...
 server-456dev |        | t3.small        |      2 |        2 | ...

 Count: 5 / 79
```