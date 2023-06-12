from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос ключа возвращает статус 200 и сам ключ key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Фрэнк', animal_type='мопс', age='6', pet_photo='images/mops.jpg'):
    """Проверяем возможность добавления питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Удал', 'кот', '3', 'images/cat1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Обнов', animal_type='хомяк', age='3'):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert  result['name'] == name
    else:
        raise Exception('There is no my pets')


def test_create_pet_simple(name='Безфото', animal_type='жираф', age='4'):
    """Проверяем, что можно добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name,animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_no_data(name='', animal_type='', age=''):
    """Негативный тест: добавление питомца с пустыми данными в поле имя, тип животного и возраст"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_get_api_key_for_data_user_empty(email='', password=''):
    """Негативный тест: запрос ключа c пустыми значениями логина и пароля возвращает статус 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_add_pet_invalid_age(name='Тествозр', animal_type='кот', age='7878'):
    """Негативный тест: добавление питомца с неверным значением поля возраст"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert  result['age'] == age
    number = result['age']


def test_get_api_key_invalid_email(email=invalid_email, password=valid_email):
    """Негативный тест с неверным логином и с валидным паролем. Возврат 403 и проверка ключа"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_api_key_invalid_password(email=valid_email, password=invalid_password):
    """Негативный тест с валидным логином и неверным паролем. Возврат 403 и проверка ключа"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_add_pet_number_animal_type(name='Цифрокот', animal_type='123123', age='5'):
    """Негативный тест: добавление питомца с цифрами вместо букв в поле тип животного"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200


def test_add_pet_number_name(name='12341234', animal_type='енот', age='3'):
    """Негативный тест: добавление питомца с цифрами вместо имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200


def test_update_pet_photo(pet_photo='images/cat1.jpg'):
    """Тест: добавление фото к существующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Котофото", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] != ''
    print(status, result)
