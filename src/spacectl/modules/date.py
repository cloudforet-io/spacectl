import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper


class Task(BaseTask):

    @execute_wrapper
    def execute(self):
        base_date = self.spec.get('base_date')
        
        if base_date:
            dt = utils.parse_timediff_query(base_date)
        else:
            dt = datetime.utcnow()

        self.output = {
            'year': dt.strftime('%Y'),
            'year-1y': self._change_time(dt, '%Y', years=-1),
            'year-2y': self._change_time(dt, '%Y', years=-2),
            'year-3y': self._change_time(dt, '%Y', years=-3),
            'month': dt.strftime('%Y-%m'),
            'month+1m': self._change_time(dt, '%Y-%m', months=+1),
            'month-1m': self._change_time(dt, '%Y-%m', months=-1),
            'month-2m': self._change_time(dt, '%Y-%m', months=-2),
            'month-3m': self._change_time(dt, '%Y-%m', months=-3),
            'month-4m': self._change_time(dt, '%Y-%m', months=-4),
            'month-5m': self._change_time(dt, '%Y-%m', months=-5),
            'month-6m': self._change_time(dt, '%Y-%m', months=-6),
            'month-7m': self._change_time(dt, '%Y-%m', months=-7),
            'month-8m': self._change_time(dt, '%Y-%m', months=-8),
            'month-9m': self._change_time(dt, '%Y-%m', months=-9),
            'month-10m': self._change_time(dt, '%Y-%m', months=-10),
            'month-11m': self._change_time(dt, '%Y-%m', months=-11),
            'date': dt.strftime('%Y-%m-%d'),
            'date+1d': self._change_time(dt, '%Y-%m-%d', days=+1),
            'date-1d': self._change_time(dt, '%Y-%m-%d', days=-1),
            'date-2d': self._change_time(dt, '%Y-%m-%d', days=-2),
            'date-3d': self._change_time(dt, '%Y-%m-%d', days=-3),
            'date-4d': self._change_time(dt, '%Y-%m-%d', days=-4),
            'date-5d': self._change_time(dt, '%Y-%m-%d', days=-5),
            'date-6d': self._change_time(dt, '%Y-%m-%d', days=-6),
            'date-7d': self._change_time(dt, '%Y-%m-%d', days=-7),
            'date-8d': self._change_time(dt, '%Y-%m-%d', days=-8),
            'date-9d': self._change_time(dt, '%Y-%m-%d', days=-9),
            'date-10d': self._change_time(dt, '%Y-%m-%d', days=-10),
            'date-11d': self._change_time(dt, '%Y-%m-%d', days=-11),
            'date-12d': self._change_time(dt, '%Y-%m-%d', days=-12),
            'date-13d': self._change_time(dt, '%Y-%m-%d', days=-13),
            'date-14d': self._change_time(dt, '%Y-%m-%d', days=-14),
            'date-15d': self._change_time(dt, '%Y-%m-%d', days=-15),
            'year_start_month': dt.replace(month=1, day=1).strftime('%Y-%m'),
            'month_start_date': dt.replace(day=1).strftime('%Y-%m-%d'),
            'datetime': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'timestamp': int(time.time())
        }

    @staticmethod
    def _change_time(dt: datetime, fmt, **kwargs):
        dt = dt + relativedelta(**kwargs)
        return dt.strftime(fmt)

