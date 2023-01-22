from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey #do we need to import the classes?

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-survey-key"

debug = DebugToolbarExtension(app)

responses = []
index = 0

def get_question_text(question_object):
    return question_object.question

@app.route('/')
def show_survey_start():
    """Show the user the title, instructions, and start button for the survey."""
    responses.clear()
    index = 0
    return render_template('survey_home.html', survey_title = satisfaction_survey.title, survey_instructions = satisfaction_survey.instructions)

@app.route('/questions/<int:question_number>')
def show_question(question_number):
    """Show the user the current question and the possible choices as buttons."""

    # if the user has already answered all of the survey questions and attempts to access a question page, redirect them to the thank you page
    if len(responses) == len(satisfaction_survey.questions):
        flash("You already answered all of the survey questions. Thank you!")
        return redirect('/thank-you')

    # if the user attempts to access questions out of order or attempts to revisit an old question after submitting their response, redirect them to the question page of the next survey question
    if question_number != len(responses):
        flash("The question you attempted to access either: does not exist, has already been answered, or has other questions that come before it.")
        return redirect(f'/questions/{len(responses)}')

    question_object = satisfaction_survey.questions[question_number]
    question_text = question_object.question
    answer_choices = question_object.choices
    return render_template('survey_question.html', survey_title = satisfaction_survey.title, question_number = question_number, question_text = question_text, answer_choices = answer_choices)


@app.route('/answer', methods=["POST"])
def store_answer():
    """Store the user's answer in the responses array and redirect them."""
    answer = request.form["answer"]
    responses.append(answer)
    index = len(responses)

    #responses.append(request.form["answer"]) #render_template('answer.html') #f'<h1>Received {request.form["answer"]} </h1>' #render_template('answer.html', responses = responses)
    
    # if index is strictly less than the length of the survey, then that means we have at least one more question to ask user 

    if index < len(satisfaction_survey.questions):
        return redirect(f'/questions/{index}')

    # otherwise, our survey is out of questions and we can redirect to the thank you page

    else:
        return redirect('/thank-you') #render_template('thank_you.html')

@app.route('/thank-you')
def show_thanks_page():
    """Show the user a thank-you page for completing the survey, including a copy of their responses."""
    receipt = zip(map(get_question_text, satisfaction_survey.questions), responses)
    return render_template('thank_you.html', record = receipt)
