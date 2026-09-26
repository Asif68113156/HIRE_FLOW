from flask import Blueprint, render_template, request, jsonify
from search.ranking import perform_search

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/')
def search_page():
    query = request.args.get('q', '')
    
    if not query:
        return render_template('search_results.html', results=None, query="")
        
    search_data = perform_search(query)
    
    return render_template('search_results.html', 
                            results=search_data['results'],
                            explanation=search_data['explanation'],
                            understood=search_data['understood'],
                            query=query)

@bp.route('/api')
def api_search():
    query = request.args.get('q', '')
    search_data = perform_search(query)
    return jsonify(search_data)
