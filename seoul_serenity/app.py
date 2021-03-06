# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from seoul_serenity.settings import ProdConfig
from seoul_serenity.assets import assets
from seoul_serenity.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
)
from seoul_serenity import public, user, api, project, client_mayor, client_committee, client, storyboard, admin

# TODO : 현재 관리자 페이지와 클라이언트가 하나의 app으로 되어 있는데
# 이 부분을 서로 분리해서 처리가 가능한지, 그럴 경우에 어떤 장점이 있는지 확인
def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(project.views.blueprint)
    # app.register_blueprint(comment.views.blueprint)
    app.register_blueprint(client.views.blueprint)
    app.register_blueprint(client_mayor.views.blueprint)
    app.register_blueprint(client_committee.views.blueprint)
    app.register_blueprint(storyboard.views.blueprint)
    app.register_blueprint(admin.views.blueprint)


    return None


# TODO : 현재 기본 설정된 에러 페이지로 이동, cleint app의 경우 별도 새로 제작된 페이지로 이동되게 수정
def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None