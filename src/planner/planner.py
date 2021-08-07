from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, YEARLY
from random import randint
from typing import Tuple, List
from enum import Enum


class PlanPeriod(Enum):
    """Getting the needed period length for which plan is made

    Args:
        Enum (int): Integer value of needed period
    """
    day = relativedelta(days=1)
    week = relativedelta(weeks=1)
    month = relativedelta(months=1)
    year = relativedelta(years=1)


class Frequency(Enum):
    """Getting the frequency of posts
    Args:
        Enum (int): Getting the frequency of posts inside PlanPeriod 
    """
    daily = [DAILY]
    weekly = [WEEKLY]
    yearly = [YEARLY]


class Planner:
    """Planner class for obtaining of the dates inside Period and frequency bounds
    """

    def __init__(self, period: str = "week", timerange: List[Tuple[int, int]] = [], start_date: datetime = datetime.now(), frequency: str = "daily", min_max_interval: Tuple[int, int] = (3600, 7200)) -> None:
        """[summary]

        Args:
            period (str, optional): Period of planning. Could be "day", "week", "month" or "year" Defaults to "week".
            timerange (List[Tuple[int, int]], optional): The list of timeranges for planned time. Ex. [(10,12), (15, 19)]. Defaults to [].
            start_date (datetime, optional): Date of start planning. Defaults to datetime.now().
            frequency (str, optional): Frequency of planning inside of period. Defaults to "daily".
            min_max_interval (Tuple[int, int], optional): Mix and max interval between planned dates. Defaults to (3600, 7200).
        """
        self.start_date = self.__check_start_date(start_date)
        self.period = self.__get_period(period)
        self.timerange = self.__check_timerange(timerange)
        self.min_max_interval = self.__check_time_bounds(min_max_interval)
        self.frequency = frequency
        self.interval = self.__generate_intervals()
        self.post_intervals = self.__generate_post_intervals()

    def __check_start_date(self, start_date):
        if isinstance(start_date, datetime) is False:
            raise ValueError(
                'Start date should be in datetime format ', start_date)
        return start_date

    def __check_time_bounds(self, min_max_interval: Tuple[int, int]):

        def get_date(h, m, s): return datetime(2020, 1, 1, 0, 0,
                                               0) + timedelta(hours=h, minutes=m, seconds=s)

        start_p = 0
        time_range = []
        min_iterval, _ = min_max_interval

        for r in self.timerange:
            time_range.extend(list(r))

        for i in range(1, len(time_range), 1):
            tr = time_range[start_p:i+1]
            if tr[1] == 24:
                tr_h, tr_m, tr_s = 23, 59, 59
            else:
                tr_h = tr[1]
                tr_m = tr_s = 0

            delta = (get_date(tr_h, tr_m, tr_s) -
                     get_date(tr[0], 0, 0)).seconds

            if delta < min_iterval:
                raise ValueError(
                    f'Hours range ({tr}) too tight for min interval {min_iterval}')
            start_p = i

        return min_max_interval

    def __get_period(self, period: str) -> Tuple[datetime, datetime]:
        if isinstance(period, str) is False:
            raise ValueError('Period should be string ', period)
        if period not in PlanPeriod.__members__.keys():
            raise ValueError(
                f'Period key should be {", ".join(list(PlanPeriod.__members__.keys()))} only ', period)
        return (self.start_date, self.start_date + PlanPeriod[period].value)

    def __check_timerange(self, tr: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        allowed_hours = range(0, 24)

        if isinstance(tr, list) is False:
            raise ValueError('Timerange should be list of tuple ints')
        for r in tr:
            if len(r) != 2:
                raise ValueError(
                    'Timerange should contain start and end hour ', r)
            if r[0] > r[1]:
                raise ValueError('Start hour should be less than endhour ', r)
            for hour in r:
                if isinstance(hour, int) is False:
                    raise ValueError('Hour should be int ', r)
                if hour not in allowed_hours:
                    raise ValueError('Hour should be int from 0 to 24 ', r)
        return tr

    def __get_frequence(self, frequency: str) -> list:
        # todo: сделать фильтр для выходных и рабочих
        if isinstance(frequency, str) is False:
            raise ValueError('Frequency should be string ', frequency)
        if frequency not in Frequency.__members__.keys():
            raise ValueError(
                f'Frequency key should be {", ".join(list(Frequency.__members__.keys()))} only ', frequency)
        return Frequency[frequency].value

    def __generate_intervals(self) -> list:
        intervals = []
        for freq in self.__get_frequence(self.frequency):
            intervals.extend(
                rrule(freq, dtstart=self.period[0].date(
                ), until=self.period[1].date())
            )
        return intervals[1:]

    def __generate_time_interval(self, cur_date: datetime) -> list:
        time_intervals = []
        def get_date(h, m, s): return cur_date + \
            timedelta(hours=h, minutes=m, seconds=s)

        min_interval, _ = self.min_max_interval

        for r in self.timerange:
            post_time = get_date(
                randint(r[0], r[1]-1), randint(0, 59), randint(0, 59))
            # time_change = timedelta(hours=h, minutes=randint(30,30), seconds=randint(0,0))
            # post_time = get_date(h, randint(0,0), randint(0,0))

            if len(time_intervals) > 0:
                delta = (post_time - time_intervals[-1]).seconds
                dev = [(post_time - ti).seconds - min_interval for ti in time_intervals if (
                    post_time - ti).seconds - min_interval < 0]
                if len(dev) > 0:
                    post_time = post_time - timedelta(seconds=delta-min(dev))

            time_intervals.append(
                post_time
            )

        return time_intervals

    def __generate_post_intervals(self):
        # print(self.interval)
        post_dates = []
        for interval in self.interval:
            post_dates.append(
                self.__generate_time_interval(interval)
            )
        return post_dates
