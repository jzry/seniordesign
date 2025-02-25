try:
    from ts.torch_handler.base_handler import BaseHandler

except ImportError:

    # If were not using TorchServe,
    # we don't really need to inherit
    # from the actual torchserve handler.
    class BaseHandler:
        pass

from torch import load as torch_load, device as torch_device, argmax as torch_argmax, no_grad
from torch.nn.functional import softmax
from torchvision import transforms

import numpy as np
from pathlib import Path
import json

from OCR.OkraDigitCounter import OkraDigitCounter, FlattenImage, TransposeImage


class OkraDigitCounterHandler(BaseHandler):
    """A custom model handler for OkraDigitCounter"""

    def __init__(self):

        super().__init__()
        self.initialized = False
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(0.0, 1.0),
            FlattenImage(),
            TransposeImage()
        ])


    def initialize(self, context=None):
        """Initialize the model. This is called at the first handle request"""

        if context is None:

            model_dir = Path(__file__).parent / 'weights'

        else:

            properties = context.system_properties
            model_dir = properties.get('model_dir')

        #
        # Init and load the model
        #
        device = 'cpu'
        state_dict = torch_load(
            Path(model_dir) / 'okra-counter.pt',
            weights_only=True,
            map_location=torch_device(device)
        )
        self.model = OkraDigitCounter()
        self.model.to(device)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        self.initialized = True


    def __inference(self, image):
        """Runs the model with the image"""

        with no_grad():
            logits = self.model(image)

        return logits


    def __prepare_image(self, data):
        """Extracts the image data and prepares it for the classifier"""

        if not isinstance(data, dict):
            data = data[0]

        raw_data = data.get("data")

        img_shape = (int(data.get("y")), int(data.get("x")))

        im = np.frombuffer(raw_data, np.uint8)
        im = im.reshape(img_shape, copy=True)
        im = self.transform(im)
        im = im.unsqueeze(dim=0)

        return im


    def __process_output(self, ouptut):
        """Converts logits into a prediction and confidence"""

        # Convert the results into probabilities
        probabilities = softmax(ouptut[0], dim=0)

        # The index with the highest probability is the predicted value
        label = torch_argmax(probabilities, dim=0)

        return { "Count": label.item() + 1 }


    def handle(self, data, context=None):
        """The method invoked by TorchServe for prediction requests"""

        if not self.initialized:
            self.initialize(context)

        img = self.__prepare_image(data)
        out = self.__inference(img)
        prediction = self.__process_output(out)

        return [json.dumps(prediction) + '\n']
