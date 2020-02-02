#!/usr/bin/env python3

import time
from typing import Callable
from dataclasses import dataclass

class EntropyGeneratorModel():
    def tick(self, *args, **kwargs):
        raise NotImplementedError(f"{self.__qualname__} should be implemented")

    def dump_entropy(self):
        raise NotImplementedError(f"{self.__qualname__} should be implemented")

@dataclass
class EntropyGenerator(EntropyGeneratorModel):
    entropy_path: str

    counter: int = 0

    bq: int = 0
    bq_1m: int = 0
    bq_5m: int = 0
    bq_15m: int = 0

    entropy: bytes = b""
    entropy_acc: str = ""

    t0: int = 0

    get_tick: Callable[[], int] = lambda : time.perf_counter_ns() // 1000

    def tick(self, *args, **kwargs):
        print('*', end='', flush=True)

        if self.counter == 0:
            self.t0 = self.get_tick()
            self.counter += 1
            return
        t1 = self.get_tick()
        delta = (t1 - self.t0)

        self.entropy_acc += str((delta % 2))
        if self.counter % 8 == 0:
            self.entropy += chr(int(self.entropy_acc, 2)).encode("utf-8")
            self.entropy_acc = ""
        self.counter += 1
        self.t0 = t1

        if self.counter >= 1024:
            self.dump_entropy()
            self.entropy = b""
            self.counter = 0
    
    def dump_entropy(self):
        with open(self.entropy_path, 'ab+') as f:
            f.write(self.entropy)
