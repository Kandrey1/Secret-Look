from config import ConfigDevelopment


broker_url = "redis://{broker_host}:{broker_port}/0".format(
        broker_host=ConfigDevelopment.REDIS_HOST,
        broker_port=ConfigDevelopment.REDIS_PORT)
result_backend = "redis://{broker_host}:{broker_port}/0".format(
        broker_host=ConfigDevelopment.REDIS_HOST,
        broker_port=ConfigDevelopment.REDIS_PORT)
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True
timezone = 'UTC'
