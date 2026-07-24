import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Now you can access the environment variables using os.getenv()
variable_name = os.getenv('VARIABLE_NAME')
