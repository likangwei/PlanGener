#encoding=utf8
"""
此文件主要用来生成markdown计划

http://www.wiz.cn/feature-markdown.html

表格
| 为知笔记|更新 | 版本 |
|------------|-----------|--------|
| WizNote | Markdown| Latest |

"""
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from datetime import datetime
from generators.al_plan_gen import AlgorithmsIterator
from generators.english_plan_gen import EnglishGenerator

if __name__ == "__main__":
    from_date = datetime.strptime("2017-12-13", "%Y-%m-%d")
    end_date = datetime.strptime("2017-12-17", "%Y-%m-%d")
    al_iter = AlgorithmsIterator(from_date, end_date, skip_weekend=False)
    print al_iter.as_text()
    en_iter = EnglishGenerator(from_date, end_date, skip_weekend=False)
    print en_iter.as_text()
