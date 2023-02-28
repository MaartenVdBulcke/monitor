from db import MariaEngine
from monitor import Monitor


engine = MariaEngine.get_engine()
measurements = Monitor.read_database(engine)
Monitor.render(measurements)
