import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from io import StringIO
from dotenv import load_dotenv

config = StringIO("BYPASS_LITSERVE=1")
load_dotenv(stream=config)

import OCR
import preprocessing
