def executeTimeDecorator(function):
    def wrapper(*args, **kwargs):
        # wrapper
        import time

        start = time.perf_counter()
        function(*args, **kwargs)
        end = time.perf_counter()
        print(f"{(end - start):.5f}")
