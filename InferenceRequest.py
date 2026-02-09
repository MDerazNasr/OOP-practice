import heapq
from collections import defaultdict


class Request:
    def __init__(self, priority, id, model, status):
        self._priority = priority
        self._id = id
        self._model = model
        self._status = status

    def get_priority(self):
        return self._priority

    def get_id(self):
        return self._id

    def get_model(self):
        return self._model

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status


class Worker:
    def __init__(self, worker_id, worker_model, worker_status, handling):
        self._id = worker_id
        self._model = worker_model
        self._status = worker_status
        self._handling = None

    def get_worker_id(self):
        return self._id

    def get_worker_model(self):
        return self._model

    def get_worker_status(self):
        return self._status

    def set_worker_status(self, status):
        self._status = status

    def get_curr_req(self):
        return self._handling

    def assign_request(self, request):
        self._handling = request


class Manager:
    def __init__(self):
        self._workers = defaultdict(list)
        self._requests = defaultdict(list)
        self._counter = 0

    def accept_request(self, request):
        heapq.heappush(
            self._requests[request.get_model()],
            (request.get_priority(), self._counter, request),
        )
        self._counter += 1

    def register_worker(self, worker):
        self._workers[worker.get_worker_model()].append(worker)

    def release_worker(self, worker):
        request = worker.get_curr_req()
        worker.assign_request(None)
        worker.set_worker_status("FREE")
        request.set_status("COMPLETED")
        self._workers[worker.get_worker_model()].append(worker)
        self.assign_job(worker)
        print("job", request.get_id(), " has been completed.")

    def assign_job(self, worker):
        if (
            len(self._requests)
            and self._requests[worker.get_worker_model()]
            and self._workers[worker.get_worker_model()]
        ):
            p, c, request = heapq.heappop(self._requests[worker.get_worker_model()])
            request.set_status("PROCESSING")
            worker = self._workers[request.get_model()].pop()
            worker.assign_request(request)
            worker.set_worker_status("BUSY")
            return
        elif len(self._requests) == 0:
            print("There are no requests")
            return
        print("there are no available workers for the remaining")


def main():
    HIGH, MEDIUM, LOW = 1, 2, 3
    job1 = Request(LOW, 12, "llama", "PENDING")
    job2 = Request(MEDIUM, 13, "llama", "PENDING")
    job3 = Request(HIGH, 14, "llama", "PENDING")

    worker1 = Worker(1, "llama", "FREE", None)
    manager = Manager()

    manager.register_worker(worker1)
    manager.accept_request(job1)
    manager.accept_request(job2)
    manager.accept_request(job3)
    manager.assign_job(worker1)
    manager.release_worker(worker1)


main()
