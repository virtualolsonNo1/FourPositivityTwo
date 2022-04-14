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
    def test_purchasedItem_purchase(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile 
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)

        # create shop item 
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)

        # create PurchaseItem 
        discoPurchase = PurchaseItem.objects.create(item=discoBall,user=self.user)

        # set expected
        PurchaseItem.purchase(discoBall,test1)
        expected = 80
        actual = test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but user had " + str(actual) + " points")
    def test_purchasedItem_purchaseLarger(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile 
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)

        # create shop item 
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=50)

        # set expected
        PurchaseItem.purchase(discoBall,test1)
        expected = 50
        actual = test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but user had " + str(actual) + " points")

    def test_purchasedItem_purchaseFailed(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile 
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)

        # create shop item 
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=150)

        # set expected
        PurchaseItem.purchase(discoBall,test1)
        expected = 100
        actual = test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but user had " + str(actual) + " points")
    def test_purchasedItem_purchaseFullCost(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile 
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)

        # create shop item 
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=100)

        # set expected
        PurchaseItem.purchase(discoBall,test1)
        expected = 0
        actual = test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but user had " + str(actual) + " points")
    def test_store_deny_anonymous(self):
        response = self.client.get('/store/', follow=True)
        expected = '/login/?next=%2Fstore%2F'
        self.assertRedirects(response, expected)

    def test_call_view_load(self):
       self.user = User.objects.create_user(username='testuser', password='12345')
       self.client.login(username='testuser', password='12345')
       test1 = Profile.objects.create(user=self.user)
       test1.save()
       response = self.client.get('/store/')
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'base/store.html')

   