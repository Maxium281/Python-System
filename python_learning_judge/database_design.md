\# SQLite 数据库设计文档（含判题系统）



\## 1. 项目背景

本数据库服务于 Python 学习教辅软件，

学习目标依据 \*\*全国计算机等级考试二级 Python\*\* 官方考试大纲。



系统提供：

\- 知识点学习

\- 练习题训练

\- 类 PTA / 力扣的 Python 代码自动评测功能



数据库类型：SQLite（单机版）



---



\## 2. 表结构设计



\### 2.1 users（用户表）

\- user\_id：主键

\- username：用户名

\- password：密码

\- role：用户角色



默认内置用户：

\- 用户名：x

\- 密码：1



---



\### 2.2 syllabus（学习大纲表）

用于存储公开学习大纲信息。



---



\### 2.3 knowledge\_points（知识点表）

与学习大纲关联，构建教学知识体系。



---



\### 2.4 learning\_progress（学习进度表）

记录用户对知识点的学习状态。



---



\### 2.5 programming\_problems（编程题表）

存储可提交代码的编程题，功能类似 PTA / 力扣。



---



\### 2.6 test\_cases（测试用例表）

存储示例与隐藏测试用例，用于自动判题。



---



\### 2.7 code\_submissions（代码提交记录表）

记录用户每一次代码提交与评测结果。



---



\## 3. 判题功能设计说明



1\. 用户提交 Python 代码

2\. 后端将代码保存为临时文件

3\. 读取 test\_cases 中的测试用例

4\. 使用 subprocess 调用本地 Python 解释器

5\. 捕获输出与异常信息

6\. 比对 expected\_output

7\. 得出判题结果（Accepted / Wrong Answer / Runtime Error）

8\. 结果写入 code\_submissions 表



---



\## 4. 设计特点

\- 完全单机版，无服务器

\- SQLite 轻量数据库

\- 支持教学与自动评测

\- 易与 Flask 框架集成

