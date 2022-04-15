from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, StoreItem, PurchaseItem
# Create your tests here.
class StoreTests(TestCase):
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
    def test_call_view_fail_blank(self):
       self.user = User.objects.create_user(username='testuser', password='12345')
       self.client.login(username='testuser', password='12345')
       test1 = Profile.objects.create(user=self.user)
       test1.save()
       response = self.client.post('/store/',{})
       self.assertFormError(response, 'form', 'item', 'This field is required.')
    def test_regular_purchase_increment(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
    
        response = self.client.post('/store/',data={'item':discoBall.pk})
        discoBall.refresh_from_db()
        #verify times purchased was incremented
        expected = 1
        actual = discoBall.timesPurchased 
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_regular_purchase_points(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
    
        response = self.client.post('/store/',data={'item':discoBall.pk})
        test1.refresh_from_db()
        #verify times purchased was incremented
        expected = 80
        actual = test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_regular_purchase_fail(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 0)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
    
        response = self.client.post('/store/',data={'item':discoBall.pk})
        discoBall.refresh_from_db()
        #verify times purchased was incremented
        expected = 0
        actual = discoBall.timesPurchased 
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_regular_purchase_points_fail(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 10)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
    
        response = self.client.post('/store/',data={'item':discoBall.pk})
        test1.refresh_from_db()
        #verify times purchased was incremented
        expected = 10
        actual = test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_regular_purchase_inventory_item(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        print(len(inventory))
        expected = "disco ball"
        actual= inventory[0].item.name
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_regular_purchase_inventory_user(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        print(len(inventory))
        expected = "testuser"
        actual= inventory[0].user.username
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_regular_purchase_inventory_fail(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 0)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        expected = 0
        actual= len(inventory)
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_purchase_2_regular(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # create item to purchase
        world = StoreItem.objects.create(name="world",image="image\StoreAssets\WorldAsset.png",cost=50)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        response = self.client.post('/store/',data={'item':world.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        expected = 2
        actual= len(inventory)
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_purchase_2_points(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # create item to purchase
        world = StoreItem.objects.create(name="world",image="image\StoreAssets\WorldAsset.png",cost=50)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        response = self.client.post('/store/',data={'item':world.pk})
        test1.refresh_from_db()
        expected = 30
        actual= test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_purchase_2_same(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # create item to purchase
        world = StoreItem.objects.create(name="world",image="image\StoreAssets\WorldAsset.png",cost=50)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        response = self.client.post('/store/',data={'item':discoBall.pk})
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        expected = 2
        actual= len(inventory)
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))
    def test_purchase_2_same_points(self):
        # add user profile and log in
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user,pointsReceived = 100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(name="disco ball",image="image\StoreAssets\DiscoBallAsset.png",cost=20)
        # purchase
        response = self.client.post('/store/',data={'item':discoBall.pk})
        response = self.client.post('/store/',data={'item':discoBall.pk})
        test1.refresh_from_db()
        expected = 60
        actual= test1.pointsReceived
        self.assertEqual(actual,expected,"Expected " + str(expected) + " but was " + str(actual))

