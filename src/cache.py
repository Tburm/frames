from datetime import datetime, timedelta

class Cache:
    def __init__(self):
        self.cache = {}

    def needs_update(self, chart_name: str, interval: timedelta = timedelta(minutes=15)) -> bool:
        now = datetime.now()
        if chart_name not in self.cache or (now - self.cache[chart_name]) > interval:
            return True
        return False

    def update_chart_time(self, chart_name: str):
        self.cache[chart_name] = datetime.now()
