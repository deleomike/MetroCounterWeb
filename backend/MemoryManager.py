import numpy as np
import queue
from sklearn.linear_model import LinearRegression

# TODO: caching and saving of the data


class MemoryManager:

    """
    1. Can return current crowd count
    2. Can return an array for the past hour
        - Array that is averaged by every 5 minutes
    3. Can return an array for the past 24 hours
        - Array that is averaged by every 15 minutes
    4. Can return an array for the past 7 days
        - Array that is averaged every 30 minutes
    5. Can return an array for the past 30 days
        - Array that is averaged every hour
    6. Can return an array for the past year
        - Array that is averaged every 12 hours
    """

    def __init__(self, interval=5):
        """
        :param interval: default of 5 min interval
        """
        self.mem = dict()

        self.interval = interval

    def insert_data(self, location: str, data_point: int):
        """
        1. Insert data point into data structure
        2. Recalculate averages
        :param location:
        :param data_point:
        :return:
        """
        if location not in self.mem:
            self.mem[location] = LocationStream(base_interval_min=self.interval)

        self.mem[location].put_value(data_point)

    def fit_regression(self, location: str):
        self.mem[location].fit_regression()

    def get_current(self, location: str) -> int:
        return self.mem[location].current_count

    def get_prediction(self, location: str):
        return self.mem[location].get_prediction()

    def get_hour(self, location) -> list:
        return self.mem[location].get_hour()

    def get_day(self, location) -> list:
        return self.mem[location].get_day()

    def get_week(self, location) -> list:
        return self.mem[location].get_week()

    def get_month(self, location) -> list:
        return self.mem[location].get_month()


class LocationStream:

    """
    1. Can return current crowd count
    2. Can return an array for the past hour
        - Array that is averaged by every 5 minutes
    3. Can return an array for the past 24 hours
        - Array that is averaged by every 15 minutes
    4. Can return an array for the past 7 days
        - Array that is averaged every 30 minutes
    5. Can return an array for the past 30 days
        - Array that is averaged every hour
    6. Can return an array for the past year
        - Array that is averaged every 12 hours
    """

    def __init__(self, base_interval_min: int = 5):

        # TODO year
        # TODO maybe custom interval

        assert base_interval_min > 0, f"Base interval cannot be 0 or negative: {base_interval_min}"

        self.base_interval_min = base_interval_min

        self.current_count = 0

        self.hour_data = RollingList(12)
        self.day_data = RollingList(96)
        self.week_data = RollingList(336)
        self.month_data = RollingList(720)

        self.XHour = np.arange(12).reshape(-1, 1)
        self.reg = LinearRegression()
        self.score = 0

    def fit_regression(self):
        data = np.array(self.hour_data.to_list())

        self.reg = self.reg.fit(self.XHour, data)
        self.score = self.reg.score(self.XHour, data)

    def get_prediction(self):
        """
        Uses the 24 hour queue because it uses 15 min increments
        :return:
        """
        # reg.score(X, y)
        #
        # reg.coef_
        #
        # reg.intercept_

        predictions = self.reg.predict([[14], [17], [23]]) # 15, 30, 60 after an hour, in 5 minute increments

        def postprocess(num):
            return int(max(0, num))

        return {
            "min_15": postprocess(predictions[0]),
            "min_30": postprocess(predictions[1]),
            "min_60": postprocess(predictions[2]),
            "score": self.score
        }

    def put_value(self, value: int, fit_regression=False):

        self.current_count = value

        self.hour_data.put(value)

        hour_arr = self.hour_data.to_list()

        # TODO accounting for custom interval

        avg_15 = np.average(hour_arr[0:2])
        avg_30 = np.average(hour_arr[0:5])
        avg_60 = np.average(hour_arr)

        self.day_data.put(avg_15)
        self.week_data.put(avg_30)
        self.month_data.put(avg_60)

        if fit_regression:
            self.fit_regression()

    def get_hour(self) -> list:
        return self.hour_data.to_list()

    def get_day(self) -> list:
        return self.day_data.to_list()

    def get_week(self) -> list:
        return self.week_data.to_list()

    def get_month(self) -> list:
        return self.month_data.to_list()


class RollingList:
    """
    Rolling queue for storing the data efficiently
    """

    def __init__(self, size: int, fill: bool = True):
        # TODO maybe init this to all zeros
        self.data = queue.Queue(size)
        self.size = size

        if fill:
            for _ in range(size):
                self.data.put(0)

    def put(self, val: int):
        if self.data.qsize() == self.size:
            self.data.get()

        self.data.put(val)

    def to_list(self) -> list:
        return list(self.data.queue)


if __name__ == "__main__":

    MM = MemoryManager()

    import time

    start = time.time()
    for i in range(10000):
        MM.insert_data("Hello", i)

    print(time.time() - start)