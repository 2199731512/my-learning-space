# 施工日报生成器

## 项目简介

土木工程施工日报自动生成工具。用户输入当天工地情况，AI（小米MiMo）生成规范的中文施工日报，导出为Word文档。

## 技术栈

- Python 3.10+
- OpenAI SDK（调用小米MiMo API，兼容OpenAI格式）
- python-docx（生成Word文档）

## 项目结构

```
├── main.py              # CLI入口，收集用户输入
├── generator.py         # 调用MiMo API生成结构化日报
├── docx_builder.py      # 渲染Word文档
├── template.py          # 日报数据结构定义（dataclass）
├── requirements.txt     # 依赖
└── output/              # 生成的日报存放目录
```

## 运行

```bash
pip install -r requirements.txt
python main.py          # 正常模式，手动输入
python main.py --test   # 测试模式，自动填入测试数据
```

## API配置

- 平台：小米MiMo
- Base URL：https://api.xiaomimimo.com/v1
- 模型：mimo-v2.5-pro
- SDK：OpenAI兼容格式

## 开发规范

- 变量名、函数名用英文
- 注释用中文
- API key不硬编码，通过环境变量或配置文件管理
