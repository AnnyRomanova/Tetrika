import inspect


def strict(func):
    def wrapper(*args):
        flag = True
        signature = inspect.signature(func)
        args_annotations_list = []
        for param in signature.parameters.values():
            args_annotations_list.append(param.annotation)
        for i in range(len(args)):
            if type(args[i]) != args_annotations_list[i]:
                flag = False
        if not flag:
            raise TypeError(
                "Типы переданных в вызов функции аргументов не соответствуют типам аргументов, объявленных в прототипе функции"
            )
        return func(*args)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

if __name__ == '__main__':
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError
