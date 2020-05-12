from yandex_testing_lesson import strip_punctuation_ru


def test():
    test_data = (('набор, слов', 'набор слов'),
                 ('другой набор. слов', 'другой набор слов'),
                 ('кое-как можно, но как именно', 'кое-как можно но как именно'),
                 ('три слова с', 'три слова с'),
                 ('хватит!', 'хватит'),
                 ('скука - это делать задачу и не понимать ошибки',
                  'скука это делать задачу и не понимать ошибки'))
    for i, j in test_data:
        try:
            out = strip_punctuation_ru(i)
            if out != j:
                return 'NO'
        except Exception:
            if j is not None:
                return 'NO'
    return 'YES'


print(test())