# Python-System

本仓库用于存放 Python 学习与练习相关代码与模块，按功能模块化组织，便于教学与作业管理。

主要模块
- python_learning_judge/ — B 模块：数据库（单机版）与判题记录管理，包含初始化脚本与数据库文件
  - 功能：存储用户、题目与提交记录的 SQLite 数据库；包含初始化脚本与数据库设计说明
  - 路径：`python_learning_judge/`

仓库结构示例
```
Python-System/
├─ README.md
├─ python_learning_judge/
│  ├─ init_db.py
│  ├─ python_learning.db
│  └─ database_design.md
└─ ...
```

快速开始
1. 克隆仓库：
   ```bash
   git clone https://github.com/Maxium281/Python-System.git
   cd Python-System
   ```
2. 查看并运行 B 模块（数据库）：
   ```bash
   # 进入模块目录
   cd python_learning_judge

   # 若要初始化数据库（示例）
   python init_db.py
   ```
3. 若要查看数据库结构或设计，请打开 `python_learning_judge/database_design.md`。

贡献与分支策略
- 我们建议在新功能或变更时创建分支并发起 PR（例如：`update/readme-structure`），便于审阅与合并。
- 提交信息示例：`chore: update README and organize python_learning_judge directory`

许可证
- 请在此处填写许可证信息（例如 MIT），或在仓库根目录添加 LICENSE 文件.

---
