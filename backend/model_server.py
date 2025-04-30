import litserve
import os

from PythonPackages.OCR.OkraAPI import OkraLitAPI

from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    api = OkraLitAPI()
    server = litserve.LitServer(api)
    # server.run(port=os.environ.get('LITSERVE_PORT', 8000)) # Original
    port = int(os.environ.get("PORT", 8000)) # default to 8000 locally
    server.run(host="0.0.0.0", port=port)

