def get_logger(name):
 class Dummy: def info(self, msg): print(f'[LOG]', msg); return Dummy()