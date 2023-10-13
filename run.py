
from app import app
import os
from cati import *
from home import *
import logging

logging.basicConfig(filename='error.log',level=logging.DEBUG)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host='0.0.0.0', port=port)
    