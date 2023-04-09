from src.utils.helpers import get_random_img


def test_get_random_img():
    img_names = ["img/1.png", "img/2.png", "img/3.png"]
    assert get_random_img(img_names) in img_names
