
# Create your views here.
# survey/views.py
import requests
from django.shortcuts import render, redirect
from .forms import SurveyForm
from pymongo import MongoClient
import google.generativeai as genai

client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string
db = client['profiledb1']  # Database name
collection = db['english_learning']  # Collection name

genai.configure(api_key="AIzaSyDt2Sx2tXkU-Y1CfLxI9JEzEcpZuhb1bZ0")
def survey_view(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Redirect to a thank you page or another page
    else:
        form = SurveyForm()
    
    return render(request, 'survey/survey.html', {'form': form})


def thank_you_view(request):
    return render(request, 'survey/thank_you.html')
def test_view(request):
    if request.method == 'POST':
        # User's answers
        user_answers = {
            'fill_in_1': request.POST.get('fill_in_1', ''),
            'fill_in_2': request.POST.get('fill_in_2', ''),
            'match_1': request.POST.get('match_1', ''),
            'match_2': request.POST.get('match_2', ''),
            'match_3': request.POST.get('match_3', ''),
            'rearrange': request.POST.get('rearrange', ''),
            'unscramble_1': request.POST.get('unscramble_1', ''),
            'synonym_1': request.POST.get('synonym_1', ''),
            'completion_1': request.POST.get('completion_1', ''),
            'completion_2': request.POST.get('completion_2', ''),
            'story_continuation': request.POST.get('story_continuation', ''),
            'dialogue_1': request.POST.get('dialogue_1', ''),
            'dialogue_2': request.POST.get('dialogue_2', ''),
            'error_detection': request.POST.get('error_detection', ''),
            'request_1': request.POST.get('request_1', ''),
            'request_2': request.POST.get('request_2', ''),
            'request_3': request.POST.get('request_3', ''),
        }

        # Prepare the prompt for the Gemini model
        prompt = f"Evaluate the following answers: {user_answers}"

        # Generate content using the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Assuming the response contains the evaluation and correct answers
        evaluation_result = response.text  # Get the generated content from the response

        # Here you would parse the evaluation_result to extract the score and correct answers
        # For demonstration, let's assume the evaluation result is a dictionary
        # You will need to adjust this based on the actual response format
        score = 0  # Replace with actual score extraction logic
        correct_answers = {}  # Replace with actual correct answers extraction logic

        # Store user answers and score in MongoDB
        collection.insert_one({
            'user_answers': user_answers,
            'score': score,
            'rank': determine_rank(score)  # Function to determine rank based on score
        })

        # Redirect to results page
        return render(request, 'survey/test_results.html', {
            'score': score,
            'total_questions': len(correct_answers),
            'correct_answers': correct_answers,
        })

    return render(request, 'survey/test.html')  # Render the test page if not a POST request

def determine_rank(score):
    if score >= 90:
        return 'Excellent'
    elif score >= 75:
        return 'Good'
    elif score >= 50:
        return 'Average'
    else:
        return 'Needs Improvement'