#coding=utf8
from datetime import timedelta
from datetime import datetime

class BasePlanIterator(object):

    header = ["计划", "时间"]
    def __init__(self, from_date, end_date, delta=1, skip_weekend=True):
        self._from_date = from_date
        self._end_date = end_date
        self._timedelta = timedelta(days=delta)
        self._skip_weekend = skip_weekend
        self.date_gener = self._date_generator()

    def _date_generator(self):
        from_date, end_date = self._from_date, self._end_date
        while from_date <= end_date:
            # 忽略周末
            if self._skip_weekend and from_date.weekday() in [6]:
                from_date += self._timedelta
                continue
            yield from_date.strftime("%Y-%m-%d")
            from_date += self._timedelta

    def get_row_str(self, cols):
        lst = [ "|" ]
        for c in cols:
            if not isinstance(c, basestring):
                print c, "is not str", "it's ", type(c)
                raise
            lst.append(c)
            lst.append(" |")
        return "".join(lst)

    def __iter__(self):
        return self

    def next(self):
        raise NotImplementedError

    def as_text(self):
        lines = [self.get_row_str(self.header), self.get_row_str(["-"] * len(self.header))]
        for line in self:
            lines.append(line)
        return '\n'.join(lines)
