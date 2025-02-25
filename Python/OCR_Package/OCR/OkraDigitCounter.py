from torch.nn import Module, RNN
from torch import transpose
from torchvision.transforms.functional import resize


class OkraDigitCounter(Module):

    def __init__(self):
        super().__init__()
        self.input_dim = 20
        self.hidden_dim = 100
        self.output_dim = 3
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

        # Pass input through encoder and decoder
        out_sequences, _ = self.encoder(x, None)
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


