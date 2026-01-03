# Python 面试题学习系统（单机版）

一个基于 Flask + SQLite 的本地面试题练习系统：题库分类浏览、答题判分、解析展示、收藏/错题本、学习进度统计，以及“模拟面试”（限时随机抽题）。

## 功能

- 题库分类：基础语法 / 框架相关 / 项目经验
- 答题：单选/多选自动判分，写入练习记录
- 解析页：显示正确答案、你的答案、解析与考点
- 学习进度：正确率、分类/难度统计、最近 7 天统计
- 收藏与错题本：收藏切换、错题列表
- 模拟面试：限时、随机抽题、逐题提交、结束汇总（状态保存在 session）

## 运行环境

- Python 3.8+（建议 3.10/3.11）
- Windows / macOS / Linux 均可

依赖见 requirements.txt。

## 快速开始

在项目根目录（本文件所在目录）执行：

1) 安装依赖

```bash
pip install -r requirements.txt
```

2) （可选）导入题库

系统数据库文件为 database/interview.db。首次运行会自动建表，但题库需要你导入题目。

- 生成示例题库 JSON：

```bash
python scripts/batch_import_questions.py --sample
```

- 导入 JSON 到数据库：

```bash
python scripts/batch_import_questions.py sample_questions.json
```

3) 启动 Web

```bash
python run.py
```

4) 打开浏览器

- 首页：http://127.0.0.1:5000/

## 页面入口

- 题库分类：http://127.0.0.1:5000/question/category
- 答题页：http://127.0.0.1:5000/question/answer?question_id=1
- 解析页：http://127.0.0.1:5000/question/explanation/1
- 学习进度：http://127.0.0.1:5000/progress/
- 模拟面试：http://127.0.0.1:5000/exam/mock

## 主要接口（便于前端调试）

题库/练习：

- GET /question/api/questions?category=basic|framework|project
- GET /question/api/question/<id>
- POST /question/api/submit_answer  JSON: {"question_id":1, "user_answer":"A"}
- GET /question/api/explanation/<id>?user_answer=A

收藏/错题：

- POST /progress/api/favorite/toggle JSON: {"question_id": 1}

模拟面试：

- POST /exam/api/start JSON: {"count":10, "category":"all", "time_limit_seconds":600}
- GET /exam/api/question
- POST /exam/api/submit JSON: {"question_id":1, "user_answer":"AB"}
- POST /exam/api/finish

## 数据库与文件说明

- Web 应用数据库：database/interview.db
- 自动建表逻辑：app/database/db.py（init_schema）
- 批量导入脚本：scripts/batch_import_questions.py

### 导入 JSON 格式（batch_import_questions.py）

该脚本要求每道题为如下字段（注意 option_a/option_b/...）：

```json
{
   "category": "Python Basics",
   "title": "题目内容",
   "option_a": "选项A",
   "option_b": "选项B",
   "option_c": "选项C",
   "option_d": "选项D",
   "correct_answer": "A",
   "difficulty": "Easy",
   "is_high_frequency": true,
   "analysis": "解析",
   "knowledge_point": "考点"
}
```

提示：data/initial_questions.json 的结构为 {options: {A:...,B:...}}，与本导入脚本格式不同；如需使用它，请先转换字段（或只用 sample_questions.json 作为模板）。

## 常见问题（排错）

### 1) 页面一直“加载中”

这通常是前端 JS 没跑起来（例如某个 static/js 文件内容不是合法 JS）。

- 打开开发者工具（F12）查看 Console 与 Network
- 确认 /question/api/questions?category=basic 能返回 JSON

历史问题：如果 static/js/jquery-3.6.0.min.js 文件开头被误加了 `# -*- coding: utf-8 -*-`，浏览器会报 Invalid or unexpected token，导致所有脚本中断；删除该行即可。

### 2) 你改了模板但页面没变化

确认你连到的是同一个 Flask 进程（尤其是端口被占用时）。本项目提供：

- http://127.0.0.1:5000/__debug/ping
- http://127.0.0.1:5000/__debug/info

响应头会带 X-App-Instance，便于确认当前实例。

### 3) 端口被占用

设置环境变量修改端口：

```bash
set PORT=5001
python run.py
```

或直接在启动时指定：

```bash
set HOST=127.0.0.1
set PORT=5001
python run.py
```

## 测试

```bash
pytest -q
```

## 目录结构（与运行相关）

```text
Python-System/
   run.py
   requirements.txt
   pages/                 # HTML 模板
   static/                # 静态资源（css/js/icons）
   app/
      blueprints/          # main/question/progress/interview
      database/db.py       # SQLite + schema
   scripts/               # 导入/工具脚本
   database/              # interview.db（运行后生成/更新）
```

## 备注：python_learning_judge/

python_learning_judge/ 目录是另一个“数据库/判题记录管理”的教学模块示例，与本 Web 面试题系统的主数据库（database/interview.db）不是同一个库。

