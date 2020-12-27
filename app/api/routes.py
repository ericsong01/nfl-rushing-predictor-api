from app.api import bp 

@bp.route('/predict')
def prediction():
    return "Here's your prediction"