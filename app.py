from flask import Flask, render_template

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from models import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    from routes.candidates import bp as candidates_bp
    from routes.search import bp as search_bp
    
    app.register_blueprint(candidates_bp)
    app.register_blueprint(search_bp)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors.html', error=404, message="Page not found"), 404
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors.html', error=500, message="Internal server error"), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
