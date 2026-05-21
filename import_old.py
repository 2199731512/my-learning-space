"""导入旧日报到数据库"""
import os
import re
from app.database import init_db, save_report

REPORTS_DIR = "reports"
OLD_DIR = "output"


def import_old_reports():
    init_db()

    # 确保 reports 目录存在
    os.makedirs(REPORTS_DIR, exist_ok=True)

    imported = 0
    for filename in os.listdir(OLD_DIR):
        # 跳过临时文件
        if filename.startswith("~$") or not filename.endswith(".docx"):
            continue

        old_path = os.path.join(OLD_DIR, filename)

        # 从文件名解析项目名和日期
        # 格式1: 项目名_施工日报_日期.docx
        # 格式2: 项目名_施工日报.docx（无日期）
        match = re.match(r"(.+?)_施工日报[_]*(.*?)\.docx", filename)
        if match:
            project_name = match.group(1)
            date_str = match.group(2).strip("_") or "未知日期"
        else:
            project_name = filename.replace(".docx", "")
            date_str = "未知日期"

        # 复制到新目录
        new_path = os.path.join(REPORTS_DIR, filename)
        if not os.path.exists(new_path):
            import shutil
            shutil.copy2(old_path, new_path)

        # 保存到数据库
        record_id = save_report(
            date=date_str,
            project_name=project_name,
            original_input="[旧数据导入] 原始输入未保存",
            ai_content='{"note": "旧数据导入，AI生成内容未保存"}',
            docx_path=new_path
        )
        print(f"已导入: ID={record_id} | {project_name} | {date_str}")
        imported += 1

    print(f"\n导入完成，共 {imported} 条")


if __name__ == "__main__":
    import_old_reports()
