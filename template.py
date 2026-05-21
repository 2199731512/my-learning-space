from dataclasses import dataclass, field
from typing import List


@dataclass
class DailyReport:
    """施工日报数据结构"""
    project_name: str = ""          # 项目名称
    date: str = ""                  # 日期
    weather: str = ""               # 天气情况
    construction_location: str = "" # 施工部位
    main_work: str = ""             # 主要工作内容
    personnel: str = ""             # 人员情况
    machinery: str = ""             # 机械设备
    safety: str = ""                # 安全文明施工
    issues: str = ""                # 存在问题及处理措施
    tomorrow_plan: str = ""         # 明日工作计划
    photo_placeholders: List[str] = field(default_factory=list)  # 图片占位符


# JSON Schema —— generator.py 的 prompt 直接引用
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "weather": {"type": "string", "description": "天气情况，如：晴，气温25-32℃"},
        "construction_location": {"type": "string", "description": "施工部位，如：3#楼主体结构"},
        "main_work": {"type": "string", "description": "主要工作内容，详细描述当天施工情况"},
        "personnel": {"type": "string", "description": "人员情况，如：管理人员15人，工人120人"},
        "machinery": {"type": "string", "description": "机械设备使用情况"},
        "safety": {"type": "string", "description": "安全文明施工情况"},
        "issues": {"type": "string", "description": "存在问题及处理措施"},
        "tomorrow_plan": {"type": "string", "description": "明日工作计划"},
        "photo_placeholders": {
            "type": "array",
            "items": {"type": "string"},
            "description": "图片占位符描述列表，如：['基坑开挖现场', '钢筋绑扎完成']"
        }
    },
    "required": [
        "weather", "construction_location", "main_work",
        "personnel", "machinery", "safety", "issues",
        "tomorrow_plan", "photo_placeholders"
    ]
}
