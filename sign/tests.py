from django.test import TestCase
from sign.models import Event, Guest
# Create your tests here.

class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=11, name="bala bala", status=True, limit=200, address='shenzhen', start_time='2016-08-31 02:13:22')
        Guest.objects.create(id=1, event_id=11, realname="alen", phone='13710101010', email='alen@email.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="bala bala")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone="13710101010")
        self.assertEqual(result.realname, 'alen')
        self.assertFalse(result.sign)

