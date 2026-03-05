# MCP Feedback Lite

轻量级 MCP 反馈工具，通过原生 tkinter 弹窗为 Cursor IDE 中的 AI Agent 提供**人机交互反馈循环**，最大化单次对话效果。

## 功能特点

- 任务完成后弹出原生桌面对话框，展示 AI 工作摘要并收集用户反馈
- 支持多轮反馈循环，无需反复开启新对话
- Catppuccin 风格深色主题，美观易用
- 超时自动关闭，支持快捷键操作（Ctrl+Enter 提交 / Esc 关闭）
- 零外部 GUI 依赖，仅使用 Python 标准库 tkinter

## 前置要求

- **Python** >= 3.11
- **[uv](https://docs.astral.sh/uv/)** — 推荐的 Python 包管理器（也可用 pip）

## 安装与使用

### 1. 克隆仓库

```bash
git clone https://github.com/woaijiadanoo/mcp-marketplace.git
cd mcp-marketplace/mcp-feedback-lite
```

### 2. 配置 Cursor MCP

在 Cursor 的 MCP 配置文件中添加以下内容。

**用户级配置**（所有项目生效）— 编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "mcp-feedback-lite": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp-feedback-lite",
        "mcp-feedback-lite"
      ],
      "timeout": 600,
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

**项目级配置**（仅当前项目生效）— 编辑 `<project>/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "mcp-feedback-lite": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp-feedback-lite",
        "mcp-feedback-lite"
      ],
      "timeout": 600,
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

> **注意**：将 `/absolute/path/to/mcp-feedback-lite` 替换为你实际克隆的目录路径。Windows 上使用 `\\` 或 `/` 分隔，例如 `D:\\workspace\\mcp-marketplace\\mcp-feedback-lite`。

### 3. 安装 Cursor Rule（推荐）

将 `.cursor/rules/mcp-feedback-loop.mdc` 拷贝到你的 Cursor 用户级规则目录，让 AI 自动遵循反馈循环工作流：

```bash
# Windows
copy .cursor\rules\mcp-feedback-loop.mdc %USERPROFILE%\.cursor\rules\

# macOS / Linux
cp .cursor/rules/mcp-feedback-loop.mdc ~/.cursor/rules/
```

也可以直接拷贝到项目的 `.cursor/rules/` 目录中，仅对该项目生效。

### 4. 重启 Cursor

配置完成后重启 Cursor，MCP 工具即生效。

## 工作原理

1. AI Agent 完成任务后调用 `interactive_feedback` 工具
2. 弹出桌面对话框，上半部分展示 AI 工作摘要，下半部分供用户输入反馈
3. 用户输入反馈后，AI 根据反馈继续执行
4. 循环往复，直到用户提交空白内容或输入退出关键词

## MCP 工具参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_directory` | string | `"."` | 项目目录路径（显示在对话框标题） |
| `summary` | string | `"已完成您请求的任务。"` | AI 工作摘要 |
| `timeout` | int | `600` | 超时秒数（超时后自动关闭） |

## 许可证

MIT
