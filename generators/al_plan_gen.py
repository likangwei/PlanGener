#coding=utf8
import os
import datetime
import json
import jinja2
from generators.base_plan_gen import BasePlanIterator
from itertools import cycle
from jinja2 import Template


class Question(object):
    id = None
    title = None
    slug = None
    difficulty = None
    status = None
    rawSlug = None
    topics = None
    paid_only = False
    def __str__(self):
        return "%s.%s" % (self.id, self.slug.replace("-", "_"))


class Topic(object):
    name = None
    questions = None

    @property
    def finish_count(self):
        return len([x for x in self.questions if x.status == "ac"])

    @property
    def finish_percent(self):
        return 100 * self.finish_count / len(self.questions)

    def __str__(self):
        return "%s (fp: %s/%s=%.2f)" % (self.name, self.finish_count, len(self.questions), self.finish_percent)


class AlgorithmsIterator(BasePlanIterator):
    
    work_space = "/Users/likangwei/workspace/leetcode/go"

    header = ["日期", "作业", "完成时间", "是否Accept", "是否临摹", "是否总结"]
    def __init__(self, *args, **kwargs):
        super(AlgorithmsIterator, self).__init__(*args, **kwargs)
        self.clz_gener = self.clz_generator()

    def next(self):
        cols = [self.date_gener.next(), self.clz_gener.next(), "0", "0", "0"]
        rst = self.get_row_str(cols)
        self.date_gener.next()
        return rst

    def build_code_file(self, question):
        #  {
        #   "status": null,
        #   "stat": {
        #     "total_acs": 1329,
        #     "question__title": "Find K-th Smallest Pair Distance",
        #     "is_new_question": true,
        #     "question__article__slug": "find-k-th-smallest-pair-distance",
        #     "total_submitted": 5860,
        #     "question__title_slug": "find-k-th-smallest-pair-distance",
        #     "question__article__live": true,
        #     "question__hide": false,
        #     "question_id": 719
        #   },
        #   "is_favor": false,
        #   "paid_only": false,
        #   "difficulty": {
        #     "level": 3
        #   },
        #   "frequency": 0,
        #   "progress": 0
        # },
        # print detail
        dir_name = '%s_%s' % (str(question.id).rjust(3, "0"), question.slug)
        file_name = '%s_%s.go' % (str(question.id).rjust(3, "0"), question.slug)
        dir_name = os.path.join(self.work_space, dir_name)
        file_name = os.path.join(dir_name, file_name)
        cmd = "mkdir -p %s" % dir_name
        print cmd
        os.system(cmd)
        template = Template(open("/Users/likangwei/Dropbox/workspace/PycharmProjects/wiznote/generators/template/ai.go").read())
        txt = template.render(slug=question.rawSlug, tags=", ".join(question.topics))
        if not os.path.exists(file_name) or (raw_input("是否覆盖%s? \n y/N  " % file_name) == "Y"):
            open(file_name, "w").write(txt)

    def get_topics(self):
        questions = self.get_questions()
        data = open("generators/leetcode.tags.json").read()
        data = json.loads(data)
        topics = data["topics"]
        rst = []
        for row in topics:
            slug = row["slug"]
            topic = Topic()
            topic.name = slug
            topic.questions = []
            for qid in row["questions"]:
                q = questions[qid]
                q.topics.add(topic.name)
                topic.questions.append(q)
            rst.append(topic)
        return rst

    def get_questions(self):
        data = open("generators/leetcode.json").read()
        data = json.loads(data)
        questions = {}
        for row in data["stat_status_pairs"]:
            stat = row["stat"]
            q = Question()
            q.id = stat["question_id"]
            q.title = stat["question__title"]
            q.rawSlug = stat["question__title_slug"]
            q.slug = stat["question__title_slug"].replace("-", "_")
            q.difficulty = row["difficulty"]["level"]
            q.status = row["status"]
            q.paid_only = row["paid_only"]
            q.topics = set()
            questions[q.id] = q
        return questions

    def clz_generator(self):
        def cmp(x, y):
            rst = x.finish_percent - y.finish_percent
            if rst == 0:
                rst = len(y.questions) - len(x.questions)
            return rst

        topics = self.get_topics()
        topics.sort(cmp=cmp)
        for t in topics:
            print str(t)

        has_yield = set()
        while True:
            for topic in topics:
                for q in topic.questions:
                    if q.status != "ac" and q.id not in has_yield and not q.paid_only:
                        has_yield.add(q.id)
                        self.build_code_file(q)
                        yield str(q)
                        break
