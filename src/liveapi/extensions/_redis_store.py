import redis


class _RedisStore:
    '''
    Factory initialization - so we can pass app config values
    '''

    def __init__(self):
        self.redis_store = None

    def set(self,key,value,expiry=None):
        self.redis_store.set(key,value,ex=expiry)

    def get(self,key):
        return self.redis_store.get(key)

    def setup_redis(self,host,port):
        self.redis_store = redis.StrictRedis(host=host,port=port,db=0,
                                             decode_responses=True)

    def get_redis_instance(self):
        return self.redis_store

    def init_app(self,app):
        self.setup_redis(app.config['REDIS_HOST'],app.config['REDIS_PORT'])
        # link to session
        # app.config['SESSION_REDIS'] = self.redis_store
