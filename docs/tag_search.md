# How to list resources with tag filter.

> This guide assumes you set your spacectl configurations. If you didn't, we recommend you to read [docs/configuration.md](docs/configuration.md) and set your spacectl configurations.

You can filter specific resources which has complex data format.

## Search EC2 which has AWS Tags.Name

When you see "Raw Data", you can find the data structure like

~~~
    "tags": [
        {
            "key": "aws:ec2launchtemplate:id",
            "value": "lt-066016cc269546737"
        },
        {
            "key": "Name",
            "value": "case1-ec2-01"
        },
        {
            "key": "aws:ec2launchtemplate:version",
            "value": "1"
        }
    ],
~~~

There are list of tags, so you want to display only one of them.
The format is

~~~
tags.?[Search Key]:=[Search Value]=>[Key of wanted value]|[Title of Cell]

Example 1. dislay value of tags.Name

tags.?key:=Name=>value|Tags.name

Example 2. display  

tags.?value:=lt-066016cc269546737=>value|Tags.launchtemplate_id

~~~

Example 1.

~~~
spacectl list server -c "server_id,data.compute.instance_type|instance_type,tags.?key:=Name=>value|Tags.name"

 server_id           | instance_type    | Tags.name
---------------------+------------------+-----------------------------------------
 server-516bad7923f1 | r5.large         |
 server-04964f9ddb36 | r5.large         |
 server-ecfd5f6a9bef | r5.large         |
 server-035357f799b9 | t3.medium        |
 server-7fc5e9e33d8e | t3.medium        |
 server-75443f631f0c | t3.medium        |
 server-19e6f7468fc9 | t3.medium        |
 server-7e151168eec9 | t1.micro         | ['case1-ec2-01']
 server-a7257d5e0615 | t1.micro         | ['case1-ec2-02']
 server-dda6beab18e4 | t1.micro         | ['case1-ec2-03']
 server-bf5900b18f63 | t1.micro         | ['case1-ec2-04']
 server-e77326cce885 | t1.micro         | ['case1-ec2-05']
 server-99cb6bf9309f | t1.micro         | ['case2-ec2-01']

~~~


Example 2.

~~~
spacectl list server -c "server_id,data.compute.instance_type|instance_type,tags.?value:=lt-066016cc269546737=>value|Tags.launchtemplate_id"
 server_id           | instance_type    | Tags.launchtemplate_id
---------------------+------------------+--------------------------
 server-516bad7923f1 | r5.large         |
 server-04964f9ddb36 | r5.large         |
 server-ecfd5f6a9bef | r5.large         |
 server-035357f799b9 | t3.medium        |
 server-7fc5e9e33d8e | t3.medium        |
 server-75443f631f0c | t3.medium        |
 server-19e6f7468fc9 | t3.medium        |
 server-7e151168eec9 | t1.micro         | ['lt-066016cc269546737']
 server-a7257d5e0615 | t1.micro         | ['lt-066016cc269546737']
 server-dda6beab18e4 | t1.micro         | ['lt-066016cc269546737']
 server-bf5900b18f63 | t1.micro         | ['lt-066016cc269546737']
 server-e77326cce885 | t1.micro         | ['lt-066016cc269546737']
 server-99cb6bf9309f | t1.micro         | ['lt-066016cc269546737']
 server-c8013da4a666 | t1.micro         | ['lt-066016cc269546737']
 ~~~
