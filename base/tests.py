import email
from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, StoreItem, PurchaseItem, Message
from .views import updatePoints, getPoints
from datetime import datetime
import datetime as dt
from updateservice.update import notifyUsers, updateDailyPoints, notifyUsers
# Create your tests here.


class StoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Do all setup")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_profile_creation(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        # set expected
        expected = 100
        self.assertEqual(test1.pointsReceived, expected,
                         "pointsReceived created correctly")

    def test_shopItem_creation(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create shop item
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # set expected
        expected = 20
        self.assertEqual(discoBall.cost, expected,
                         "shop item created correctly")

    def test_purchasedItem_creation(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        # create shop item
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # create PurchaseItem
        discoPurchase = PurchaseItem.objects.create(
            item=discoBall, user=self.user)
        # set expected
        expected = "testuser"
        self.assertEqual(discoPurchase.user.username, expected,
                         "purchasedItem created correctly")

    def test_purchasedItem_purchase(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        # create shop item
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # create PurchaseItem
        discoPurchase = PurchaseItem.objects.create(
            item=discoBall, user=self.user)
        # set expected
        PurchaseItem.purchase(discoBall, test1)
        expected = 80
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but user had " + str(actual) + " points")

    def test_purchasedItem_purchaseLarger(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        # create shop item
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=50)
        # set expected
        PurchaseItem.purchase(discoBall, test1)
        expected = 50
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but user had " + str(actual) + " points")

    def test_purchasedItem_purchaseFailed(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        # create shop item
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=150)
        # set expected
        PurchaseItem.purchase(discoBall, test1)
        expected = 100
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but user had " + str(actual) + " points")

    def test_purchasedItem_purchaseFullCost(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        # create shop item
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=100)
        # set expected
        PurchaseItem.purchase(discoBall, test1)
        expected = 0
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but user had " + str(actual) + " points")
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but user had " + str(actual) + " points")

    def test_store_deny_anonymous(self):
        response = self.client.get('/store/', follow=True)
        expected = '/login/?next=%2Fstore%2F'
        self.assertRedirects(response, expected)

    def test_call_view_load(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user)
        test1.save()
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/store.html')

    def test_call_view_fail_blank(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user)
        test1.save()
        response = self.client.post('/store/', {})
        self.assertFormError(response, 'form', 'item',
                             'This field is required.')

    def test_regular_purchase_increment(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase

        response = self.client.post('/store/', data={'item': discoBall.pk})
        discoBall.refresh_from_db()
        # verify times purchased was incremented
        expected = 1
        actual = discoBall.timesPurchased
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_purchase_points(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase

        response = self.client.post('/store/', data={'item': discoBall.pk})
        test1.refresh_from_db()
        # verify times purchased was incremented
        expected = 80
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_purchase_fail(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=0)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase

        response = self.client.post('/store/', data={'item': discoBall.pk})
        discoBall.refresh_from_db()
        # verify times purchased was incremented
        expected = 0
        actual = discoBall.timesPurchased
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_purchase_points_fail(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=10)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase

        response = self.client.post('/store/', data={'item': discoBall.pk})
        test1.refresh_from_db()
        # verify times purchased was incremented
        expected = 10
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_purchase_inventory_item(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        print(len(inventory))
        expected = "disco ball"
        actual = inventory[0].item.name
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_purchase_inventory_user(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        print(len(inventory))
        expected = "testuser"
        actual = inventory[0].user.username
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_purchase_inventory_fail(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=0)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        expected = 0
        actual = len(inventory)
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_purchase_2_regular(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # create item to purchase
        world = StoreItem.objects.create(
            name="world", image="image\StoreAssets\WorldAsset.png", cost=50)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        response = self.client.post('/store/', data={'item': world.pk})
        test1.refresh_from_db()
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        expected = 2
        actual = len(inventory)
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_purchase_2_points(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # create item to purchase
        world = StoreItem.objects.create(
            name="world", image="image\StoreAssets\WorldAsset.png", cost=50)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        response = self.client.post('/store/', data={'item': world.pk})
        test1.refresh_from_db()
        expected = 30
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_purchase_2_same(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # create item to purchase
        world = StoreItem.objects.create(
            name="world", image="image\StoreAssets\WorldAsset.png", cost=50)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        response = self.client.post('/store/', data={'item': discoBall.pk})
        inventory = PurchaseItem.objects.filter(user=test1.user.id)
        expected = 2
        actual = len(inventory)
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_purchase_2_same_points(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        # create item to purchase
        discoBall = StoreItem.objects.create(
            name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
        # purchase
        response = self.client.post('/store/', data={'item': discoBall.pk})
        response = self.client.post('/store/', data={'item': discoBall.pk})
        test1.refresh_from_db()
        expected = 60
        actual = test1.pointsReceived
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))
class MessageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Do all setup")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_message_creation(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test2 = Profile.objects.create(user=user2)

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy", pointTotal=20)

        # test message was sent as user has enough points to start
        success = updatePoints(self.user, user2, message.pointTotal)

        # set expected
        expected = ""

        self.assertEquals(success, expected, "message created successfully")

    def test_message_creation_correct_body(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test2 = Profile.objects.create(user=user2)

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy", pointTotal=20)

        # test message was sent as user has enough points to start
        text = message.body

        # set expected
        expected = "Howdy"

        self.assertEqual(
            text, expected, "message created successfully with correct body")

    def test_message_creation_correct_point_total(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test2 = Profile.objects.create(user=user2)

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy", pointTotal=20)

        # test message was sent as user has enough points to start
        text = message.pointTotal

        # set expected
        expected = 20

        self.assertEqual(
            text, expected, "message created successfully with correct point total")

    def test_correct_message_points_sender_update_points(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(
            user=self.user, pointsReceived=100, pointsToSend=100)
        test2 = Profile.objects.create(user=user2)

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy", pointTotal=20)

        # test message was sent as user has enough points to start
        updatePoints(self.user, user2, message.pointTotal)
        test1.refresh_from_db()
        actual = test1.pointsToSend

        # set expected
        expected = 80

        self.assertEqual(actual, expected,
                         "correct number of points subtracted from sender")

    def test_correct_message_points_receiver_update_points(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        user2.save()
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2)
        test2.save()

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # test message was sent as user has enough points to start
        pointTotal = getPoints(message.body)
        updatePoints(self.user, user2, pointTotal)

        print(test2.pointsReceived)
        print(test1.pointsToSend)
        test2.refresh_from_db()
        actual = test2.pointsReceived

        # set expected
        expected = 20

        self.assertEqual(actual, expected,
                         "correct number of points subtracted from sender")

    def test_correct_point_total_no_points_get_points(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy", pointTotal=0)

        # test message was sent as user has enough points to start
        actual = getPoints(message.body)

        # set expected
        expected = 0

        self.assertEqual(
            actual, expected, "correct number of points allotted to message (0 points)")

    def test_correct_point_total_lots_of_points_get_points(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy 💯💯💯", pointTotal=0)

        # test message was sent as user has enough points to start
        actual = getPoints(message.body)

        # set expected
        expected = 300

        self.assertEqual(
            actual, expected, "correct number of points allotted to message (300 points)")

    def test_too_many_points_no_message_sent_update_points(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user)
        test1.save()
        test2 = Profile.objects.create(user=user2)
        test2.save()

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy 💯💯💯", pointTotal=300)

        # test message was sent as user has enough points to start
        success = updatePoints(self.user, user2, 300)
        actual = "Error not enough sender points!"

        # check success is false
        self.assertEquals(
            success, actual, "properly updated points despite the sending user not having enough points to send this message")

    def test_create_message_form_working_status_code(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # set response
        response = self.client.post(reverse("create-message"))

        self.assertEquals(response.status_code, 200,
                          "messaging (specifically createMessage) did not work when logged in, whereas it should")

    def test_create_message_form_not_working_status_code_not_logged_in(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)
        # set response
        response = self.client.post(reverse("create-message"))

        # set expected
        self.assertNotEquals(response.status_code, 200,
                             "messaging worked when not logged in, which shouldn't be possible")

    def test_call_view_fail_blank_message_receiver_field(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user)
        test1.save()
        response = self.client.post('/create-message/', {})
        self.assertFormError(response, 'form', 'receiver',
                             'This field is required.')

    def test_call_view_fail_blank_message_body_field(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        test1 = Profile.objects.create(user=self.user)
        test1.save()
        response = self.client.post('/create-message/', {})
        self.assertFormError(response, 'form', 'body',
                             'This field is required.')

    def test_regular_message_sent_correct_sender_points_post_request(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        response = self.client.post(
            '/create-message/', {'receiver': user2.pk, 'body': "Howdy✨✨"})
        test1.refresh_from_db()
        # verify correct updated sender points
        actual = test1.pointsToSend
        expected = 60
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_regular_message_sent_correct_receiver_points_post_request(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        response = self.client.post(
            '/create-message/', {'receiver': user2.pk, 'body': "Howdy✨✨"})
        test2.refresh_from_db()
        # verify correct updated receiver points
        actual = test2.pointsReceived
        expected = 140
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_no_login_message_unsent_unchanged_receiver_points_post_request(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        response = self.client.post(
            '/create-message/', {'receiver': user2.pk, 'body': "Howdy💯"})
        test2.refresh_from_db()
        # verify unchanged receiver points
        actual = test2.pointsReceived
        expected = 100
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_no_login_message_unsent_unchanged_sender_points_post_request(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        response = self.client.post(
            '/create-message/', {'receiver': user2.pk, 'body': "Howdy💯"})
        test1.refresh_from_db()
        # verify unchanged sender points
        actual = test1.pointsToSend
        expected = 100
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_message_deny_anonymous_create_message(self):
        response = self.client.post('/create-message/', follow=True)
        expected = '/login/?next=%2Fcreate-message%2F'
        self.assertRedirects(response, expected)
class LeaderboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Do all setup")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_deny_anonymous_leaderboard(self):
        response = self.client.post('/leaderboard/', follow=True)
        expected = '/login/?next=%2Fleaderboard%2F'
        # redirects to login page if not logged in when click on leaderboard
        self.assertRedirects(response, expected)

    def test_leaderboard_correct_top_profile(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        # create message
        Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # refresh profiles points
        test1.refresh_from_db()
        test2.refresh_from_db()

        # get leaderboard context and top senders
        response = self.client.get('/leaderboard/')
        context = response.context
        topSenders = context['topSenders']

        # verify correct user at the top
        actual = topSenders[0].user.username
        expected = str(test1)
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_leaderboard_correct_second_profile(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # refresh profiles points
        test1.refresh_from_db()
        test2.refresh_from_db()

        # get leaderboard context and top senders
        response = self.client.get('/leaderboard/')
        context = response.context
        topSenders = context['topSenders']

        # verify correct user at the top
        actual = topSenders[1].user.username
        expected = str(test2)
        self.assertEqual(actual, expected, "Expected " +
                         str(expected) + " but was " + str(actual))

    def test_leaderboard_form_not_working_status_code_not_logged_in(self):
        # set response
        response = self.client.post(reverse("leaderboard"))

        # set expected
        self.assertNotEquals(response.status_code, 200,
                             "leaderboard worked when not logged in, which shouldn't be possible")

    def test_leaderboard_working_status_code(self):
        # set response
        response = self.client.post(reverse("leaderboard"))

        self.assertEquals(response.status_code, 302,
                          "leaderboard did not work when logged in, whereas it should")

    def test_leaderboard_working_context_top_senders_top_sender(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # refresh profiles points
        test1.refresh_from_db()
        test2.refresh_from_db()

        # set response
        response = self.client.post('/leaderboard/')
        context = response.context['topSenders']

        self.assertEquals(context[0].user.username, "testuser",
                          "leaderboard did not work when logged in, whereas it should")

    def test_leaderboard_working_context_top_senders_second_sender(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # refresh profiles points
        test1.refresh_from_db()
        test2.refresh_from_db()

        # set response
        response = self.client.post('/leaderboard/')
        context = response.context['topSenders']

        self.assertEquals(context[1].user.username, "testuser2",
                          "leaderboard did not work when logged in, whereas it should")

    def test_leaderboard_working_context_top_senders_max_length_ten(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        user3 = User.objects.create_user(
            username='testuser3', password='12345')
        user4 = User.objects.create_user(
            username='testuser4', password='12345')
        user5 = User.objects.create_user(
            username='testuser5', password='12345')
        user6 = User.objects.create_user(
            username='testuser6', password='12345')
        user7 = User.objects.create_user(
            username='testuser7', password='12345')
        user8 = User.objects.create_user(
            username='testuser8', password='12345')
        user9 = User.objects.create_user(
            username='testuser9', password='12345')
        user10 = User.objects.create_user(
            username='testuser10', password='12345')
        user11 = User.objects.create_user(
            username='testuser11', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        test3 = Profile.objects.create(user=user3, pointsReceived=100)
        test3.save()
        test4 = Profile.objects.create(user=user4, pointsReceived=100)
        test4.save()
        test5 = Profile.objects.create(user=user5, pointsReceived=100)
        test5.save()
        test6 = Profile.objects.create(user=user6, pointsReceived=100)
        test6.save()
        test7 = Profile.objects.create(user=user7, pointsReceived=100)
        test7.save()
        test8 = Profile.objects.create(user=user8, pointsReceived=100)
        test8.save()
        test9 = Profile.objects.create(user=user9, pointsReceived=100)
        test9.save()
        test10 = Profile.objects.create(user=user10, pointsReceived=100)
        test10.save()
        test11 = Profile.objects.create(user=user11, pointsReceived=100)
        test11.save()

        # set response
        response = self.client.post('/leaderboard/')
        context = response.context['topSenders']

        self.assertEquals(
            len(context), 10, "leaderboard did not work when logged in, whereas it should")

    def test_leaderboard_working_context_page(self):
        # add user profile and log in
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2, pointsReceived=100)
        test2.save()
        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # refresh profiles points
        test1.refresh_from_db()
        test2.refresh_from_db()

        # set response
        response = self.client.post('/leaderboard/')
        context = response.context['page']

        self.assertEquals(context, "Leaderboard",
                          "leaderboard did not work when logged in, whereas it should")

class ProfileTests(TestCase):
        @classmethod
        def setUpTestData(cls):
                print("Do all setup")

        def setUp(self):
                # create user
                self.user = User.objects.create_user(
                username='testuser', password='12345')
                self.client.login(username='testuser', password='12345')
                test1 = Profile.objects.create(user=self.user,pointsReceived=50)
                test1.save()
                pass
        def test_store_deny_anonymous(self):
                self.client.logout()
                response = self.client.get('/profile/', follow=True)
                expected = '/login/?next=%2Fprofile%2F'
                self.assertRedirects(response, expected)

        def test_call_view_load(self):
                response = self.client.get('/profile/')
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'base/profile.html')

        def test_profile_self_username(self):
                response = self.client.get('/profile/')
                expected = 'testuser'
                userContext= response.context['user']
                actual = userContext.username
                print(actual)
                self.assertEqual(actual,expected,"username was not as expected")
        def test_profile_self_inventory(self):
                # create item to purchase
                discoBall = StoreItem.objects.create(
                name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
                # purchase
                response = self.client.post('/store/', data={'item': discoBall.pk})
                self.user.refresh_from_db()

                # get page
                response = self.client.get('/profile/')
                actual = response.context['inventory'][0]
                inventoryExp = PurchaseItem.objects.filter(user=self.user)
                expected = inventoryExp[0]

                # check response is as expected
                print(actual)
                self.assertEqual(actual,expected,"inventory was not as expected")

        def test_profile_other_username(self):
                # create another user profile
                user2 = User.objects.create_user(
                username='testuser2', password='12345')
                test2 = Profile.objects.create(user=user2, pointsReceived=100)
                test2.save()

                response = self.client.post('/profile/',data={'user': test2.pk})
                expected = 'testuser'
                userContext= response.context['user']
                actual = userContext.username
                print(actual)
                self.assertEqual(actual,expected,"username was not as expected")
        def test_profile_other_inventoryEmpty(self):
                # create another user profile
                user2 = User.objects.create_user(
                username='testuser2', password='12345')
                test2 = Profile.objects.create(user=user2, pointsReceived=100)
                test2.save()
                # create item to purchase as test1 
                discoBall = StoreItem.objects.create(
                name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
                # purchase as test1 
                response = self.client.post('/store/', data={'item': discoBall.pk})
                self.user.refresh_from_db()

                # get page
                response = self.client.post('/profile/',data={'user': test2.pk})
                actual = len(response.context['inventory'])
                inventoryExp = PurchaseItem.objects.filter(user=self.user)
                expected = len(inventoryExp)

                # check response is as expected
                print(actual)
                self.assertEqual(actual,expected,"inventory was not as expected")
        def test_profile_other_inventory(self):
                # create another user profile
                user2 = User.objects.create_user(
                username='testuser2', password='12345')
                test2 = Profile.objects.create(user=user2, pointsReceived=100)
                test2.save()
                self.client.logout()
                self.client.login(username='testuser2', password='12345')

                # create item to purchase as test2
                discoBall = StoreItem.objects.create(
                name="disco ball", image="image\StoreAssets\DiscoBallAsset.png", cost=20)
                # purchase as test2
                response = self.client.post('/store/', data={'item': discoBall.pk})
                test2.refresh_from_db()

                # get page
                response = self.client.post('/profile/',data={'user': user2.pk})
                actual = response.context['inventory'][0]
                inventoryExp = PurchaseItem.objects.filter(user=user2)
                expected = inventoryExp[0]

                # check response is as expected
                print(actual)
                self.assertEqual(actual,expected,"inventory was not as expected")

class HomeTests(TestCase):
        @classmethod
        def setUpTestData(cls):
                print("Do all setup")

        def setUp(self):
                pass
        def test_call_view_load(self):
            response = self.client.get('')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'base/home.html')
        def test_home_loggedout_page(self):
            response = self.client.get('')
            actual = response.context['page']
            expected = 'Home'
            # check response is as expected
            self.assertEqual(actual,expected,"page was not as expected")
        def test_home_loggedout_message_count(self):
            response = self.client.get('')
            actual = 'message_count' in response.context
            expected = False
            # check response is as expected
            self.assertEqual(actual,expected,"message_count was not as expected") 
        def test_home_loggedout_messages_to(self):
                response = self.client.get('')
                actual = 'messages_to' in response.context
                expected = False
                # check response is as expected
                self.assertEqual(actual,expected,"messages were not as expected")   
        def test_home_loggedout_senders(self):
                response = self.client.get('')
                actual = 'senders' in response.context
                expected = False
                # check response is as expected
                self.assertEqual(actual,expected,"senders were not as expected")         
        def test_home_loggedin_page(self):
            # create user
            self.user = User.objects.create_user(
            username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            test1 = Profile.objects.create(user=self.user,pointsReceived=50)
            test1.save()
            response = self.client.get('')
            actual = response.context['page']
            expected = 'Home'
            # check response is as expected
            self.assertEqual(actual,expected,"page was not as expected")
        def test_home_loggedin_message_count_one(self):
            # add user profile and log in
            self.user = User.objects.create_user(
                username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            user2 = User.objects.create_user(
                username='testuser2', password='12345')
            test1 = Profile.objects.create(user=self.user, pointsReceived=100)
            test1.save()
            test2 = Profile.objects.create(user=user2, pointsReceived=100)
            test2.save()

            # create message 
            response = self.client.post(
                '/create-message/', {'receiver': user2.pk, 'body': "Howdy✨✨"})
            test2.refresh_from_db()

            # login as test2 
            self.client.logout()
            self.client.login(username='testuser2', password='12345')
            
            response = self.client.get('')
            actual = response.context['message_count']
            expected = 1
            # check response is as expected
            self.assertEqual(actual,expected,"message_count was not as expected")  
        def test_home_loggedin_message_count_two(self):
            # add user profile and log in
            self.user = User.objects.create_user(
                username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            user2 = User.objects.create_user(
                username='testuser2', password='12345')
            test1 = Profile.objects.create(user=self.user, pointsReceived=100)
            test1.save()
            test2 = Profile.objects.create(user=user2, pointsReceived=100)
            test2.save()

            # create message 
            response = self.client.post(
                '/create-message/', {'receiver': user2.pk, 'body': "Howdy✨✨"})
            response = self.client.post(
                '/create-message/', {'receiver': user2.pk, 'body': "Howdy again✨✨"})
            test2.refresh_from_db()

            # login as test2 
            self.client.logout()
            self.client.login(username='testuser2', password='12345')
            
            response = self.client.get('')
            actual = response.context['message_count']
            expected = 2
            # check response is as expected
            self.assertEqual(actual,expected,"message_count was not as expected")  
        def test_home_loggedout_messages_to(self):
            # create user
            self.user = User.objects.create_user(
            username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            test1 = Profile.objects.create(user=self.user,pointsReceived=50)
            test1.save()
            response = self.client.get('')
            actual = response.context['page']
            expected = 'Home'
            # check response is as expected
            self.assertEqual(actual,expected,"page was not as expected")
        def test_home_loggedin_message_to(self):
            # add user profile and log in
            self.user = User.objects.create_user(
                username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            user2 = User.objects.create_user(
                username='testuser2', password='12345')
            test1 = Profile.objects.create(user=self.user, pointsReceived=100)
            test1.save()
            test2 = Profile.objects.create(user=user2, pointsReceived=100)
            test2.save()

            # create message 
            response = self.client.post(
                '/create-message/', {'receiver': user2.pk, 'body': "Howdy✨✨"})
            test2.refresh_from_db()

            # login as test2 
            self.client.logout()
            self.client.login(username='testuser2', password='12345')

            response = self.client.get('')
            messages = response.context['messages_to']
            actual = messages[0].body
            expected = "Howdy✨✨"
            # check response is as expected
            self.assertEqual(actual,expected,"message was not as expected") 
        def test_home_loggedin_senders(self):
            # add user profile and log in
            self.user = User.objects.create_user(
                username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            user2 = User.objects.create_user(
                username='testuser2', password='12345')
            test1 = Profile.objects.create(user=self.user, pointsReceived=100)
            test1.save()
            test2 = Profile.objects.create(user=user2, pointsReceived=100)
            test2.save()

            # create message 
            response = self.client.post(
                '/create-message/', {'receiver': user2.pk, 'body': "Howdy✨✨"})
            test2.refresh_from_db()

            # login as test2 
            self.client.logout()
            self.client.login(username='testuser2', password='12345')

            response = self.client.get('')
            senders = response.context['senders']
            actual = senders[0].username
            expected = "testuser"
            # check response is as expected
            self.assertEqual(actual,expected,"senders were not as expected")         
class SettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Do all setup")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
    
    def test_deny_anonymous_settings(self):
        response = self.client.post('/settings/', follow=True)
        expected = '/login/?next=%2Fsettings%2F'
        # redirects to login page if not logged in when click on settings
        self.assertRedirects(response, expected)

    def test_settings_redirect_home(self):
            # add user profile and log in
            self.user = User.objects.create_user(username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            test1 = Profile.objects.create(user=self.user,pointsReceived = 100,email="test@gmail.com")
            test1.save()
            
            with open('base\static\media\earth-clipart-earth.png', 'rb') as f:
                data = {
                    "profilePic": f,
                    "email":"test@gmail.com"
                }

                # set response
                response = self.client.post('/settings/', data=data)
                expected = '/'
                self.assertRedirects(response, expected)
    def test_settings_redirect_home(self):
            # add user profile and log in
            self.user = User.objects.create_user(username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            test1 = Profile.objects.create(user=self.user,pointsReceived = 100,email="test@gmail.com")
            test1.save()
            

            # set response
            response = self.client.get('/settings/')
            actual =     response.context['page']
            expected = 'Settings'
            self.assertEqual(actual,expected,"Page was not as expected")    
    def test_settings_update_email(self):
            # add user profile and log in
            self.user = User.objects.create_user(username='testuser', password='12345')
            self.client.login(username='testuser', password='12345')
            test1 = Profile.objects.create(user=self.user,pointsReceived = 100,email="test@gmail.com")
            test1.save()
                
            with open('base\static\media\earth-clipart-earth.png', 'rb') as f:
                data = {
                    "profilePic": f,
                    "email":"test2@gmail.com"
                    }

                # set response
                self.client.post('/settings/', data=data)
                self.user.refresh_from_db()
                self.assertEquals('test2@gmail.com', self.user.email)

class UpdateServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Do all setup")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
    
    def test_update_points_at_midnight(self):
        self.user = User.objects.create_user(
        username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        user2.save()
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2)
        test2.save()

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # test message was sent as user has enough points to start
        pointTotal = getPoints(message.body)
        updatePoints(self.user, user2, pointTotal)

        updateDailyPoints(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        test1.refresh_from_db()
        actual = test1.pointsToSend

        # set expected
        expected = 100

        self.assertEqual(actual, expected,
                        "correct number of points allotted to all users")

    def test_dont_update_points_not_midnight(self):
        self.user = User.objects.create_user(
        username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        user2.save()
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2)
        test2.save()

        # create message
        message = Message.objects.create(
            sender=self.user, receiver=user2, body="Howdy✨", pointTotal=20)

        # test message was sent as user has enough points to start
        pointTotal = getPoints(message.body)
        updatePoints(self.user, user2, pointTotal)

        updateDailyPoints(datetime.now().replace(hour=0, minute=2, second=0, microsecond=0))
        test1.refresh_from_db()
        actual = test1.pointsToSend

        # set expected
        expected = 80

        self.assertEqual(actual, expected,
                        "correct number of points allotted to all users when not updated since it isn't midnight")

    def test_notify_user(self):
        self.user = User.objects.create_user(
        username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        user2.save()
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2)
        test2.save()

        # test message was sent as user has enough points to start
        test1.lastMessageSent = datetime(2022, 4, 30, 4, 5, 6)
        test1.save()
        test1.refresh_from_db()
        actual = notifyUsers()

        # set expected
        expected = True

        self.assertEqual(actual, expected,
                        "didn't send notification despite no message or notification having been sent in past 24 hours")

    def test_dont_notify_user(self):
        self.user = User.objects.create_user(
        username='testuser', password='12345')
        user2 = User.objects.create_user(
            username='testuser2', password='12345')
        user2.save()
        login = self.client.login(username='testuser', password='12345')

        # create profile
        test1 = Profile.objects.create(user=self.user, pointsReceived=100)
        test1.save()
        test2 = Profile.objects.create(user=user2)
        test2.save()

        # test message was sent as user has enough points to start
        test1.lastMessageSent = datetime(2022, 5, 2, 4, 5, 6)
        test1.save()
        test1.refresh_from_db()
        actual = notifyUsers()

        # set expected
        expected = False

        self.assertEqual(actual, expected,
                        "sent notification despite message or notification being sent in the past 24 hours")