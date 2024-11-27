def function_execution_test(num_tests: int = 1):
    def inner(function):
        def wrapper(*args, **kwargs):
            import time
            overall_time: float = 0
            for i in range(num_tests):
                i += 1
                start = time.perf_counter()
                function(*args, **kwargs)
                end = time.perf_counter()
                overall_time += (end - start)
                print(f"Test number: {i} | Time to execute: {(end - start):.5f}s")
            print('\n')
            print("Average Execution Time: ")
            print(f"{(overall_time / num_tests):.5f}s")

        return wrapper
    return inner

if __name__ == "__main__":
    @function_execution_test(num_tests=1)
    def test_func():
        print("Executing Function...")
    test_func()