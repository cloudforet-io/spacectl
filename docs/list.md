# How to list resources with spacectl

> This guide assumes you set your spacectl configurations. If you didn't, we recommend you to read [docs/configuration.md](docs/configuration.md) and set your spacectl configurations.

You can list all resource which support `list` api. `table `, `json`, and `yaml` are available as an output format. 

**Note**: If you have no resource in your SpaceONE domain, `list` can show nothing and you might feel like it doens't work.

## Usage Examples

### Quick Start

```bash
# example: 2 ways simply list inventory.Server
$ spaceclt list identity.Domain # 1. Full name
 domain_id           | name   | state   | plugin_id  ...
 domain-123abc123    | umi0410| ENABLED |            ...
$ spacectl list domain # 2. alias
 domain_id           | name   | state   | plugin_id  ...
 domain-123abc123    | umi0410| ENABLED |            ...
```

### Pass some parameters

You can pass some parameters which are `text` or `json`. If you are in a case that you have to pass a `google.protobuf.Struct` parameter, you can use `-j` and pass json data.

```bash
# 1. text parameter
$ spacectl list server -p domain_id=domain-123abc123
 server_id         | name    | provider ...
 server-123abc123  | foo     | aws ...
 ...
 
# 2. json parameter like curl
$ spacectl list server -j '{"domain_id":"domain-123abc123"}'
 server_id         | name    | provider ...
 server-123abc123  | foo     | aws ...
 ...
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

**quiet** - You can get only the value of selected column. You should specify only one column. Also, you can pipe some commands.

```bash
$ spacectl list domain -p name=<YOUR_DOMAIN_NAME> -o quiet -c domain_id
domain-123abc123

# example to use quiet output as a parameter
$ spacectl list server -p domain_id=$(spacectl list domain -p name=<YOUR_DOMAIN_NAME> -o quiet -c domain_id)
```



### Speficy columns

You can specify columns which you want to get in the api result with `-c`. Multiple columns are seperated by comma(`,`) without space.

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
```