from werkzeug import find_modules, import_string


def views_register(app):
    for name in find_modules('miniapp.views'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
