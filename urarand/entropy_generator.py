#!/usr/bin/env python3

import time
from typing import Callable
from dataclasses import dataclass

class EntropyGeneratorModel():
    def tick(self, *args, **kwargs):
        raise NotImplementedError(f"{self.__qualname__} should be implemented")

    def dump_entropy(self):
        raise NotImplementedError(f"{self.__qualname__} should be implemented")

def get_tick_function():
    """
        This function returns the function to get the current tick, depending
        on the OS/CPU/whatever precision
    """

    f = lambda divisor : lambda : time.perf_counter_ns() // divisor

    for divisor in range(9):
        for j in range(100):
            ts = f(divisor)()
            if ts % 10 != 0:
                return stats(f(divisor))

    raise Exception("time.perf_counter_ns() seems buggy ?")

def stats():
    def decorator(func):
        ts = func()
        print(ts % 10)
        return ts
    return decorator

@dataclass
class EntropyGenerator(EntropyGeneratorModel):
    entropy_path: str = "./" + str(__qualname__) + ".bin"

    counter: int = 0

    bq: int = 0
    bq_1m: int = 0
    bq_5m: int = 0
    bq_15m: int = 0

    entropy: bytes = b""
    entropy_acc: str = ""

    t0: int = 0

    get_tick: Callable[[], int] = get_tick_function()

    def _delta_to_bits(self, delta):
        return str(delta % 2)

    @stats
    def tick(self, *args, **kwargs):
        if self.counter == 0:
            self.t0 = self.get_tick()
            self.counter += 1
            return
        t1 = self.get_tick()
        delta = (t1 - self.t0)

        self.entropy_acc += self._delta_to_bits(delta)
        if self.counter % 8 == 0:
            while len(self.entropy_acc) > 8:
                print('*' * 8, end='', flush=True)
                self.entropy += bytes([int(self.entropy_acc[:8], 2)])
                self.entropy_acc = self.entropy_acc[8:]
        self.counter += 1
        self.t0 = t1

        if self.counter >= 1024:
            self.dump_entropy()
            self.entropy = b""
            self.counter = 0

    def dump_entropy(self):
        with open(self.entropy_path, 'ab+') as f:
            f.write(self.entropy)

@dataclass
class EntropyGenerator_2_bits(EntropyGenerator):
    entropy_path: str = "./" + str(__qualname__) + ".bin"
    def _delta_to_bits(self, delta):
        return str((delta % 2)) + str((delta // 2) % 2)

@dataclass
class EntropyGenerator_4_bits(EntropyGenerator):
    entropy_path: str = "./" + str(__qualname__) + ".bin"
    def _delta_to_bits(self, delta):
        return str((delta % 2)) + str((delta // 2) % 2) + str((delta // 4) % 2) + str((delta // 8) % 2)
