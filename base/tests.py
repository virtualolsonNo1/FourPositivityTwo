from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, StoreItem, PurchaseItem

# Create your tests here.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Do all setup")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_profile_creation(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile 
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)

        # set expected
        expected = 100

        self.assertEqual(test1.pointsReceived,expected,"pointsReceived created correctly")

    def test_shopItem_creation(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')


        # create shop item 
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)

        # set expected
        expected = 20

        self.assertEqual(discoBall.cost,expected,"shop item created correctly")

    def test_purchasedItem_creation(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile 
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)

        # create shop item 
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)

        # create PurchaseItem 
        discoPurchase = PurchaseItem.objects.create(item=discoBall,user=self.user)

        # set expected
        expected = "testuser"

        self.assertEqual(discoPurchase.user.username,expected,"purchasedItem created correctly")