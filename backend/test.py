from dotenv import load_dotenv
load_dotenv()

import os
print(os.getenv("OPENWEATHER_API_KEY"))
