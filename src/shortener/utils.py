import random


DEFAULT_CHARS = 'ABCDEFGHIJKLMNOPRSTUWXYZabcdefghijklmnoprstuwxyz0123456789'


def code_generator(size=5, chars=DEFAULT_CHARS):
    return ''.join(random.choice(chars) for _ in range(size))


def create_shortcode(instance, size=5):
    model = instance.__class__
    exists = True
    while exists:
        code = code_generator(size=size)
        exists = model.objects.filter(shortcode=code).exists()
    return code
