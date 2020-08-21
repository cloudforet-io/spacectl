# How to list resources with spacectl

> This guide assumes you set your spacectl configurations. If you didn't, we recommend you to read [docs/configuration.md](docs/configuration.md) and set your spacectl configurations.

You can list all resource which support `list` api. `table `, `json`, and `yaml` are available as an output format. 

**Note**: If you have no resource in your SpaceONE domain, `list` can show nothing and you might feel like it doens't work.

## Usage Examples

### Quick Start

```bash
# example: 2 ways simply list inventory.Server
$ spaceclt list identity.Domain # 1. Full name
$ spacectl list domain # 2. alias
```

### Pass some parameters

You can pass some parameters which are `text` or `json`.

```bash
# 1. text parameter
$ spacectl list server -p domain_id=domain-123abc123

# 2. json parameter like curl
$ spacectl list server -j '{"domain_id":"domain-123abc123"}'
```



