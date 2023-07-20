from django.test import TestCase
from .models import City
from .views import find_money_values, mean, insert_data
# Create your tests here.


testText = "The average total cost in Paris for one day can vary depending on individual preferences and spending habits. However, as a rough estimate, you can expect to spend around €150 to €250 per person per day in Paris. This estimate includes accommodation, meals, transportation, attractions, and miscellaneous expenses.Please note that this estimate is a general guideline and actual costs may vary. It's always a good idea to plan and budget according to your specific preferences, activities, and spending patterns."


class parsingTestCase(TestCase):
    def test_parsing(self):
        '''This test case checks that the `find_money_values` function correctly parses money values from a string.
        A string containing two money values, "150" and "250" is passed to the function.
        The `find_money_values` function is called on the string and function should return a list containing the two money values.
        '''
        money_values = find_money_values(testText)
        self.assertEqual(money_values, [150, 250])

    def test_mean(self):
        '''This test case checks that the `mean` function correctly calculates the mean of a list of numbers.
        A list of numbers, [150, 250] given as input to the function in previous test case.
        The `mean` function is called on the list. The function should return the mean of the numbers, which is 200
        '''
        money_values = find_money_values(testText)
        self.assertEqual(mean(money_values), 200)


class CityModelTest(TestCase):

    def test_create_city(self):
        '''This test case checks that the `CityModel` class can correctly create a new city object.
        The city object should have the correct name, price, and date_created.
        '''
        name = "New York"
        price = 100000
        date = "2023-07-20"

        city = City.objects.create(name=name, price=price, date_created=date)

        self.assertEqual(city.name, name)
        self.assertEqual(city.price, price)
        self.assertEqual(city.date_created, date)

    def test_get_city_by_name(self):
        '''This test case checks that the `CityModel` class can correctly retrieve a city object by name.
        The retrieved city object should have the same name, price, and date_created as the original city object
        '''
        name = "New York"
        price = 100000
        date = "2023-07-20"

        city = City.objects.create(name=name, price=price, date_created=date)

        city_from_db = City.objects.get(name=name)
        self.assertEqual(city, city_from_db)
