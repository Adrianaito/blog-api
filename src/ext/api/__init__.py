from .user import user_bp
from .blog_post import blogpost_bp

def init_app(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(blogpost_bp)
