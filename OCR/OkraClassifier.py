import torch
import torchvision.models as models


def get_model(weights_file=None, device='cpu'):

    model = models.resnet18(num_classes=10)
    model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)

    if weights_file is not None:
        state_dict = torch.load(
            weights_file,
            weights_only=True,
            map_location=torch.device(device)
        )
        model.load_state_dict(state_dict)

    model.to(device)

    return model

