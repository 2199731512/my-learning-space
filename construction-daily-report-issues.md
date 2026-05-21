# 施工日报生成器 — 问题与改进记录

## 问题1：API地址错误

- 用户给的 `token-plan-cn.xiaomimo.com` 不存在
- `api.xiaomimo.com` 一开始DNS解析失败（后恢复）
- **解决**：从官方文档 `platform.xiaomimimo.com/llms.txt` 确认正确地址为 `https://api.xiaomimimo.com/v1`

## 问题2：API Key无效

- 第一个key `tp-cdk...` 返回401 Invalid API Key
- **解决**：用户更换为 `sk-cnyc...` 后正常

## 问题3：模型名大小写

- 文档示例为 `mimo-v2.5-pro`（全小写）
- **解决**：按官方文档统一用小写

## 问题4：SDK选型错误

- 初始计划用 Anthropic SDK
- MiMo只兼容OpenAI格式，不兼容Anthropic SDK
- **解决**：改用 `openai` SDK

## 问题5：终端中文编码

- `python main.py` 通过heredoc传入中文时出现 `surrogates not allowed` 错误
- **解决**：改用独立 `test_run.py` 测试脚本绕过

## 问题6：文件占用

- 生成的docx文件被其他程序打开时，再次写入报 `PermissionError`
- **解决**：输出文件名加版本后缀避免冲突

## 问题7：表格样式粗糙

- 初始版本没有内边距、没有垂直居中
- **解决**：用 `OxmlElement` 设置 `tcMar`（内边距）和 `vAlign`（垂直居中）

## 改进清单

| 项目 | 改进内容 |
|---|---|
| 字段名 | `construction部位` → `construction_location`（中文变量名不可用） |
| 图片占位符 | `【附图：XXX】` → `【附图1：XXX】`（带编号） |
| output目录 | 手动创建 → `os.makedirs("output", exist_ok=True)` |
| 测试模式 | 新增 `--test` 参数，自动填入固定数据 |
| API配置 | 从官方llms.txt获取，不靠猜测 |
