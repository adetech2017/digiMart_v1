import pytest
from django.contrib.auth import get_user_model
from buyer.models import Buyer

@pytest.mark.django_db
def test_buyer_model():
    # Create a test user using the custom user model (core.models.User)
    user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    # Create a Buyer instance using the user created above
    buyer = Buyer.objects.create(
        user=user,
        user_type='buyer',
        gender='Male',
        phone_number='1234567890',
        address='123 Main St, City',
    )

    # Assert that the buyer object has been created correctly
    assert buyer.user.username == 'testuser'
    assert buyer.user.email == 'test@example.com'
    assert buyer.user.check_password('testpassword')
    assert buyer.user_type == 'buyer'
    assert buyer.gender == 'Male'
    assert buyer.phone_number == '1234567890'
    assert buyer.address == '123 Main St, City'
    assert buyer.groups.count() == 0  # Buyer should not have any groups initially

    # Test the __str__ method of the Buyer model
    assert str(buyer) == 'testuser'
