import heapq


class Job:
    def __init__(self, priority, contents, job_id, status):
        self._priority = priority
        self._contents = contents
        self._job_id = job_id
        self._status = status

    def get_priority(self):
        return self._priority

    def get_type(self):
        return self._type

    def get_contents(self):
        return self._contents

    def get_job_id(self):
        return self._job_id

    def set_status(self, new_status):
        self._status = new_status

    def process(self):
        pass


class Translate(Job):
    def process(self):
        print(f"Summarizing job {self._job_id}: {self._contents}")


class Summarize(Job):
    def process(self):
        print(f"Summarizing job {self._job_id}: {self._contents}")


class DocumentAnalyser:
    def __init__(self):
        self._jobs = []
        heapq.heapify(self._jobs)
        self.counter = 0
        self.queue = set()

    def submitJob(self, job):
        if job.get_contents() in self.queue:
            print("Duplicate job rejected: ", job.get_contents())
            return
        else:
            self.queue.add(job.get_contents())
            heapq.heappush(self._jobs, (job.get_priority(), self.counter, job))
            self.counter += 1

    def processNext(self):
        if not self._jobs:
            print("No jobs in list.")
            return

        p, c, next = heapq.heappop(self._jobs)
        self.queue.remove(next.get_contents())
        next.set_status("PROCESSING")
        next.process()
        next.set_status("COMPLETED")


def main():
    HIGH, MEDIUM, LOW = 1, 2, 3
    job1 = Summarize(MEDIUM, "Hello World", "124", "PENDING")
    job4 = Summarize(MEDIUM, "Hello World", "124", "PENDING")
    job2 = Translate(LOW, "Hello", "324", "PENDING")
    job3 = Summarize(HIGH, "pineapple", "424", "PENDING")

    jobs = DocumentAnalyser()
    jobs.submitJob(job1)
    jobs.submitJob(job2)
    jobs.submitJob(job4)
    jobs.submitJob(job3)
    jobs.processNext()
    jobs.processNext()
    jobs.processNext()
    jobs.processNext()


main()
