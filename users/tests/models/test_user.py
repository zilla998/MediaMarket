from users.models import CustomUser


def test_create_user(db):
    CustomUser.objects.create_user(
        username="test_user", email="test@email.com", password="iuwhndwad"
    )

    assert CustomUser.objects.count() == 1

    get_user = CustomUser.objects.first()
    assert CustomUser.objects.all().count() == 1
    assert get_user.username == "test_user"
    assert get_user.email == "test@email.com"
