import time


class RunTimer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = None
        self.elapsed_before_pause = 0.0
        self.paused = False
        self.finished = False
        self.final_time = None

    def start(self):
        self.start_time = time.time()
        self.elapsed_before_pause = 0.0
        self.paused = False
        self.finished = False
        self.final_time = None

    def pause(self):
        if self.start_time is None:
            return

        if self.paused:
            return

        if self.finished:
            return

        self.elapsed_before_pause = self.get_elapsed()
        self.paused = True

    def resume(self):
        if self.start_time is None:
            return

        if not self.paused:
            return

        if self.finished:
            return

        self.start_time = time.time()
        self.paused = False

    def finish(self):
        if self.finished:
            return self.final_time

        self.final_time = self.get_elapsed()
        self.finished = True
        self.paused = False

        return self.final_time

    def get_elapsed(self):
        if self.start_time is None:
            return 0.0

        if self.finished:
            return self.final_time or 0.0

        if self.paused:
            return self.elapsed_before_pause

        return self.elapsed_before_pause + (time.time() - self.start_time)

    def format_time(self, seconds=None):
        if seconds is None:
            seconds = self.get_elapsed()

        total_seconds = int(seconds)
        minutes = total_seconds // 60
        sec = total_seconds % 60
        milli = int((seconds - total_seconds) * 1000)

        return f"{minutes:02d}:{sec:02d}.{milli:03d}"