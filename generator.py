import json
import os
from openai import OpenAI
from template import DailyReport, JSON_SCHEMA


# MiMo API 配置
API_KEY = os.getenv("MIMO_API_KEY", "sk-cnycjj4li94hk465tlbv5hudr24h51btlzprtuqjakl32a3q")
BASE_URL = "https://api.xiaomimimo.com/v1"
MODEL = "mimo-v2.5-pro"


def generate_report(project_name: str, date: str, description: str) -> DailyReport:
    """调用 MiMo API 生成施工日报"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    prompt = f"""你是一位专业的施工日报撰写人员。根据以下信息生成一份规范的中文施工日报。

项目名称：{project_name}
日期：{date}
今日工地情况描述：
{description}

请严格按照以下JSON格式输出，不要输出其他内容：
{json.dumps(JSON_SCHEMA, ensure_ascii=False, indent=2)}

注意：
1. 天气情况要合理推断或标注"待补充"
2. 人员情况要根据工作内容合理估算
3. 机械设备要与工作内容匹配
4. 安全文明施工要写出具体措施
5. 图片占位符用简短描述，如"基坑开挖现场"、"钢筋绑扎完成"
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )

    content = response.choices[0].message.content.strip()

    # 尝试提取JSON（处理模型可能输出的markdown代码块）
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    data = json.loads(content)

    # 构建 DailyReport 对象
    report = DailyReport(
        project_name=project_name,
        date=date,
        weather=data.get("weather", ""),
        construction_location=data.get("construction_location", ""),
        main_work=data.get("main_work", ""),
        personnel=data.get("personnel", ""),
        machinery=data.get("machinery", ""),
        safety=data.get("safety", ""),
        issues=data.get("issues", ""),
        tomorrow_plan=data.get("tomorrow_plan", ""),
        photo_placeholders=data.get("photo_placeholders", []),
    )

    return report
