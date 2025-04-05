import litserve
import os

from PythonPackages.OCR.OkraAPI import OkraLitAPI


if __name__ == '__main__':
    api = OkraLitAPI()
    server = litserve.LitServer(api)
    server.run(port=os.environ.get('LITSERVE_PORT', 8000))

