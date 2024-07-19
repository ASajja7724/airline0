from django.db.models import Max
from django.test import Client,TestCase

from .models import Airport, Flight, Passenger

# Create your tests here.
class FlightTestCase(TestCase):

    # set up dummy data to test the application - 
    # will do this is a seperate db that usres don't see

    def setUp(self):

        # create  dummy airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # create dummy flights
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=100) # should be invalid 
        Flight.objects.create(origin=a1, destination=a2, duration=-100) # should be invalid

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)
        # verify that 3 flights are departing
    
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)
        # verify that there is one arriavl
    
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)       
        self.assertTrue(f.is_valid_flight())
        # verify that this is a valid flight

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)       
        self.assertFalse(f.is_valid_flight())
        # verify that this is not a valid flight

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())
        # verify that this is not a valid flight 

    def test_index(self): # this will test the default /flights page 
        c = Client() # client making request
        response = c.get("/flights/") # respone from request
        self.assertEqual(response.status_code, 200)
        # the web page should load without error
        self.assertEqual(response.content["flights"].count(), 3)
        # check that we got 3 flights on the the index page

    def test_valid_flight_page(self): # checks if we can load a flight page
        a1 = Airport.objects.get(code="AAA")
        f = Airport.objects.get(origin=a1, destination=a1)

        c = Client()
        reponse = c.get(f"/flights/{f.id}")
        # load the flight page with the id of flight f
        self.assertEqual(reponse.status_code, 200)
        # check that a status code of 200 is being returned 
    
    def test_invalid_flight_page(self):
        # get a flight page with an index out of range of the db
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
        # - gets the largest possible id in the database

        c = Client()
        response = c.get(f"/flights/{max_id + 1}") # id is out of db range
        self.assertEqual(response.status_code, 404)
        # this should return a 404 code - meaniin that the page was not found

    def test_flight_page_passengers(self):
        f = Flight.objects.get(id=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.context["passengers"].count(), 1)
        # check only one passenger is inthe flight
