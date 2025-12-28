# -*- coding: utf-8 -*-
"""
批量导入题目脚本
支持从JSON文件批量导入题目到数据库
"""
import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.database.db_manager import DBManager
from app.core.question_bank import QuestionBank
from app.utils.logger import Logger

logger = Logger()


def import_from_json(json_file: str):
    """从JSON文件导入题目"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("错误：JSON文件应该包含一个题目数组")
            return False
        
        db_manager = DBManager()
        
        success_count = 0
        fail_count = 0
        
        print(f"\n开始导入 {len(data)} 道题目...\n")
        
        for idx, question_data in enumerate(data, 1):
            try:
                # 验证必需字段
                required_fields = ['title', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
                missing_fields = [f for f in required_fields if f not in question_data]
                
                if missing_fields:
                    print(f"题目 {idx}: 缺少必需字段 {missing_fields}，跳过")
                    fail_count += 1
                    continue
                
                # 设置默认值
                category = question_data.get('category', 'Python Basics')
                title = question_data.get('title', '')
                option_a = question_data.get('option_a', '')
                option_b = question_data.get('option_b', '')
                option_c = question_data.get('option_c', '')
                option_d = question_data.get('option_d', '')
                difficulty = question_data.get('difficulty', 'Easy')
                is_high_frequency = int(question_data.get('is_high_frequency', False))
                
                # 直接插入题目（不包含时间字段，因为数据库表可能没有）
                sql = """INSERT INTO questions 
                         (category, title, option_a, option_b, option_c, option_d, 
                          difficulty, is_high_frequency)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                
                cursor = db_manager.execute(sql, (
                    category, title, option_a, option_b, option_c, option_d, 
                    difficulty, is_high_frequency
                ))
                question_id = cursor.lastrowid
                
                # 插入答案
                correct_answer = question_data.get('correct_answer', '')
                analysis = question_data.get('analysis', '')
                knowledge_point = question_data.get('knowledge_point', '')
                
                if correct_answer:
                    answer_sql = """INSERT INTO answers 
                                    (question_id, correct_answer, analysis, knowledge_point)
                                    VALUES (?, ?, ?, ?)"""
                    db_manager.execute(answer_sql, (
                        question_id, correct_answer, analysis, knowledge_point
                    ))
                
                db_manager.commit()
                
                success_count += 1
                if idx % 10 == 0:
                    print(f"已导入 {idx}/{len(data)} 道题目...")
                    
            except Exception as e:
                fail_count += 1
                db_manager.rollback()
                print(f"题目 {idx}: 导入失败 - {e}")
        
        print(f"\n导入完成！")
        print(f"成功: {success_count} 道")
        print(f"失败: {fail_count} 道")
        
        db_manager.close()
        return True
        
    except FileNotFoundError:
        print(f"错误：文件不存在 - {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"错误：JSON格式错误 - {e}")
        return False
    except Exception as e:
        print(f"错误：{e}")
        return False


def create_sample_json(output_file: str = 'sample_questions.json'):
    """创建示例JSON文件"""
    sample_questions = [
        {
            "category": "Python Basics",
            "title": "Python中如何定义一个列表？",
            "option_a": "list = []",
            "option_b": "list = list()",
            "option_c": "list = [1, 2, 3]",
            "option_d": "以上都可以",
            "correct_answer": "D",
            "difficulty": "Easy",
            "is_high_frequency": True,
            "analysis": "在Python中，可以使用多种方式定义列表：空列表[]、list()函数、或直接包含元素。",
            "knowledge_point": "Python基础语法 - 列表定义"
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
            "knowledge_point": "Python基础语法 - 函数定义"
        },
        {
            "category": "Flask Framework",
            "title": "Flask中如何定义一个路由？",
            "option_a": "@app.route('/path')",
            "option_b": "app.route('/path')",
            "option_c": "route('/path')",
            "option_d": "flask.route('/path')",
            "correct_answer": "A",
            "difficulty": "Medium",
            "is_high_frequency": True,
            "analysis": "Flask使用装饰器@app.route()来定义路由。",
            "knowledge_point": "Flask框架 - 路由定义"
        },
        {
            "category": "Data Structure",
            "title": "Python中字典的键必须是什么类型？",
            "option_a": "只能是字符串",
            "option_b": "只能是数字",
            "option_c": "必须是不可变类型",
            "option_d": "可以是任何类型",
            "correct_answer": "C",
            "difficulty": "Medium",
            "is_high_frequency": False,
            "analysis": "字典的键必须是不可变类型（如字符串、数字、元组），不能是列表或字典等可变类型。",
            "knowledge_point": "数据结构 - 字典特性"
        },
        {
            "category": "Algorithm",
            "title": "以下哪个是O(n log n)时间复杂度的排序算法？",
            "option_a": "冒泡排序",
            "option_b": "快速排序",
            "option_c": "选择排序",
            "option_d": "插入排序",
            "correct_answer": "B",
            "difficulty": "Hard",
            "is_high_frequency": False,
            "analysis": "快速排序的平均时间复杂度是O(n log n)，是最常用的高效排序算法之一。",
            "knowledge_point": "算法 - 排序算法复杂度"
        }
    ]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_questions, f, ensure_ascii=False, indent=2)
    
    print(f"示例文件已创建: {output_file}")
    print(f"包含 {len(sample_questions)} 道示例题目")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("批量导入题目工具")
        print("\n使用方法:")
        print("  python batch_import_questions.py <json_file>  # 从JSON文件导入")
        print("  python batch_import_questions.py --sample     # 创建示例JSON文件")
        print("\nJSON文件格式:")
        print("  [")
        print("    {")
        print("      \"category\": \"Python Basics\",")
        print("      \"title\": \"题目内容\",")
        print("      \"option_a\": \"选项A\",")
        print("      \"option_b\": \"选项B\",")
        print("      \"option_c\": \"选项C\",")
        print("      \"option_d\": \"选项D\",")
        print("      \"correct_answer\": \"A\",")
        print("      \"difficulty\": \"Easy\",  # Easy/Medium/Hard")
        print("      \"is_high_frequency\": true,")
        print("      \"analysis\": \"解析内容\",")
        print("      \"knowledge_point\": \"知识点\"")
        print("    }")
        print("  ]")
        return
    
    if sys.argv[1] == '--sample':
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'sample_questions.json'
        create_sample_json(output_file)
    else:
        json_file = sys.argv[1]
        if not os.path.exists(json_file):
            print(f"错误：文件不存在 - {json_file}")
            print("提示：使用 --sample 参数创建示例文件")
            return
        
        import_from_json(json_file)


if __name__ == '__main__':
    main()

