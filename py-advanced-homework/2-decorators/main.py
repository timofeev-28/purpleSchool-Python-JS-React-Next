from functools import wraps


def limit_args(max_value, mode):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if mode == "clip":
                new_args = [
                    (
                        min(arg, max_value)
                        if isinstance(arg, (int, float))
                        else arg
                    )
                    for arg in args
                ]
                new_kwargs = {
                    k: (
                        min(v, max_value) if isinstance(v, (int, float)) else v
                    )
                    for k, v in kwargs.items()
                }
                return fn(*new_args, **new_kwargs)

            if mode == "error":
                for arg in args:
                    if isinstance(arg, (int, float)) and arg > max_value:
                        raise ValueError(
                            f"Максимальное значение аргумента должно быть не больше {max_value}"
                        )
                for _, v in kwargs.items():
                    if isinstance(v, (int, float)) and v > max_value:
                        raise ValueError(
                            f"Максимальное значение аргумента должно быть не больше {max_value}"
                        )

            return fn(*args, **kwargs)

        return wrapper

    return decorator


@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b


# @limit_args(max_value=10, mode="error")
# def multiply(a, b):
#     return a * b


if __name__ == "__main__":
    try:
        print(multiply(2, 3))
        print(multiply(100, 3))
    except ValueError as e:
        print(f"[WARN]: {e}")
