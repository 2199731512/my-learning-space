import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import init_db, get_all_reports, get_report_by_id

app = FastAPI(title="施工日报生成器")

# 模板目录
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)

# docx 文件存放目录
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")


@app.on_event("startup")
async def startup():
    """应用启动时初始化数据库"""
    init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """首页 - 日报列表"""
    reports = get_all_reports()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"reports": reports}
    )


@app.get("/report/{report_id}", response_class=HTMLResponse)
async def detail(request: Request, report_id: int):
    """详情页"""
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="日报不存在")
    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={"report": report}
    )


@app.get("/download/{report_id}")
async def download(report_id: int):
    """下载 docx 文件"""
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="日报不存在")

    docx_path = report["docx_path"]

    # 如果是相对路径，转换为绝对路径
    if not os.path.isabs(docx_path):
        docx_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), docx_path)

    if not os.path.exists(docx_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    filename = os.path.basename(docx_path)
    return FileResponse(
        path=docx_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


def start_web(host: str = "127.0.0.1", port: int = 8000):
    """启动 Web 服务"""
    import uvicorn
    print(f"\nWeb 服务已启动：http://{host}:{port}")
    print("按 Ctrl+C 停止服务\n")
    uvicorn.run(app, host=host, port=port)
