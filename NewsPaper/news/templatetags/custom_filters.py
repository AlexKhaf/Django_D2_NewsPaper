from django import template

register = template.Library()
# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать
# и фильтры потеряются :(


@register.filter(name='censor')
# регистрируем наш фильтр под именем multiply, чтоб django понимал,
# что это именно фильтр, а не простая функция
def censor(value, arg):
    censor_list = [
        "ругательство",
        "оскорбление",
        "плохое_слово"
    ]
    for censor in censor_list:
        if value.find(censor) != -1:
            value = value.replace(censor,"***")
    return value