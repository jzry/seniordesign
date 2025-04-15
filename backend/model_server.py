import litserve
import os

from PythonPackages.OCR.OkraAPI import OkraLitAPI

from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    api = OkraLitAPI()
    server = litserve.LitServer(api)
    server.run(port=os.environ.get('PORT', 8000))

