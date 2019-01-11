import os
from liveapi import app

if __name__=="__main__":
    app.run()
    # cert = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ssl_keys/cert.pem')
    # key = cert.replace("cert","key")
    # app.run(ssl_context=(cert,key))
