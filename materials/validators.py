from rest_framework.exceptions import ValidationError


def url_validator(url):
    """Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com"""
    test_url = 'https://youtube.com'
    if test_url not in url:
        raise ValidationError('Допускаются ссылки только на youtube.com')
