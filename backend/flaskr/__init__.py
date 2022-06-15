import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
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

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,OPTIONS'
        )
        return response

    @app.route('/api/v1.0/categories')
    def retrieve_categories():
        allCategories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in allCategories]
        categoriesDict = {}
        for item in categories:
            categoriesDict[str(item['id'])] = item['type']
        return jsonify({
            'success': True,
            'categories': categoriesDict
        })

    @app.route('/api/v1.0/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        allCategories = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in allCategories]
        categoriesDict = {}
        for item in categories:
            categoriesDict[str(item['id'])] = item['type']
        categoriesType = [category['type'] for category in categories]
        current_category = random.choice(categoriesType)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categoriesDict,
            'currentCategory': current_category,
        })

    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id
                ).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'question': question_id
            })
        except Exception as e:
            abort(422)

    @app.route('/api/v1.0/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        searchTerm = body.get('searchTerm', None)
        try:
            if searchTerm:
                result = Question.query.order_by(
                    Question.id
                ).filter(
                    Question.question.ilike('%{}%'.format(searchTerm))
                    )
                all_questions = [question.format() for question in result]
                allCategories = Category.query.order_by(Category.id).all()
                categories = [category.format() for category in allCategories]
                categoriesDict = {}
                for item in categories:
                    categoriesDict[str(item['id'])] = item['type']
                categoriesType = [category['type'] for category in categories]
                currentCategory = random.choice(categoriesType)
                return jsonify({
                    'success': True,
                    'questions': all_questions,
                    'totalQuestions': len(all_questions),
                    'currentCategory': currentCategory
                })
            else:
                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty)
                question.insert()

                return jsonify({
                    'success': True
                })
        except Exception as e:
            abort(422)

    @app.route('/api/v1.0/categories', methods=['POST'])
    def create_category():
        body = request.get_json()
        type = body.get('type', None)
        try:
            if type:
                category = Category(type=type)
                category.insert()
                return jsonify({
                    'success': True
                })
            else:
                abort(500)
        except Exception as e:
            abort(422)

    @app.route('/api/v1.0/categories/<int:category_id>/questions')
    def category_questions(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id)
            current_category = Category.query.get(category_id).type
            all_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': all_questions,
                'totalQuestions': len(Question.query.all()),
                'currentCategory': current_category
            })
        except Exception as e:
            abort(404)

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def get_new_question():
        try:
            body = request.get_json()
            previousQuestions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            if str(type(quiz_category)) == "<class 'dict'>":
                if quiz_category['id'] == 0:
                    result = Question.query.all()
                    available_questions = [
                        question.format()for question in result
                        ]
                    question = random.choice(available_questions)
                    return jsonify({
                        'success': True,
                        'question': question,
                    })
                else:
                    current_category = Category.query.filter(
                        Category.id == quiz_category['id']
                        ).one_or_none()
                    if len(previousQuestions) != 0:
                        result = Question.query.filter(
                            Question.id.not_in(previousQuestions),
                            Question.category == current_category.id
                            ).all()
                        if result:
                            if len(result) > 1:
                                available_questions = [
                                    question.format() for question in result
                                    ]
                                question = random.choice(available_questions)
                            else:
                                question = result.format()
                            return jsonify({
                                'success': True,
                                'question': question
                            })
                        else:
                            result = Question.query.all()
                            available_questions = [
                                question.format() for question in result
                                ]
                            question = random.choice(available_questions)
                            return jsonify({
                                'success': True,
                                'question': question
                            })
                    else:
                        result = Question.query.filter(
                            Question.category == current_category.id
                            ).all()
                        if result:
                            if len(result) > 1:
                                available_questions = [
                                    question.format() for question in result
                                    ]
                                question = random.choice(available_questions)
                            else:
                                question = result.format()
                            return jsonify({
                                'success': True,
                                'question': question
                            })
            else:
                current_category = Category.query.filter(
                    Category.type == quiz_category
                    ).one_or_none()
                result = Question.query.filter(
                    Question.id.not_in(previousQuestions),
                    Question.category == current_category.id
                    ).all()
                if result:
                    if len(result) > 1:
                        available_questions = [
                            question.format() for question in result
                            ]
                        question = random.choice(available_questions)
                    else:
                        question = result.format()
                    return jsonify({
                        'success': True,
                        'question': question
                    })
        except Exception as e:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def not_successful(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Request Not Successful'
        }), 500

    return app
