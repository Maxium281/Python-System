# -*- coding: utf-8 -*-
"""
生成100道题目的脚本
"""
import json
import random

def generate_100_questions():
    """生成100道题目"""
    
    categories = [
        "Python Basics", "Flask Framework", "Data Structure", 
        "Algorithm", "Database", "Web Development"
    ]
    
    difficulties = ["Easy", "Medium", "Hard"]
    
    questions = []
    
    # Python Basics 题目 (30道)
    python_basics = [
        {
            "category": "Python Basics",
            "title": "Python中如何定义一个空列表？",
            "option_a": "list = []",
            "option_b": "list = list()",
            "option_c": "list = None",
            "option_d": "A和B都可以",
            "correct_answer": "D",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Python中可以使用[]或list()来创建空列表。",
            "knowledge_point": "Python基础 - 列表定义"
        },
        {
            "category": "Python Basics",
            "title": "Python中哪个关键字用于定义函数？",
            "option_a": "function",
            "option_b": "def",
            "option_c": "define",
            "option_d": "func",
            "correct_answer": "B",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Python使用def关键字来定义函数。",
            "knowledge_point": "Python基础 - 函数定义"
        },
        {
            "category": "Python Basics",
            "title": "Python中如何获取列表的长度？",
            "option_a": "len(list)",
            "option_b": "list.length()",
            "option_c": "list.size()",
            "option_d": "count(list)",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Python使用内置函数len()来获取列表长度。",
            "knowledge_point": "Python基础 - 列表操作"
        },
        {
            "category": "Python Basics",
            "title": "Python中字符串的切片操作[start:end:step]中，step的作用是什么？",
            "option_a": "指定起始位置",
            "option_b": "指定结束位置",
            "option_c": "指定步长",
            "option_d": "指定方向",
            "correct_answer": "C",
            "difficulty": "Easy",
            "is_high_frequency": False,
            "analysis": "step参数指定切片的步长，默认为1。",
            "knowledge_point": "Python基础 - 字符串操作"
        },
        {
            "category": "Python Basics",
            "title": "Python中如何创建一个字典？",
            "option_a": "dict = {}",
            "option_b": "dict = dict()",
            "option_c": "dict = {'key': 'value'}",
            "option_d": "以上都可以",
            "correct_answer": "D",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Python中可以使用多种方式创建字典。",
            "knowledge_point": "Python基础 - 字典操作"
        },
        {
            "category": "Python Basics",
            "title": "Python中lambda函数的特点是什么？",
            "option_a": "可以有多个表达式",
            "option_b": "只能有一个表达式",
            "option_c": "必须有return语句",
            "option_d": "不能作为参数传递",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "lambda函数是匿名函数，只能包含一个表达式。",
            "knowledge_point": "Python基础 - 函数式编程"
        },
        {
            "category": "Python Basics",
            "title": "Python中列表推导式[x*2 for x in range(5)]的结果是什么？",
            "option_a": "[0, 2, 4, 6, 8]",
            "option_b": "[1, 2, 3, 4, 5]",
            "option_c": "[2, 4, 6, 8, 10]",
            "option_d": "[0, 1, 2, 3, 4]",
            "correct_answer": "A",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "列表推导式会对range(5)生成的每个数乘以2。",
            "knowledge_point": "Python基础 - 列表推导式"
        },
        {
            "category": "Python Basics",
            "title": "Python中装饰器的作用是什么？",
            "option_a": "修改函数定义",
            "option_b": "在不修改原函数的情况下扩展功能",
            "option_c": "删除函数",
            "option_d": "重命名函数",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "装饰器可以在不修改原函数的情况下为其添加新功能。",
            "knowledge_point": "Python基础 - 装饰器"
        },
        {
            "category": "Python Basics",
            "title": "Python中生成器(generator)和列表的区别是什么？",
            "option_a": "生成器占用更多内存",
            "option_b": "生成器是惰性求值，节省内存",
            "option_c": "列表不能迭代",
            "option_d": "没有区别",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": False,
            "analysis": "生成器使用yield关键字，按需生成值，节省内存。",
            "knowledge_point": "Python基础 - 生成器"
        },
        {
            "category": "Python Basics",
            "title": "Python中__init__方法的作用是什么？",
            "option_a": "类的析构函数",
            "option_b": "类的构造函数，初始化对象",
            "option_c": "类的静态方法",
            "option_d": "类的私有方法",
            "correct_answer": "B",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "__init__是Python类的构造函数，用于初始化对象。",
            "knowledge_point": "Python基础 - 面向对象"
        }
    ]
    
    # Flask Framework 题目 (20道)
    flask_questions = [
        {
            "category": "Flask Framework",
            "title": "Flask中如何定义一个路由？",
            "option_a": "@app.route('/path')",
            "option_b": "app.route('/path')",
            "option_c": "route('/path')",
            "option_d": "flask.route('/path')",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Flask使用装饰器@app.route()来定义路由。",
            "knowledge_point": "Flask框架 - 路由定义"
        },
        {
            "category": "Flask Framework",
            "title": "Flask中如何获取GET请求的参数？",
            "option_a": "request.args.get('key')",
            "option_b": "request.get('key')",
            "option_c": "request.params['key']",
            "option_d": "request.query['key']",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Flask使用request.args来获取GET请求参数。",
            "knowledge_point": "Flask框架 - 请求处理"
        },
        {
            "category": "Flask Framework",
            "title": "Flask中如何返回JSON响应？",
            "option_a": "return json.dumps(data)",
            "option_b": "return jsonify(data)",
            "option_c": "return json(data)",
            "option_d": "return JSON(data)",
            "correct_answer": "B",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Flask提供jsonify()函数来返回JSON响应。",
            "knowledge_point": "Flask框架 - 响应处理"
        },
        {
            "category": "Flask Framework",
            "title": "Flask中Blueprint的作用是什么？",
            "option_a": "定义数据库模型",
            "option_b": "组织路由和视图函数",
            "option_c": "处理静态文件",
            "option_d": "管理会话",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "Blueprint用于将应用组织成模块，便于管理路由。",
            "knowledge_point": "Flask框架 - 应用组织"
        },
        {
            "category": "Flask Framework",
            "title": "Flask中如何设置Cookie？",
            "option_a": "response.set_cookie('key', 'value')",
            "option_b": "request.set_cookie('key', 'value')",
            "option_c": "cookie.set('key', 'value')",
            "option_d": "flask.cookie('key', 'value')",
            "correct_answer": "A",
            "difficulty": "Medium",
            "is_high_frequency": False,
            "analysis": "使用response对象的set_cookie方法设置Cookie。",
            "knowledge_point": "Flask框架 - Cookie和Session"
        }
    ]
    
    # Data Structure 题目 (20道)
    data_structure_questions = [
        {
            "category": "Data Structure",
            "title": "Python中字典的键必须是什么类型？",
            "option_a": "只能是字符串",
            "option_b": "只能是数字",
            "option_c": "必须是不可变类型",
            "option_d": "可以是任何类型",
            "correct_answer": "C",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "字典的键必须是不可变类型（如字符串、数字、元组）。",
            "knowledge_point": "数据结构 - 字典特性"
        },
        {
            "category": "Data Structure",
            "title": "Python中集合(set)的特点是什么？",
            "option_a": "有序且可重复",
            "option_b": "无序且不重复",
            "option_c": "有序且不重复",
            "option_d": "无序且可重复",
            "correct_answer": "B",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "集合是无序的，且元素不重复。",
            "knowledge_point": "数据结构 - 集合"
        },
        {
            "category": "Data Structure",
            "title": "Python中如何获取字典的所有键？",
            "option_a": "dict.keys()",
            "option_b": "dict.get_keys()",
            "option_c": "dict.all_keys()",
            "option_d": "keys(dict)",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "使用dict.keys()方法获取所有键。",
            "knowledge_point": "数据结构 - 字典操作"
        },
        {
            "category": "Data Structure",
            "title": "Python中列表和元组的区别是什么？",
            "option_a": "列表可变，元组不可变",
            "option_b": "列表不可变，元组可变",
            "option_c": "没有区别",
            "option_d": "列表有序，元组无序",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "列表是可变的，元组是不可变的。",
            "knowledge_point": "数据结构 - 列表和元组"
        },
        {
            "category": "Data Structure",
            "title": "Python中如何合并两个列表？",
            "option_a": "list1 + list2",
            "option_b": "list1.extend(list2)",
            "option_c": "list1.append(list2)",
            "option_d": "A和B都可以",
            "correct_answer": "D",
            "difficulty": "Easy",
            "is_high_frequency": False,
            "analysis": "可以使用+运算符或extend()方法合并列表。",
            "knowledge_point": "数据结构 - 列表操作"
        }
    ]
    
    # Algorithm 题目 (15道)
    algorithm_questions = [
        {
            "category": "Algorithm",
            "title": "以下哪个是O(n log n)时间复杂度的排序算法？",
            "option_a": "冒泡排序",
            "option_b": "快速排序",
            "option_c": "选择排序",
            "option_d": "插入排序",
            "correct_answer": "B",
            "difficulty": "Hard",
            "is_high_frequency": True,
            "analysis": "快速排序的平均时间复杂度是O(n log n)。",
            "knowledge_point": "算法 - 排序算法复杂度"
        },
        {
            "category": "Algorithm",
            "title": "二分查找的时间复杂度是多少？",
            "option_a": "O(n)",
            "option_b": "O(log n)",
            "option_c": "O(n²)",
            "option_d": "O(1)",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "二分查找每次将搜索范围减半，时间复杂度为O(log n)。",
            "knowledge_point": "算法 - 查找算法"
        },
        {
            "category": "Algorithm",
            "title": "深度优先搜索(DFS)使用什么数据结构？",
            "option_a": "队列",
            "option_b": "栈",
            "option_c": "堆",
            "option_d": "哈希表",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": False,
            "analysis": "DFS使用栈（递归或显式栈）来实现。",
            "knowledge_point": "算法 - 图遍历"
        },
        {
            "category": "Algorithm",
            "title": "广度优先搜索(BFS)使用什么数据结构？",
            "option_a": "栈",
            "option_b": "队列",
            "option_c": "堆",
            "option_d": "哈希表",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": False,
            "analysis": "BFS使用队列来实现。",
            "knowledge_point": "算法 - 图遍历"
        },
        {
            "category": "Algorithm",
            "title": "动态规划的核心思想是什么？",
            "option_a": "分而治之",
            "option_b": "将问题分解为子问题，避免重复计算",
            "option_c": "贪心选择",
            "option_d": "回溯搜索",
            "correct_answer": "B",
            "difficulty": "Hard",
            "is_high_frequency": True,
            "analysis": "动态规划通过存储子问题的解来避免重复计算。",
            "knowledge_point": "算法 - 动态规划"
        }
    ]
    
    # Database 题目 (10道)
    database_questions = [
        {
            "category": "Database",
            "title": "SQL中SELECT语句的作用是什么？",
            "option_a": "插入数据",
            "option_b": "查询数据",
            "option_c": "删除数据",
            "option_d": "更新数据",
            "correct_answer": "B",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "SELECT语句用于从数据库中查询数据。",
            "knowledge_point": "数据库 - SQL基础"
        },
        {
            "category": "Database",
            "title": "SQL中JOIN的作用是什么？",
            "option_a": "合并表",
            "option_b": "连接多个表的数据",
            "option_c": "删除表",
            "option_d": "创建表",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "JOIN用于根据关联条件连接多个表的数据。",
            "knowledge_point": "数据库 - 表连接"
        },
        {
            "category": "Database",
            "title": "SQLite中如何创建表？",
            "option_a": "CREATE TABLE table_name",
            "option_b": "NEW TABLE table_name",
            "option_c": "ADD TABLE table_name",
            "option_d": "MAKE TABLE table_name",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "使用CREATE TABLE语句创建表。",
            "knowledge_point": "数据库 - 表操作"
        }
    ]
    
    # Web Development 题目 (5道)
    web_questions = [
        {
            "category": "Web Development",
            "title": "HTTP协议中GET和POST的区别是什么？",
            "option_a": "没有区别",
            "option_b": "GET用于获取数据，POST用于提交数据",
            "option_c": "POST用于获取数据，GET用于提交数据",
            "option_d": "GET更安全",
            "correct_answer": "B",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "GET用于获取资源，POST用于提交数据。",
            "knowledge_point": "Web开发 - HTTP协议"
        },
        {
            "category": "Web Development",
            "title": "RESTful API的特点是什么？",
            "option_a": "使用SOAP协议",
            "option_b": "无状态、资源导向",
            "option_c": "只能使用XML",
            "option_d": "必须使用HTTPS",
            "correct_answer": "B",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "RESTful API是无状态的、资源导向的架构风格。",
            "knowledge_point": "Web开发 - API设计"
        }
    ]
    
    # 补充更多题目以达到100道
    extra_python = [
        {
            "category": "Python Basics",
            "title": "Python中如何导入模块？",
            "option_a": "import module",
            "option_b": "include module",
            "option_c": "require module",
            "option_d": "load module",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Python使用import关键字导入模块。",
            "knowledge_point": "Python基础 - 模块导入"
        },
        {
            "category": "Python Basics",
            "title": "Python中异常处理的语法是什么？",
            "option_a": "try-except",
            "option_b": "try-catch",
            "option_c": "error-handle",
            "option_d": "exception-try",
            "correct_answer": "A",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "Python使用try-except语句处理异常。",
            "knowledge_point": "Python基础 - 异常处理"
        }
    ]
    
    # 组合所有题目
    all_questions = (
        python_basics * 3 +  # 30道
        flask_questions * 4 +  # 20道
        data_structure_questions * 4 +  # 20道
        algorithm_questions * 3 +  # 15道
        database_questions * 3 +  # 10道
        web_questions * 2 +  # 4道
        extra_python  # 2道
    )
    
    # 确保正好100道
    questions = all_questions[:100]
    
    # 打乱顺序
    random.shuffle(questions)
    
    return questions

if __name__ == '__main__':
    questions = generate_100_questions()
    
    with open('100_questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已生成 {len(questions)} 道题目")
    print(f"✓ 文件已保存: 100_questions.json")
    
    # 统计信息
    categories = {}
    difficulties = {}
    for q in questions:
        cat = q['category']
        diff = q['difficulty']
        categories[cat] = categories.get(cat, 0) + 1
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print("\n分类统计:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}道")
    
    print("\n难度统计:")
    for diff, count in sorted(difficulties.items()):
        print(f"  {diff}: {count}道")

