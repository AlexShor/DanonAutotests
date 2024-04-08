# from custom_moduls.console_design.colors import ConsoleColors as CCol
# from custom_moduls.console_design.indentation_levels import indentation_levels as Ilvl
#
#
# def benchmark(func):
#     import time
#
#     def wrapper(*args, **kwargs):
#         start_creating_files = time.time()
#         print(f'{Ilvl(1)}Start: "{func.__name__}".')
#
#         res = func(*args, **kwargs)
#
#         end_creating_files = time.time() - start_creating_files
#         print(f'{Ilvl(1)}End: "{func.__name__}". Time:', round(end_creating_files, 3), end='\n\n')
#
#         return res
#     return wrapper
#
#
# class ConsoleDecorator:
#     def __init__(self, main_massage, level=0, ):
#         self.n = n
#
#     def __call__(self, func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             for _ in range(self.n):
#                 value = func(*args, **kwargs)
#             return value
#
#         return wrapper