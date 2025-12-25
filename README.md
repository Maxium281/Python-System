<!-- -*- coding: utf-8 -*- -->
# Python 面试题学习系统（单机版）

## 项目概述

一个**基于 Flask 的单机版 Python 面试题学习系统**，集问题管理、模拟面试、进度跟踪和错题本于一体。全程运行在本地，无需联网。

## 架构设计

### 三层架构

```
┌─────────────────────────────────────────────────────────┐
│ 表现层（前端）                                          │
│ - Jinja2 模板 + Bootstrap 本地版 + 原生 JS              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 应用层（核心）                                          │
│ - Flask 框架（主程序、路由、视图函数）                  │
│ - 面向对象核心类（题库、用户进度、模拟面试等）          │
│ - 工具类（本地资源加载、日志处理）                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 数据层                                                  │
│ - SQLite 数据库 + DBManager 封装类                      │
└─────────────────────────────────────────────────────────┘
```

### 核心类说明

| 类名 | 主要职责 |
|------|--------|
| `QuestionBank` | 题目查询、分类、搜索 |
| `InterviewSimulator` | 模拟面试生成、倒计时、记录保存 |
| `UserProgress` | 答题记录、正确率计算、收藏管理 |
| `Config` | 路径管理、本地资源检查 |
| `DBManager` | SQLite 连接、查询、执行、提交/回滚 |
| `LocalResourceLoader` | 静态资源（CSS、JS）加载与校验 |
| `Logger` | 统一日志记录 |

## 项目目录结构

```
python_interview_system/
├── app/
│   ├── __init__.py                    # Flask 应用工厂
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                  # 配置管理类
│   │   ├── question_bank.py           # 题库管理类
│   │   ├── interview_simulator.py     # 模拟面试类
│   │   └── user_progress.py           # 用户进度类
│   ├── routes/
│   │   ├── __init__.py                # 路由注册
│   │   ├── index.py                   # 首页路由
│   │   ├── question.py                # 题库路由
│   │   ├── exam.py                    # 模拟面试路由
│   │   └── progress.py                # 进度页路由
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── local_resource_loader.py   # 本地资源加载器
│   │   └── logger.py                  # 日志工具类
│   ├── templates/                     # Jinja2 模板（HTML）
│   └── static/                        # 静态资源（CSS、JS、图片）
├── app/database/
│   ├── __init__.py
│   └── db_manager.py                  # SQLite 数据库封装
├── database/
│   └── interview.db                   # SQLite 数据库文件
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Pytest 配置与固定装置
│   ├── test_dbmanager.py              # DBManager 单元测试
│   ├── test_question_bank.py          # QuestionBank 单元测试
│   ├── test_user_progress.py          # UserProgress 单元测试
│   └── test_interview_simulator.py    # InterviewSimulator 单元测试
├── logs/
│   └── interview_system.log           # 应用日志文件
├── run.py                             # 项目启动文件
├── requirements.txt                   # 依赖包列表
└── README.md                          # 项目文档
```

## 数据库表结构

### questions 表（题目表）
| 字段名 | 类型 | 主键 | 说明 |
|--------|------|------|------|
| id | INTEGER | √ | 题目 ID |
| category | TEXT | | 题目分类（基础语法、Flask框架等） |
| title | TEXT | | 题干 |
| option_a | TEXT | | 选项 A |
| option_b | TEXT | | 选项 B |
| option_c | TEXT | | 选项 C |
| option_d | TEXT | | 选项 D |
| difficulty | TEXT | | 难度（简单、中等、困难） |
| is_high_frequency | INTEGER | | 是否高频题（1=是，0=否） |

### answers 表（答案解析表）
| 字段名 | 类型 | 主键 | 说明 |
|--------|------|------|------|
| id | INTEGER | √ | 解析 ID |
| question_id | INTEGER | | 关联题目 ID（外键） |
| correct_answer | TEXT | | 正确答案（如 A、AB） |
| analysis | TEXT | | 答案解析 |
| knowledge_point | TEXT | | 涉及知识点 |

