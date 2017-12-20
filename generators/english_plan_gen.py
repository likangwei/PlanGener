#coding=utf8
from generators.base_plan_gen import BasePlanIterator
from collections import OrderedDict

class EnglishGenerator(BasePlanIterator):
    
    header = ["日期", "课程", "状态"]
    def __init__(self, *args, **kwargs):
        super(EnglishGenerator, self).__init__(*args, **kwargs)
        self.clz_gener = self.clz_generator()
        self.clzs = OrderedDict()
        self.clzs["level2"] = [["unit1", 19, 30], 
                               ["unit2", 20, 30],
                               ["unit3", 0, 24],
                               ["考试", 0, 1]
                              ]

    def next(self):
        return self.get_row_str([self.date_gener.next(), self.clz_gener.next(), "未完成"])

    def clz_generator(self):
        m = self.clzs
        lessions_per_day = 3
        has_count = 0
        cache = OrderedDict()
        for level in m:
            for unit, has_finish, total in m[level]:
                for i in range(has_finish+1, total+1):
                    page_num = (i-1) / 6 + 1
                    clz_num = i - ((page_num-1)*6)
                    unit_dict = cache.setdefault(level, OrderedDict())
                    page_dict = unit_dict.setdefault(unit, OrderedDict())
                    lession_lst = page_dict.setdefault(page_num, [])
                    lession_lst.append(clz_num)
                    has_count += 1
                    if has_count == 3:
                        yield self.getString(cache)
                        cache = OrderedDict()
                        has_count = 0
        if has_count:
            yield self.getString(cache)

    def getString(self, m):
        rst = []
        for level in m:
            for unit in m[level]:
                for page in m[level][unit]:
                    rst.append("%s:%s:page:%s, clz:%s" % (level, unit, page, str(m[level][unit][page])))
        return "英语流利说: " + ",".join(rst)


