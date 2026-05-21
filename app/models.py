from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReportCreate(BaseModel):
    """创建日报请求模型"""
    date: str
    project_name: str
    original_input: str
    ai_content: str
    docx_path: str


class ReportResponse(BaseModel):
    """日报响应模型"""
    id: int
    date: str
    project_name: str
    original_input: str
    ai_content: str
    docx_path: str
    created_at: Optional[str] = None
