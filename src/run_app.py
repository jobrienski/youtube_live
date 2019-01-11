import os
from liveapi import app

configtype = os.getenv( 'FLASK_ENV' ) or 'development'
if os.getenv('FLASK_PORT'):
    port = int(os.getenv('FLASK_PORT'))
else:
    port = 5000

if __name__=="__main__":
    app.run( host='localhost', port=port )
    # cert = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl_keys/cert.pem')
    # key = cert.replace("cert","key")
    # app.run(ssl_context=(cert,key))
