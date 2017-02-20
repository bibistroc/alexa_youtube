from alexa import app, sio
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename='%s/logs/web.log' % dir_path,
                    level=logging.DEBUG,
                    format='%(asctime)-15s %(levelname)-10s %(message)s')

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=5000, debug=True)
