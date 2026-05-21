"""测试脚本 - 跳过交互输入直接生成日报"""
from generator import generate_report
from docx_builder import build_docx
import os

os.makedirs("output", exist_ok=True)

project_name = "某某建设集团"
date = "2026年5月20日"
description = "今天进行了3#楼二层柱钢筋绑扎，浇筑C30混凝土约50方。现场有管理人员12人，工人85人。使用了1台塔吊、2台混凝土罐车。安全方面进行了班前安全教育，现场配备灭火器6个。发现2#楼东侧临边防护缺失，已安排整改。明天计划进行3#楼二层梁板模板支设。"

print("正在调用 MiMo API 生成日报...")
report = generate_report(project_name, date, description)
print(f"生成完成，天气：{report.weather}")
print(f"施工部位：{report.construction_location}")

output_path = os.path.join("output", "测试_施工日报_v2.docx")
build_docx(report, output_path)
print(f"Word文档已保存：{os.path.abspath(output_path)}")
