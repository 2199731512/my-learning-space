import os
import sys
import json
from datetime import datetime
from generator import generate_report
from docx_builder import build_docx
from app.database import init_db, save_report
from app.web import start_web


def main():
    # 自动创建 output 目录（兼容旧路径）
    os.makedirs("output", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # 初始化数据库
    init_db()

    # Web 模式
    if "--web" in sys.argv:
        start_web()
        return

    print("=" * 50)
    print("        施工日报生成器")
    print("=" * 50)
    print()

    # 测试模式：--test 参数自动填入固定数据
    if "--test" in sys.argv:
        print("[测试模式] 自动填入测试数据\n")
        project_name = "滨江住宅项目A栋"
        date_input = datetime.now().strftime("%Y年%m月%d日")
        description = "今日天气晴，完成3层楼板混凝土浇筑，投入木工8人、钢筋工5人、混凝土工4人，塔吊1台正常运行，无安全事故，明日计划进行4层模板安装"
    else:
        # 正常模式：收集用户输入
        project_name = input("请输入项目名称：").strip()
        if not project_name:
            project_name = "未命名项目"

        date_input = input("请输入日期（直接回车默认今天）：").strip()
        if not date_input:
            date_input = datetime.now().strftime("%Y年%m月%d日")

        print("\n请输入今日工地情况描述（输入完毕后按回车）：")
        print("（例如：今天进行了3#楼二层柱钢筋绑扎，浇筑了C30混凝土约50方...）")
        description = input().strip()

        if not description:
            print("错误：工地情况描述不能为空")
            return

    print("\n正在生成施工日报...")

    try:
        # 调用 AI 生成日报
        report = generate_report(project_name, date_input, description)

        # 生成文件名
        safe_name = project_name.replace(" ", "_").replace("/", "_")
        filename = f"{safe_name}_施工日报_{date_input}.docx"
        output_path = os.path.join("reports", filename)

        # 生成 Word 文档
        build_docx(report, output_path)

        # 保存到数据库
        ai_content = json.dumps({
            "weather": report.weather,
            "construction_location": report.construction_location,
            "main_work": report.main_work,
            "personnel": report.personnel,
            "machinery": report.machinery,
            "safety": report.safety,
            "issues": report.issues,
            "tomorrow_plan": report.tomorrow_plan,
            "photo_placeholders": report.photo_placeholders,
        }, ensure_ascii=False)

        record_id = save_report(
            date=date_input,
            project_name=project_name,
            original_input=description,
            ai_content=ai_content,
            docx_path=output_path
        )

        print(f"\n施工日报已生成！")
        print(f"文件路径：{os.path.abspath(output_path)}")
        print(f"记录ID：{record_id}")
        print(f"\n提示：运行 `python main.py --web` 可启动 Web 界面查看历史日报")

    except Exception as e:
        print(f"\n生成失败：{e}")


if __name__ == "__main__":
    main()
