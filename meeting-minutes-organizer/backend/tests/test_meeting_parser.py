from app.services.meeting_parser import parse_meeting_minutes


COMPLEX_MEETING_TEXT = """
会议标题：订单履约系统二期评审会
会议时间：2026年7月16日 周四 14:00-16:10
参会人员：张伟（产品负责人）、李娜、王磊、赵敏、陈晨、刘洋
主持人：张伟

会议议题：
1. 确认订单拆单策略和库存锁定方案
2. 讨论支付回调延迟对履约链路的影响
3. 明确灰度上线范围、监控指标和回滚预案

张伟：今天主要确认二期履约方案，目标是月底前支持多仓拆单和异常订单人工兜底。
李娜：产品侧确认拆单规则按仓库优先、时效次之执行，特殊大客户订单需要保留人工审核入口。
王磊：技术方案上，库存锁定服务会在支付成功后写入锁定流水；如果支付回调超过 5 分钟，会触发补偿任务。
赵敏：测试发现沙箱环境里支付回调偶发延迟，可能导致订单状态停留在待确认，影响客服查询。
陈晨：运维侧建议灰度先覆盖华东仓 10% 流量，并增加库存锁定失败率、回调耗时 P95 两个监控项。
刘洋：数据看板需要新增拆单成功率、人工审核量和异常订单关闭时长，方便上线后复盘。

关键结论：
- 拆单策略最终采用“仓库优先 + 时效兜底”，大客户订单保留人工审核。
- 灰度范围先限定华东仓 10% 流量，稳定 48 小时后再扩大到 50%。
- 支付回调超过 5 分钟必须进入补偿队列，并在客服后台展示处理中状态。

待办事项：
1. 李娜负责补充大客户人工审核的产品交互，截止 7月18日 18:00。
2. 王磊完成库存锁定接口和补偿任务联调，DDL：7月22日。
3. 赵敏跟进支付回调延迟的自动化回归用例，最晚下周三。
4. 陈晨输出灰度监控面板和回滚脚本，截止时间：2026年7月24日。
5. 刘洋提交上线后数据看板字段清单，月底前完成。

风险与问题：
- 支付渠道回调延迟仍存在不确定性，可能影响订单状态一致性。
- 华东仓库存服务当前 QPS 余量不足，灰度扩大时存在瓶颈。
- 客服后台处理中状态文案尚未确认，可能造成用户理解偏差。

下一步安排：
- 明天上午同步支付渠道补偿接口人，确认重试频率和告警阈值。
- 下周一进行第一轮联调评审。
- 上线前安排一次回滚演练，并由陈晨记录演练结果。
"""


def test_parse_complex_chinese_meeting_minutes() -> None:
    result = parse_meeting_minutes(COMPLEX_MEETING_TEXT)

    assert result["meeting_time"] == "2026年7月16日 周四 14:00-16:10"
    assert result["participants"] == ["张伟", "李娜", "王磊", "赵敏", "陈晨", "刘洋"]
    assert result["speakers"] == ["张伟", "李娜", "王磊", "赵敏", "陈晨", "刘洋"]

    assert "确认订单拆单策略和库存锁定方案" in result["topics"]
    assert "讨论支付回调延迟对履约链路的影响" in result["topics"]
    assert "明确灰度上线范围、监控指标和回滚预案" in result["topics"]

    assert "拆单策略最终采用“仓库优先 + 时效兜底”，大客户订单保留人工审核" in result["conclusions"]
    assert "灰度范围先限定华东仓 10% 流量，稳定 48 小时后再扩大到 50%" in result["conclusions"]

    action_items = result["action_items"]
    assert isinstance(action_items, list)
    assert {item["owner"] for item in action_items} >= {"李娜", "王磊", "赵敏", "陈晨", "刘洋"}
    assert {
        (item["owner"], item["deadline"])
        for item in action_items
    } >= {
        ("李娜", "7月18日 18:00"),
        ("王磊", "7月22日"),
        ("赵敏", "下周三"),
        ("陈晨", "2026年7月24日"),
        ("刘洋", "月底前完成"),
    }
    assert any(item["owner"] == "王磊" and "库存锁定接口和补偿任务联调" in item["task"] for item in action_items)

    assert "支付渠道回调延迟仍存在不确定性，可能影响订单状态一致性" in result["risks"]
    assert "华东仓库存服务当前 QPS 余量不足，灰度扩大时存在瓶颈" in result["risks"]
    assert "明天上午同步支付渠道补偿接口人，确认重试频率和告警阈值" in result["next_steps"]
    assert "下周一进行第一轮联调评审" in result["next_steps"]


def test_parse_inline_fields_and_action_item_variants() -> None:
    text = """
    时间：2026年8月1日 上午 09:30
    与会人：周强、孙悦；何敏
    议题：确认发票模块上线范围；讨论历史数据迁移
    周强：决定本期只上线电子发票，纸票能力延期。
    待办：负责人：孙悦，任务：整理迁移失败数据清单，截止：8月3日
    待办：历史数据灰度校验脚本，负责人：何敏，最晚下周五
    问题：老系统存在部分税号为空的数据，需要业务确认处理口径。
    下一步：会后同步财务负责人，并在上线前完成数据抽样。
    """

    result = parse_meeting_minutes(text)

    assert result["meeting_time"] == "2026年8月1日 上午 09:30"
    assert result["participants"] == ["周强", "孙悦", "何敏"]
    assert result["speakers"] == ["周强"]
    assert result["topics"] == ["确认发票模块上线范围", "讨论历史数据迁移"]
    assert "决定本期只上线电子发票，纸票能力延期" in result["conclusions"]
    assert {item["owner"] for item in result["action_items"]} >= {"孙悦", "何敏"}
    assert any(item["deadline"] == "8月3日" for item in result["action_items"])
    assert any(item["deadline"] == "下周五" for item in result["action_items"])
    assert "老系统存在部分税号为空的数据，需要业务确认处理口径" in result["risks"]
    assert "会后同步财务负责人，并在上线前完成数据抽样" in result["next_steps"]
