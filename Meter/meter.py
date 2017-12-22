import math
import numpy as np
import torch


class Meter(object):
    def __init__(self):
        pass

    def reset(self):
        pass

    def add(self, *args, **kwargs):
        pass

    def value(self):
        pass


class AverageMeter(Meter):
    def __abs__(self):
        super(AverageMeter, self).__init__()
        self.sum = 0.0
        self.n = 0
        self.var = 0.0
        self.mean = 0.0
        self.std = 0.0


class SlidingWindowAverageMeter(Meter):
    def __init__(self, window_size=16):
        super(SlidingWindowAverageMeter, self).__init__()
        self.window_size = window_size
        self.value_queue = torch.Tensor(window_size)
        self.sum = 0.0
        self.n = 0
        self.var = 0.0
        self.mean = 0.0
        self.std = 0.0

    def reset(self):
        self.sum = 0.0
        self.n = 0
        self.value_queue.fill_(0)

    def add(self, value):
        index = self.n % self.window_size
        old_value = self.value_queue[index]
        self.sum += value - old_value
        self.value_queue[index] = value
        self.n += 1

    def value(self):
        n = min(self.n, self.window_size)
        mean = self.sum / max(1, n)
        return mean


class MovingAverageMeter(Meter):
    def __init__(self, momemtum=0.9):
        super(MovingAverageMeter, self).__init__()
        self.momemtum = momemtum

    def reset(self):
        self.num = 0.0

    def add(self, value):
        old_value = self.num
        self.num = (1 - self.momemtum) * value \
                   + self.momemtum * old_value

    def value(self):
        return self.num
