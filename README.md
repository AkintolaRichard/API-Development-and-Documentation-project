# API Development and Documentation Final Project

## Trivia App

Trivia App is a web application containing a trivia game.

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.
The [backend](./backend/README.md) directory contains the backend setup.

> View the [Backend README](./backend/README.md) for more details. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in the flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```
The [frontend](./frontend/README.md) directory contains how to setup the React frontend that will consume the data from the Flask server.

> View the [Frontend README](./frontend/README.md) for more details.

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Request Not Successful

### Endpoints
#### GET /api/v1.0/categories
- General:
    - Returns a dictionary with a single key, categories, that contains a dictionary of id: category key:value pairs.
- Sample: `curl http://127.0.0.1:5000/api/v1.0/categories`

``` {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "success": true
    }

```

#### GET /api/v1.0/questions
- General:
    - Returns a paginated set of questions, a total number of questions, all categories and current category string.
- Sample: `curl http://127.0.0.1:5000/api/v1.0/questions?page=1`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}
```

### GET /api/v1.0/categories/{id}/questions
- General:
    - Returns a dictionary with questions for a category specified by the `id`, total questions, and current category string.
- `curl http://127.0.0.1:5000/api/v1.0/categories/1/questions`
```
{
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}
```

#### DELETE /api/v1.0/questions/{id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted book and success value.
- `curl -X DELETE http://127.0.0.1:5000/api/v1.0/questions/1`
```
{
  "question": 1,
  "success": true,
}
```

#### POST /api/v1.0/quizzes
- General:
    - Accepts a post request containing the keys `previous_questions`, `quiz_category` and the values of the data types `list/array`, `string` respectively. Return an array of question and success value.
- `curl -X POST http://127.0.0.1:5000/api/v1.0/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[1,4,20,12], "quiz_category": "History"}'`
```
"question": {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
    },
    "success": true
}
```

#### POST /api/v1.0/questions
- General:
    - Creates a new question using the submitted question, answer, difficulty, category. Returns success value.
        - `curl http://127.0.0.1:5000/api/v1.0/questions -X POST -H "Content-Type: application/json" -d '{"question":"Here is a new question", "answer":"Here is the answer", "difficulty":1, "category":3}'`
        ```
        {
        "success": true,
        }
        ```
    - Returns an array of questions that met the specified searchTerm, a number of totalQuestions and the current category string.
        - `curl -X POST http://127.0.0.1:5000/api/v1.0/questions -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`
        ```
        {
        "currentCategory": "Art",
        "questions": [
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }
        ],
        "success": true,
        "totalQuestions": 2
        }
        ```
#### POST /api/v1.0/categories
- General:
    - Creates a new category using the submitted category. Returns success value.
        - `curl http://127.0.0.1:5000/api/v1.0/categories -X POST -H "Content-Type: application/json" -d '{"category":"Technology"}'`
        ```
        {
        "success": true,
        }
        ```

## Deployment N/A

## Authors
Udacity, Coach Caryn, Richard Akintola

## License
Check [License](./LICENSE.txt) for the license.

## Acknowledgements 
The Project Reviewers, the awesome team at Udacity, and all of the students, soon to be full stack extraordinaires!

