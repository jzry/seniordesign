from torch.nn import Conv2d
from torch import load as torch_load
from torch import device as torch_device
from torchvision.models import resnet18


def get_model(weights_file=None, device='cpu'):

    model = resnet18(num_classes=10)
    model.conv1 = Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)

    if weights_file is not None:
        state_dict = torch_load(
            weights_file,
            weights_only=True,
            map_location=torch_device(device)
        )
        model.load_state_dict(state_dict)

    model.to(device)

    return model

