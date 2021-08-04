from . import blog


@blog.route('/')
def index():
    return "Hello from blog Index"
