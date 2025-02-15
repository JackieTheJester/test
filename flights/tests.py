from django.test import TestCase, Client
from .models import Flight, Airport, Passenger

# Create your tests here.

class FlightTestCase(TestCase):
    def setUp(self):
        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create fligths.
        Flight.objects.create(origin = a1, destination = a2, duration=100)
        Flight.objects.create(origin = a1, destination = a1, duration=200)
        Flight.objects.create(origin = a1, destination = a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual (a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual (a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):  
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())
        
    def test_index(self):
        # Set up client to make request
        c = Client()

        # Send get request to index page and store response
        response = c.get("/flights/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure three flights are returned in the context
        self.assertEqual(response.context["flights"].count() , 3)

