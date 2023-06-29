def low(r):
    return r.lower()

l = [str.capitalize, str.lower, cap]

# for l1 in l:
#     print(l1,l1('HeLLo'))


# functions can accept and return functions as args
def get_speak_func(volume):
    def whisper(text):
        return text.lower() + '...'
    def yell(text):
        return text.upper() + '!'
    if volume > 0.5:
        return yell
    else:
        return whisper

# functions can accept and return functions as args and also access parent state(data)
def speak_func(text,volume):
    def whisper():
        return text.lower() + '...'
    def yell():
        return text.upper() + '!'
    if volume > 0.5:
        return yell()
    else:
        return whisper()

# decorators for functions without arguments
def uppercase(func):
    def wrapper():
        original_result = func()
        modified_result = original_result.upper()
        return modified_result
    return wrapper

# decorators for functions with arguments
def uppercase(func):
    def wrapper(*args):
        return func(*args).upper()
    return wrapper
