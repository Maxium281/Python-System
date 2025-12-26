# python_learning_judge

模块名称：Python 学习教辅 — 数据库模块（B 模块）

简短描述
- Python学习教辅软件数据库模块（含判题记录与用户管理）

用途
- 初始化并管理一个本地 SQLite 数据库，用于存储用户（students）、题目（problems）和提交记录（submissions）。

特点与说明
- 单机版，无服务器：数据库以 SQLite 文件形式（python_learning.db）保存在模块目录，可直接运行与查看。
- 目录中包含：
  - `init_db.py`：用于创建/初始化数据库表结构与示例数据的脚本
  - `python_learning.db`：示例或当前数据库文件（可直接打开）
  - `database_design.md`：数据库结构说明文档，包含表结构、关系与字段说明

快速使用
1. 进入模块目录：
   ```bash
   cd python_learning_judge
   ```
2. 初始化数据库（创建表并插入示例数据）：
   ```bash
   python init_db.py
   ```
3. 使用或查看数据库：
   - 使用 SQLite 浏览器打开 `python_learning.db`
   - 或在 Python 中使用 `sqlite3` 模块连接并查询

建议说明
- 若有需要将来扩展为有后端服务（例如 Flask），建议把当前数据库连接逻辑抽象成可重用模块，便于迁移到服务端。
- 请勿将敏感或个人信息提交到仓库中的数据库文件，必要时在提交前清理或将示例数据替换为虚拟数据。
