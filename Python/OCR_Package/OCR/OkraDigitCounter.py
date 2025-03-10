from torch.nn import Module, Sequential, Conv2d, MaxPool2d, Linear, ReLU, Flatten
from torch.nn.functional import pad


class OkraDigitCounter(Module):

    def __init__(self):
        super().__init__()

        self.feature = Sequential(
            Conv2d(1, 12, 3),
            MaxPool2d(2, 2),
            ReLU(),
            Conv2d(12, 24, 3),
            MaxPool2d(2, 2),
            ReLU(),
            Flatten()
        )
        self.linear = Sequential(
            Linear(6 * 6 * 24, 100),
            ReLU(),
            Linear(100, 3),
        )


    def forward(self, x):

        y = self.feature(x)
        return self.linear(y)


class PadImage:

    def __call__(self, x):

        if x.shape[-2] == x.shape[-1]:
            return x

        # This is how much padding will be needed to make the image a square
        padding = abs(x.shape[-2] - x.shape[-1]) // 2

        # If the y dimension is smaller the x dimension, then use the pad on
        # the y dimension (add more rows than columns).
        #
        # If the x dimension is smaller the y dimension, then use the pad on
        # the x dimension (add more columns than rows).
        #
        if x.shape[-2] < x.shape[-1]:
            x = pad(x, (0, 0, padding, padding))

        else:
            x = pad(x, (padding, padding))

        return x

