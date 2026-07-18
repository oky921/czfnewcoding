from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_parse_meeting_with_normal_input() -> None:
    response = client.post(
        "/api/meetings/parse",
        json={
            "rawText": """
            会议时间：2026年7月16日 14:00-15:00
            参会人员：张伟、李娜、王磊
            议题：确认订单拆单策略；讨论库存锁定方案
            张伟：确认本期先支持华东仓灰度。
            关键结论：灰度范围限定华东仓 10% 流量。
            待办：李娜负责补充产品说明，截止 7月18日。
            风险：库存服务 QPS 余量不足，灰度扩大时存在瓶颈。
            下一步：下周一进行联调评审。
            """
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["meeting_time"] == "2026年7月16日 14:00-15:00"
    assert data["participants"] == ["张伟", "李娜", "王磊"]
    assert data["speakers"] == ["张伟"]
    assert "确认订单拆单策略" in data["topics"]
    assert "灰度范围限定华东仓 10% 流量" in data["conclusions"]
    assert data["action_items"][0]["owner"] == "李娜"
    assert data["action_items"][0]["deadline"] == "7月18日"
    assert "库存服务 QPS 余量不足，灰度扩大时存在瓶颈" in data["risks"]
    assert "下周一进行联调评审" in data["next_steps"]


def test_parse_meeting_rejects_empty_text() -> None:
    response = client.post("/api/meetings/parse", json={"rawText": "   \n  "})

    assert response.status_code == 422


def test_parse_meeting_without_meeting_time() -> None:
    response = client.post(
        "/api/meetings/parse",
        json={
            "rawText": """
            参会人：周强、孙悦
            议题：确认发票模块上线范围
            周强：决定本期只上线电子发票。
            待办：孙悦整理迁移失败数据清单，截止：8月3日。
            """
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["meeting_time"] is None
    assert data["participants"] == ["周强", "孙悦"]
    assert "确认发票模块上线范围" in data["topics"]


def test_parse_meeting_with_multiple_action_items() -> None:
    response = client.post(
        "/api/meetings/parse",
        json={
            "rawText": """
            时间：2026年8月1日 上午 09:30
            与会人：周强、孙悦、何敏
            待办事项：
            1. 孙悦负责整理迁移失败数据清单，截止：8月3日。
            2. 何敏完成历史数据灰度校验脚本，最晚下周五。
            3. 周强提交上线审批材料，月底前完成。
            """
        },
    )

    assert response.status_code == 200
    action_items = response.json()["action_items"]
    assert len(action_items) == 3
    assert {(item["owner"], item["deadline"]) for item in action_items} == {
        ("孙悦", "8月3日"),
        ("何敏", "下周五"),
        ("周强", "月底前完成"),
    }


def test_parse_meeting_recognizes_risks() -> None:
    response = client.post(
        "/api/meetings/parse",
        json={
            "rawText": """
            会议时间：2026年9月5日 10:00
            参会人员：陈晨、刘洋
            风险与问题：
            - 支付渠道回调延迟仍存在不确定性，可能影响订单状态一致性。
            - 客服后台处理中状态文案尚未确认，可能造成用户理解偏差。
            刘洋：数据同步任务存在阻塞，需要排查异常日志。
            """
        },
    )

    assert response.status_code == 200
    risks = response.json()["risks"]
    assert "支付渠道回调延迟仍存在不确定性，可能影响订单状态一致性" in risks
    assert "客服后台处理中状态文案尚未确认，可能造成用户理解偏差" in risks
    assert "数据同步任务存在阻塞，需要排查异常日志" in risks
