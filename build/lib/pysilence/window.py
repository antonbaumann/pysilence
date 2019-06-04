import math
import time

import numpy as np

from . import util, silence


class WindowEnergyIterator:
    """
    iterate efficiently over average energy values of a `window`
    in an array of audio data

    Functionality of this data structure explained with the help of an example:

        window_size = 6
        step_size   = 3

        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  <- Audio data
        [0, 1, 2, 3, 4, 5]                                  <- Window 0
                 [3, 4, 5, 6, 7, 8]                         <- Window 1
                          [6, 7, 8, 9, 10, 11]              <- Window 2

        [0, 1, 2][3, 4, 5][6, 7, 8][9, 10, 11] <- chunks with chunk_size = 3

        avg_energy(window_0) = (avg_energy(chunk_0) + avg_energy(chunk_1)) / 2
    """
    def __init__(self, audio_data, window_size, step_size):
        self.audio_data = audio_data
        self.window_size = window_size
        self.step_size = step_size

        self.start_time = time.time()
        self.position = 0  # current window index

        # nr of windows that will be generated
        self.nr_windows = int((len(self.audio_data) - self.window_size + self.step_size) // self.step_size)

        self.chunk_size = math.gcd(window_size, step_size)
        self.queue = RingQueue(window_size // self.chunk_size)
        self._init_queue()

    # fill queue with queueSize - 1 chunk values
    # so next time if a chunk is added the average energy of the window
    # can be calculated
    def _init_queue(self):
        for i in range(self.queue.size - 1):
            self.queue.add(silence.get_energy(self.audio_data[i * self.chunk_size:(i + 1) * self.chunk_size]))

    # print progress
    def progress(self):
        remaining = util.time_remaining(self.position, len(self.audio_data) // self.chunk_size, self.start_time)
        print(f'\r{self.position} of {len(self.audio_data) // self.chunk_size}  ETA: {remaining}', end='')

    def has_next(self):
        return self.position < self.nr_windows

    # return average energy in next window
    def next_window_energy(self):
        self.queue.add(
            silence._get_energy(
                self.audio_data[self.queue.index * self.chunk_size: (self.queue.index + 1) * self.chunk_size]
            )
        )
        self.position += 1
        return self.queue.get_energy()


class RingQueue:
    """
    this data structure allows us to hold the last n energy values
    """
    def __init__(self, size):
        self.size = size
        self.data = np.zeros(self.size)
        self.index = 0

    # add overwrite oldest value with new value
    def add(self, value):
        self.data[self.index % self.size] = value
        self.index += 1

    # returns the average energy in the queue
    def get_energy(self):
        return sum(self.data) / self.size
