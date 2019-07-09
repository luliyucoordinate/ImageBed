---
layout: post
title: python递归解析JSON（目前最好的方案）
category : python
tags : [python, JSON]
stickie: true
date: 2018-05-11 00:00:00
---

我们要完成的任务是输出`JSON`字典，并且对其中的每个元素，要输出它的所有父节点。那么很容易想到的做法就是递归解析。

我参考了别人的一些文章和回答，总结了如下的解决方案：

```python
from __future__ import print_function
import json

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre+[key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:                   
                    yield pre+[key, '[]']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict
        
if __name__ == "__main__":
    sJOSN =  ''
    sValue = json.loads(sJOSN)
    for i in dict_generator(sValue):
        print('.'.join(i[0:-1]), ':', i[-1])
```

我对于以下几个例子做出测试

```json
{
    "base_config":{
        "enforce":{
            "value":"0",
            "inherit":"0",
            "global":"0"
        },
        "modify":{
            "value":"0",
            "inherit":"0",
            "global":"0"
        }
    },
    "safe_control_list":{
        "list":[
            {
                "gid":"0",
                "gname":"全网计算机",
                "isactive":"1",
                "rule_id":"0",
                "rule_name":"请选择规则",
                "time_range":"所有时间",
                "time_range_id":"1",
                "policy_tpl":"33",
                "policy_tpl_id":"17",
                "isonline":"3",
                "priority":"1"
            }
        ]
    }
}
```

测试结果如下

```
base_config.enforce.value : 0
base_config.enforce.inherit : 0
base_config.enforce.global : 0
base_config.modify.value : 0
base_config.modify.inherit : 0
base_config.modify.global : 0
safe_control_list.list.gid : 0
safe_control_list.list.gname : 全网计算机
safe_control_list.list.isactive : 1
safe_control_list.list.rule_id : 0
safe_control_list.list.rule_name : 请选择规则
safe_control_list.list.time_range : 所有时间
safe_control_list.list.time_range_id : 1
safe_control_list.list.policy_tpl : 33
safe_control_list.list.policy_tpl_id : 17
safe_control_list.list.isonline : 3
safe_control_list.list.priority : 1
```

使用另外一个测试用例

```json
{
    "detail":{
        "baseline":{
            "cancel_scheduled_task":"1",
            "comeonstage":"topwin",
            "conf_ver":2635792175,
            "conf_ver_s":"f7f8ac46##",
            "mission_id":0,
            "rules":{

            },
            "scheduled_task":"1",
            "scheduled_task_rule":{
                "autoexec_on_coundown":"1",
                "exec_countdown":"0",
                "exec_interval":"0",
                "exec_mode":"4",
                "exec_time":"*|00|*|*|*",
                "extra":{
                    "countdown_type":"3600",
                    "cycle_type":"1",
                    "every_type":"1"
                },
                "gid":0,
                "is_notice":"1",
                "is_reportback":"0",
                "module_id":3,
                "name":"",
                "notice_msg":"",
                "status":1,
                "tpl_id":420,
                "type":1
            }
        }
    },
    "id":1,
    "type":2100
}
```

测试结果如下

```json
detail.baseline.cancel_scheduled_task : 1
detail.baseline.comeonstage : topwin
detail.baseline.conf_ver : 2635792175
detail.baseline.conf_ver_s : f7f8ac46##
detail.baseline.mission_id : 0
detail.baseline.rules : {}
detail.baseline.scheduled_task : 1
detail.baseline.scheduled_task_rule.autoexec_on_coundown : 1
detail.baseline.scheduled_task_rule.exec_countdown : 0
detail.baseline.scheduled_task_rule.exec_interval : 0
detail.baseline.scheduled_task_rule.exec_mode : 4
detail.baseline.scheduled_task_rule.exec_time : *|00|*|*|*
detail.baseline.scheduled_task_rule.extra.countdown_type : 3600
detail.baseline.scheduled_task_rule.extra.cycle_type : 1
detail.baseline.scheduled_task_rule.extra.every_type : 1
detail.baseline.scheduled_task_rule.gid : 0
detail.baseline.scheduled_task_rule.is_notice : 1
detail.baseline.scheduled_task_rule.is_reportback : 0
detail.baseline.scheduled_task_rule.module_id : 3
detail.baseline.scheduled_task_rule.name : 
detail.baseline.scheduled_task_rule.notice_msg : 
detail.baseline.scheduled_task_rule.status : 1
detail.baseline.scheduled_task_rule.tpl_id : 420
detail.baseline.scheduled_task_rule.type : 1
id : 1
type : 2100
```

**如果大家在使用过程中有任何问题，希望告知，我加以完善！！！**

