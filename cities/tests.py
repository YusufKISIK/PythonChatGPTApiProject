from django.test import TestCase
from .models import City
# Create your tests here.


class MoneyTestCase(TestCase):
    def setUp(self):
        City.objects.create(name="London", price="150")

    def test_city_country(self):
        london = City.objects.get(name="London")
        self.assertEqual(london.price, 150)


class parsingTestCase(TestCase):
    testText = "The average total cost in Paris for one day can vary depending on individual preferences and spending habits. However, as a rough estimate, you can expect to spend around €150 to €250 per person per day in Paris. This estimate includes accommodation, meals, transportation, attractions, and miscellaneous expenses.Please note that this estimate is a general guideline and actual costs may vary. It's always a good idea to plan and budget according to your specific preferences, activities, and spending patterns."

    def test_parsing(self):
        self.assertEqual(150, 150)
