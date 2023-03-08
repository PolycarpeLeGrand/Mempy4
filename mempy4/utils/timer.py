"""Contains the Timer class

Useful to time stuff
Will start and print on init unless specified otherwise
Use .step(msg) to step. Will print msg, time since last step and total time
"""

from datetime import datetime


class Timer:
    def __init__(self, start=True, vocal=True):

        self.start_time = None
        self.step_time = None
        self.steps = []

        self.vocal = vocal
        if start:
            self.start()

    def start(self):
        self.start_time = datetime.now()
        self.step_time = self.start_time
        self.steps.append(self.step_time)
        if self.vocal:
            print(f'Starting timer. Local time: {self.start_time}')

    # returns total time since start
    def get_run_time(self):
        return datetime.now()-self.start_time

    # adds a new step and returns time since last step
    def step(self, flavor=''):
        prev_step = self.step_time
        self.step_time = datetime.now()
        self.steps.append(self.step_time)
        curr_step_time = self.step_time - prev_step
        if self.vocal:
            print(f'{flavor} Step time: {curr_step_time} - Total time {self.get_run_time()}')
        return curr_step_time

    # returns a list with all the step times, starting with start
    def get_steps(self):
        return self.steps


