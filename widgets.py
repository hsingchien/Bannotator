from PySide6.QtWidgets import QDoubleSpinBox
import numpy as np


class PlaySpeedSpinBox(QDoubleSpinBox):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.cutoff_low = -2.0
        self.cutoff_high = 2.0
        self.step_ratio = 10.0

    def stepBy(self, steps: int) -> None:
        if (
            np.ceil(self.value()) == self.cutoff_low
            and steps > 0
            and self.value() < self.cutoff_low - 0.00001
        ):
            return super().setValue(self.cutoff_low)
        if (
            np.floor(self.value()) == self.cutoff_high
            and steps < 0
            and self.value() > self.cutoff_high + 0.00001
        ):
            return super().setValue(self.cutoff_high)

        if (self.value() >= self.cutoff_high and steps > 0) or (
            self.value() <= self.cutoff_low and steps < 0
        ):
            return super().stepBy(steps * self.step_ratio)
        elif (self.value() >= self.cutoff_high + 1 and steps < 0) or (
            self.value() <= self.cutoff_low - 1 and steps > 0
        ):
            return super().stepBy(steps * self.step_ratio)
        else:
            return super().stepBy(steps)