### user_records 表（答题记录表）
| 字段名 | 类型 | 主键 | 说明 |
|--------|------|------|------|
| id | INTEGER | √ | 记录 ID |
| question_id | INTEGER | | 关联题目 ID（外键） |
| user_answer | TEXT | | 用户答案 |
| is_correct | INTEGER | | 是否正确（1=是，0=否） |
| answer_time | TIMESTAMP | | 答题时间 |
| exam_id | INTEGER | | 模拟面试 ID（0=非模拟面试） |

### favorite 表（收藏表）
| 字段名 | 类型 | 主键 | 说明 |
|--------|------|------|------|
| id | INTEGER | √ | 收藏 ID |
| question_id | INTEGER | | 关联题目 ID（外键） |
| collect_time | TIMESTAMP | | 收藏时间 |

## 安装与配置

### 环境要求
- Python 3.8 或以上
- pip 包管理工具

### 安装步骤

1. **进入项目目录**
   ```bash
   cd d:\wfx\pthon大作业\Python-System
   ```

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **验证本地资源**
   ```bash
   python run.py
   ```
   应用会自动创建必要的目录和日志文件。

## 运行应用

### 启动服务器
```bash
python run.py
```

### 访问应用
打开浏览器，访问：`http://127.0.0.1:5000`

### 主要功能
- **首页**：查看学习进度摘要
- **题库**：按分类浏览题目，搜索功能
- **答题**：做题并自动保存答题记录
- **模拟面试**：20 道题目，30 分钟倒计时
- **错题本**：查看答错的题目
- **收藏**：管理收藏的题目
- **进度页**：查看学习统计与分析

## 单元测试

### 运行测试
```bash
pytest -q
```

### 测试覆盖范围

| 测试文件 | 测试内容 |
|---------|--------|
| test_dbmanager.py | 数据库增删改查、事务回滚 |
| test_question_bank.py | 题目查询、分类浏览、搜索功能 |
| test_user_progress.py | 答题记录、进度计算、收藏管理 |
| test_interview_simulator.py | 模拟面试生成、记录保存 |

### 期望结果
全部 8 个测试通过

```
....... [100%]
8 passed in 0.50s
```

## 代码规范

### 命名规范
- **类名**：大驼峰，如 `QuestionBank`
- **方法/变量名**：小驼峰，如 `get_question_by_id`
- **常量**：全大写 + 下划线，如 `DB_PATH`
- **模块名**：小写 + 下划线，如 `question_bank.py`

### 代码格式
- 使用 **4 个空格**缩进（禁用制表符）
- 每行代码不超过 **80 字符**
- 所有类和方法添加文档字符串（Docstring）

### 文档字符串示例
```python
class QuestionBank:
    """
    题库管理类，实现题目查询、分类、搜索功能
    
    Attributes:
        db_manager (DBManager): 数据库操作实例
        category_list (list): 题目分类列表
    """
    def get_question_by_id(self, question_id: int) -> dict:
        """
        根据题目 ID 查询题目详情
        
        Args:
            question_id (int): 题目 ID
            
        Returns:
            dict: 题目详情（含答案和解析）
        """
        pass
```

## 核心设计原则

1. **单机化**：禁用网络请求，所有资源本地存放
2. **面向对象**：业务逻辑封装为类，避免全局变量
3. **低耦合**：模块间通过接口通信
4. **可测试性**：所有核心类均有单元测试
5. **可追溯性**：所有操作都有日志记录

## 常见操作示例

### 添加新题目
```python
from app.database.db_manager import DBManager

db = DBManager()
db.execute(
    "INSERT INTO questions (category, title, option_a, option_b, option_c, option_d, difficulty, is_high_frequency) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ('Python基础', '什么是 Python？', '编程语言', '编程工具', '框架', '库', '简单', 1)
)
db.commit()
```

