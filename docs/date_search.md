# How to list resources with date search query

> This guide assumes you set your spacectl configurations. If you didn't, we recommend you to read [docs/configuration.md](docs/configuration.md) and set your spacectl configurations.

You can filter specific resources which has complex data format.

## Search EC2 which was created at specific date range

Example 1.

Query resources which is created from 2022-04-01 to 2022-04-02
~~~
 spacectl list server -j '{"query": {"filter": [{"k": "created_at", "v": "2022-04-01", "o": "gt"},{"k": "created_at", "v": "2022-04-02", "o": "lt"}]}}' -c server_id,name,provider,created_at
 server_id           | name         | provider   | created_at
---------------------+--------------+------------+--------------------------
 server-0088491fbc8e | spot-k8s-dev | aws        | 2022-04-01T11:00:31.016Z
 server-2102ec2cbb6e | spot-k8s-dev | aws        | 2022-04-01T11:00:30.970Z
~~~

Example 2.

Query resources which is deleted from 2022-04-01 to 2022-04-02.

If you want to search deleted resource, you have to add a ***state*** field.

~~~
spacectl list server -j '{"query": {"filter": [{"k": "deleted_at", "v": "2022-04-01", "o": "gt"},{"k": "deleted_at", "v": "2022-04-02", "o": "lt"},{"k": "state", "v": "DELETED", "o": "eq"}]}}' -c server_id,name,provider,created_at,deleted_at
 server_id           | name                    | provider   | created_at               | deleted_at
---------------------+-------------------------+------------+--------------------------+--------------------------
 server-af9929fc39dc |                         | aws        | 2022-04-01T18:00:36.721Z | 2022-04-01T22:01:01.227Z
 server-8626317db2d3 |                         | aws        | 2022-04-01T10:00:29.504Z | 2022-04-01T13:01:22.393Z
 server-7cf2b6d9a870 |                         | aws        | 2022-04-01T09:00:55.720Z | 2022-04-01T13:01:22.393Z
 server-78070069840d |                         | aws        | 2022-04-01T08:00:59.569Z | 2022-04-01T13:01:22.393Z
 server-65c00a40b5d3 |                         | aws        | 2022-04-01T10:00:29.568Z | 2022-04-01T13:01:22.393Z
 server-3d23be7e742a |                         | aws        | 2022-04-01T10:00:29.537Z | 2022-04-01T13:01:22.393Z
 server-0455ff745f93 |                         | aws        | 2022-04-01T09:00:56.242Z | 2022-04-01T13:01:22.393Z
 ~~~
