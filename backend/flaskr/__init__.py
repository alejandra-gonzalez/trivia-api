import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # CORS set up. Allow '*' for origins.
  CORS(app, resources={'/': {'origins': '*'}})

  # Set Access-Control-Allow using the after_request decorator
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 
    'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 
    'GET, POST, PUT, DELETE, OPTIONS')
    return response

  # This endpoint handles GET requests for all available categories.
  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.type).all()

    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })

  # This endpoint handles GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 
  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    categories = Category.query.order_by(Category.type).all()

    if len(current_questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': {category.id: category.type for category in categories},
      'current_category': None
      })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  # This endpoint gets questions of a specific category. 
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    category = Category.query.filter_by(id=category_id).one_or_none()

    if (category is None):
      abort(404)
    
    selection = Question.query.filter_by(category=category_id).all()
    paginated_selection = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': paginated_selection,
      'total_questions': len(Question.query.all()),
      'current_category': category.type
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  return app

    