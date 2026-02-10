import heapq
import threading
from collections import defaultdict


class MetricTracker(threading.Thread):
    def __init__(self):
        super().__init__()
        self._models = defaultdict(list)
        self._totals = defaultdict(int)
        self.lock = threading.Lock()
        self.time = 0

    def record(self, model, latency):
        with self.lock:
            heapq.heappush(self._models, (self.time, latency))
            self._totals[model] += latency
        return

    def avg(self, model):
        with self.lock:
            return self._totals[model] / len(self._models[model])


def main():
    test = MetricTracker()
    test.record("llama", 120)
    test.record("llama", 320)
    test.record("llama", 220)
    test.record("mistral", 100)
    test.avg("llama")


main()
