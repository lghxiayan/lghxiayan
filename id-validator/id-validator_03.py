from id_validator import validator
from faker import Faker

fake = Faker('ZH-CN')


def get_sex(sex_code):
    return '男' if sex_code == 1 else '女'


def generate_fake():
    name = fake.name()
    id_card_number = validator.fake_id(True, '黄梅县')
    sex = get_sex(validator.get_info(id_card_number)['sex'])
    birthday = validator.get_info(id_card_number)['birthday_code']
    street_address = fake.street_address()
    address = validator.get_info(id_card_number)['address'] + street_address
    age = validator.get_info(id_card_number)['age']
    phone_number = fake.phone_number()
    return name, id_card_number, sex, birthday, address, age, phone_number


print(generate_fake())
