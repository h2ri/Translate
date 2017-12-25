import abc
import redis
import configparser

conf = configparser.ConfigParser()
conf.read(".env")


class CachingStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_value_from_key(self, key):
        pass

    @abc.abstractmethod
    def create_or_append_value_to_key(self, value, key):
        pass


class RedisCacheStrategy(CachingStrategy):

    def __init__(self):
        if not hasattr(RedisCacheStrategy, 'pool'):
            RedisCacheStrategy.create_pool(self)
        self._connection = redis.Redis(connection_pool=RedisCacheStrategy.pool)

    def create_pool(self):
        RedisCacheStrategy.pool = redis.ConnectionPool(
            host=conf.get("Redis","host"),)

    def get_value_from_key(self, key, field):
        value = self._connection.hmget(key, field)
        if not value:
            return None
        return value[0]

    def create_or_append_value_to_key(self, key, value, field):
        return self._connection.hmset(key, {field: value})


class CachingContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_value(self, key, language):
        return self.strategy.get_value_from_key(key, language)

    def set_value(self, key, value, language):
        return self.strategy.create_or_append_value_to_key(key, value, language)


if __name__ == '__main__':

    caching_redis = RedisCacheStrategy()
    context = CachingContext(caching_redis)