# 施工日报生成器

土木工程施工日报自动生成工具。输入当天工地情况，AI生成规范的中文施工日报，导出为Word文档。

## 快速开始

```bash
pip install -r requirements.txt
python main.py          # 正常模式，手动输入
python main.py --test   # 测试模式，自动填入测试数据
```

## 项目结构

```
├── main.py              # CLI入口
├── generator.py         # 调用MiMo API生成日报
├── docx_builder.py      # 渲染Word文档
├── template.py          # 数据结构定义
├── requirements.txt     # 依赖
└── output/              # 生成的日报存放目录
```

## 技术栈

- Python 3.10+
- OpenAI SDK（小米MiMo API，兼容OpenAI格式）
- python-docx

## API配置

- 平台：小米MiMo (platform.xiaomimimo.com)
- Base URL：https://api.xiaomimimo.com/v1
- 模型：mimo-v2.5-pro
