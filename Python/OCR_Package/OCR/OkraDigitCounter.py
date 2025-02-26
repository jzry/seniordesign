from torch.nn import Module, RNN, Conv2d, MaxPool2d, Sequential
from torch import transpose, concat
from torchvision.transforms.functional import resize


class OkraDigitCounter(Module):

    def __init__(self):
        super().__init__()
        self.input_dim = 27    # This should be the output size of self.feature
        self.hidden_dim = 100
        self.output_dim = 3
        self.feature = Sequential(
            Conv2d(in_channels=1, out_channels=3, kernel_size=3),
            MaxPool2d(kernel_size=2, stride=2, padding=(1, 0))
        )
        self.encoder = RNN(
            self.input_dim,
            self.hidden_dim,
            batch_first=True,
            nonlinearity='relu'
        )
        self.decoder = RNN(
            self.hidden_dim,
            self.output_dim,
            batch_first=True,
            nonlinearity='relu'
        )

    def forward(self, x):

        # Extract features from image
        y = self.feature(x)
        y = concat([y[i] for i in range(y.shape[0])], dim=1)
        y = y.unsqueeze(dim=0)

        # Pass input through encoder and decoder
        out_sequences, _ = self.encoder(y, None)
        _, out = self.decoder(out_sequences, None)

        return out.squeeze(dim=0)


class TransposeImage:

    def __call__(self, x):
        if len(x.shape) == 3:
            return transpose(x[0], 0, 1)
        else:
            return transpose(x, 0, 1)

class FlattenImage:

    def __call__(self, x):
        if len(x.shape) == 3:
            width = x.shape[2]
        else:
            width = x.shape[1]
        height = 20
        return resize(x, (height, width))


