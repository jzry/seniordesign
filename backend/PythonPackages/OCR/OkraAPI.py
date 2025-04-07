from litserve import LitAPI

from torch import load as torch_load, device as torch_device, argmax as torch_argmax
from torch import no_grad, float32
from torch.nn.functional import softmax
from torchvision.transforms import v2

import numpy as np
from pathlib import Path
import base64

from .OkraClassifier import OkraClassifier


class OkraLitAPI(LitAPI):
    """Defines a LitServe API for serving the Okra Classifier"""

    def setup(self, device):
        """Initialize and load the model"""

        model_dir = Path(__file__).parent / 'weights'

        #
        # Init and load the model
        #
        state_dict = torch_load(
            Path(model_dir) / 'okra-resnet.pt',
            weights_only=True,
            map_location=torch_device(device)
        )
        self.model = OkraClassifier()
        self.model.to(device)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        #
        # Prepare the image transformations
        #
        self.transform = v2.Compose([
            v2.ToImage(),
            v2.ToDtype(float32, scale=True),
            v2.Resize((28, 28))
        ])


    def decode_request(self, request):
        """Retrieve the image from the request"""

        raw_img = base64.b64decode(request.get('data').encode('ascii'))
        img_shape = (int(request.get('y')), int(request.get('x')))

        #
        # Build a tensor from the raw data and the image shape
        #
        img = np.frombuffer(raw_img, np.uint8)
        img = img.reshape(img_shape, copy=True)
        img = self.transform(img)
        img = img.reshape((1, 1, 28, 28))
        img = img.to(self.device)

        return img


    def predict(self, x):
        """Run the model with the input image"""

        with no_grad():
            logits = self.model(x)

        return logits


    def encode_response(self, output):
        """Prepare response from model output"""

        # Convert the results into probabilities
        probabilities = softmax(output[0], dim=0)

        # The index with the highest probability is the predicted value
        digit_value = torch_argmax(probabilities)
        confidence = probabilities[digit_value] * 100

        return { 'Digit': digit_value.item(), 'Confidence': confidence.item() }


    def direct_request(self, payload):
        """Pass the payload directly to the API functions"""

        data = self.decode_request(payload)
        result = self.predict(data)
        response = self.encode_response(result)
        return response
