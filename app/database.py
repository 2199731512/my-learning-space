import sqlite3
import os
import re
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

# 数据库文件路径
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "reports.db")


def init_db():
    """初始化数据库，创建表结构"""
    os.makedirs(DB_DIR, exist_ok=True)
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                project_name TEXT NOT NULL,
                original_input TEXT NOT NULL,
                ai_content TEXT NOT NULL,
                docx_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


@contextmanager
def get_connection():
    """获取数据库连接的上下文管理器"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def parse_date(date_str: str) -> datetime:
    """解析日期字符串，支持多种格式，返回 datetime 对象用于排序"""
    if not date_str:
        return datetime.min

    # 尝试多种格式
    formats = [
        "%Y年%m月%d日",   # 2026年05月20日
        "%Y-%m-%d",       # 2026-05-20
        "%Y/%m/%d",       # 2026/05/20
        "%Y.%m.%d",       # 2026.05.20
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    # 尝试提取数字
    match = re.search(r"(\d{4})\D+(\d{1,2})\D+(\d{1,2})", date_str)
    if match:
        try:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            pass

    return datetime.min


def format_date(date_str: str) -> str:
    """统一日期格式为 YYYY年MM月DD日"""
    if not date_str:
        return "未知日期"

    # 已经是目标格式
    if re.match(r"^\d{4}年\d{2}月\d{2}日$", date_str):
        return date_str

    # 尝试解析
    dt = parse_date(date_str)
    if dt == datetime.min:
        return date_str  # 无法解析，返回原值

    return dt.strftime("%Y年%m月%d日")


def save_report(date: str, project_name: str, original_input: str,
                ai_content: str, docx_path: str) -> int:
    """保存日报记录，返回记录ID"""
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO reports (date, project_name, original_input, ai_content, docx_path)
               VALUES (?, ?, ?, ?, ?)""",
            (date, project_name, original_input, ai_content, docx_path)
        )
        conn.commit()
        return cursor.lastrowid


def get_all_reports() -> List[dict]:
    """获取所有日报，按日期倒序排列"""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM reports").fetchall()
        reports = [dict(row) for row in rows]

    # 在 Python 中排序（因为 SQLite 无法解析中文日期）
    reports.sort(key=lambda r: parse_date(r.get("date", "")), reverse=True)

    # 统一日期显示格式，带兜底逻辑
    for report in reports:
        date_str = report.get("date", "")
        dt = parse_date(date_str)
        if dt == datetime.min:
            created_at = report.get("created_at", "")
            if created_at:
                try:
                    dt = datetime.strptime(str(created_at)[:10], "%Y-%m-%d")
                    report["date_display"] = dt.strftime("%Y年%m月%d日")
                except (ValueError, TypeError):
                    report["date_display"] = "未知日期"
            else:
                report["date_display"] = "未知日期"
        else:
            report["date_display"] = dt.strftime("%Y年%m月%d日")

    return reports


def get_report_by_id(report_id: int) -> Optional[dict]:
    """根据ID获取日报"""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM reports WHERE id = ?", (report_id,)
        ).fetchone()
        if row:
            report = dict(row)
            date_str = report.get("date", "")
            dt = parse_date(date_str)
            if dt == datetime.min:
                created_at = report.get("created_at", "")
                if created_at:
                    try:
                        dt = datetime.strptime(str(created_at)[:10], "%Y-%m-%d")
                        report["date_display"] = dt.strftime("%Y年%m月%d日")
                    except (ValueError, TypeError):
                        report["date_display"] = "未知日期"
                else:
                    report["date_display"] = "未知日期"
            else:
                report["date_display"] = dt.strftime("%Y年%m月%d日")
            return report
        return None
