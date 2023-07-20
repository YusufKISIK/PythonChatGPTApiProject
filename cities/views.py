from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import City
import openai
from statistics import mean
import psycopg2
import re
from datetime import datetime
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY
# Create your views here.

hostname = 'localhost'
database = 'CountryPriceList'
username = 'postgres'
pwd = '8686'
port = 5432
conn = None
cur = None

valueOfCity = 0


def index(request):
    cities = City.objects.all()
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append(
                {"role": "user", "content": "what will be avarage total cost in euro in " +
                 prompt + " for one day without give me breakdown of expected costs"})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=200,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append(
                {"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            print(formatted_response)
            money_values = find_money_values(formatted_response)
            costs = mean(money_values)
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            insert_data(prompt, costs, dt_string)

            return render(request, 'cities/index.html', {'Cities': cities})
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': ''
            }
            return render(request, 'cities/index.html', {'Cities': cities})
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')


def details(request, city_name):
    city = get_object_or_404(City, pk=city_name)
    return render(request, 'cities/detail.html', {'city': city})
    cities = City.objects.all()
    return render(request, 'cities/index.html', {'cities': cities})


# this is the view for handling errors


def error_handler(request):
    return render(request, 'cities/error.html')


def find_money_values(text):
    # Regular expression pattern to match money values
    pattern = r'[€$£][0-9,]+(?:\.[0-9]{2})?'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    # Remove the Euro(€) sign and commas, and convert to float
    money_values = [float(match.replace('€', '').replace(',', ''))
                    for match in matches]
    return money_values


def insert_data(name, price, date):  # insert data into the database
    try:
        conn = psycopg2.connect(host=hostname, user=username,
                                password=pwd, dbname=database, port=port)
        cur = conn.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS cities_city (
            Name varchar(50) NOT NULL, Price int NOT NULL, date_created varchar(50) NOT NULL)'''  # create the table if it does not exist
        cur.execute(create_table_query)

        select_query = '''SELECT * FROM cities_city WHERE Name = %s'''  # check if the city already exists in the database
        cur.execute(select_query, (name,))
        rows = cur.fetchall()

        if len(rows) == 0:  # if the city does not exist in the database
            insert_query = '''INSERT INTO cities_city ( 
                Name, Price, date_created) VALUES (%s, %s, %s)'''
            record_to_insert = (name, price, date)
            print(record_to_insert)
            cur.execute(insert_query, record_to_insert)
            conn.commit()
            print("Data inserted successfully into table")
        else:  # if the city already exists in the database.
            print("City already exists in the database")

    except Exception as error:  # if there is an error
        print("I am unable to connect to the database. Because: ", error)

    finally:  # close the connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