### 查询题目
```python
from app.core.question_bank import QuestionBank
from app.database.db_manager import DBManager

db = DBManager()
qb = QuestionBank(db)
questions = qb.get_questions_by_category('Python基础')
for q in questions:
    print(q['title'])
```

### 查看学习进度
```python
from app.core.user_progress import UserProgress
from app.database.db_manager import DBManager

db = DBManager()
up = UserProgress(db)
progress = up.get_progress()
print(f"总答题数：{progress['total']}")
print(f"正确率：{progress['accuracy']}")
print(f"各分类进度：{progress['category_count']}")
```

### 获取错题本
```python
error_questions = up.get_error_questions()
for q in error_questions:
    print(f"{q['title']} - 正确答案：{q['correct_answer']}")
```

## 日志说明

应用日志写入 `logs/interview_system.log`，同时输出到控制台：

```
2025-12-25 22:59:04,945 - INFO - Flask 应用初始化成功
2025-12-25 22:59:05,123 - INFO - 成功查询题目 ID 1
2025-12-25 22:59:05,456 - ERROR - 查询题目失败：数据库连接错误
```

### 日志级别
- **INFO**：正常操作信息
- **WARNING**：警告信息（如资源不存在但已自动创建）
- **ERROR**：错误信息（异常、失败操作）
- **DEBUG**：调试信息

## 常见问题排查

### 问题 1：ModuleNotFoundError: No module named 'flask'
**解决方案**：运行 `pip install -r requirements.txt` 安装依赖

### 问题 2：UnicodeDecodeError in conftest.py
**解决方案**：确保所有 Python 文件使用 **UTF-8 编码**保存（非 GBK/CP936）

### 问题 3：FileNotFoundError for static resources
**解决方案**：下载 Bootstrap 和 jQuery 到 `app/static/css/` 和 `app/static/js/`

### 问题 4：database/interview.db 文件未找到
**解决方案**：应用首次运行时会自动创建 `database/` 目录和数据库文件

### 问题 5：模板页面不显示
**解决方案**：创建 `app/templates/` 目录下的 HTML 模板文件（index.html、question_list.html 等）

## 依赖包列表

| 包名 | 版本 | 用途 |
|-----|------|------|
| Flask | 2.3.3 | Web 框架 |
| Jinja2 | 3.1.2 | 模板引擎 |
| Werkzeug | 2.3.7 | WSGI 工具库 |
| click | 8.1.7 | CLI 工具库 |
| blinker | 1.6.3 | 信号支持 |
| pytest | 7.4.0 | 测试框架 |

## 后续功能规划

- [ ] 用户认证（用户名/密码）
- [ ] 题目难度筛选与过滤
- [ ] 自定义模拟面试配置
- [ ] 导出进度报告（PDF/CSV）
- [ ] 批量导入题目（Excel）
- [ ] 深色模式界面
- [ ] 题目标签管理
- [ ] 学习计划功能

## 团队协作说明

### 分工职责
- **开发负责人 & 框架核心工程师（A）**：架构设计、核心类开发、代码审核
- **数据库工程师（B）**：DBManager 开发、数据库表设计、数据导入
- **前端工程师（C）**：Jinja2 模板、前后端联调、UI 优化
- **测试工程师（D）**：单元测试、功能测试、BUG 定位

### 沟通计划
- **每日站会**：上午 9:30，同步进度、暴露风险
- **周例会**：每周五下午 3:00，总结周进度、调整计划
- **代码审核**：每天下班前，提交代码到 Git，A 负责审核

## 版本历史

### v1.0（2025-12-25）
- 完成三层架构设计
- 实现核心业务类（题库、用户进度、模拟面试）
- 完成 Flask 路由与视图
- 实现 SQLite 数据库封装
- 编写单元测试（覆盖率 80%+）
- 项目交付

## 许可证

MIT License

## 联系方式

开发团队 - Python 面试题学习系统项目
