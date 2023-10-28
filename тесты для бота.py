import pytest
from unittest.mock import Mock

from main import *
from main import but1
from main import but2
from main import text
from main import information
from main import but5
from main import but3
from main import but4


#главное меню
@pytest.mark
def start_test():
    message = Mock()
    user(message)

    message.answer.assert_called_with(hello_text)
    message.answer.assert_called_with(get('https://i.pinimg.com/564x/59/f9/b2/59f9b2507ccd8bfcfd40a32f39a57373.jpg').content)


@pytest.mark
def menu_test1():
    message = 'начнем!'
    menu(message)

    message.answer.assert_called_with(main_menu_text)


@pytest.mark
def menu_test2():
    message = 'главное меню'
    menu(message)

    message.answer.assert_called_with(main_menu_text)

@pytest.mark
def menu_test3():
    message = '/start'
    menu(message)

    message.answer.assert_called_with('Сейчас бот будет перезапущен!')

@pytest.mark
def menu_test3():
    message = Mock
    menu(message)

    message.answer.assert_called_with(mistake_text)


#погода
@pytest.mark
def pogoda_test():
    message = 'погода ⛅'
    menu(message)

    message.answer.assert_called_with(get('https://i.pinimg.com/564x/0e/91/4d/0e914de3125362a619b969be10b291a7.jpg').content)
    message.answer.assert_called_with('Погода в каком городе требуется?')


@pytest.mark
def pogoda_test1():
    message = 'Moscow'
    menu(message)

    message.answer.assert_called_with(information)

@pytest.mark
def pogoda_test2():
    message = Mock
    get_weathers(message)

    message.answer.assert_called_with('❗❗Город не найден, повторите запрос! ❗❗')

@pytest.mark
def pogoda_test3():
    message ='сменить город'
    next_step(message)

    message.answer.assert_called_with(pogoda(message))

@pytest.mark
def pogoda_test4():
    message ='главное меню'
    next_step(message)


    message.answer.assert_called_with(quit(message))

@pytest.mark
def pogoda_test4():
    next_step(message)
    message = Mock

    message.answer.assert_called_with('❗❗Город не найден, повторите запрос! ❗❗')


#помощь
@pytest.mark
def help_test():
    message = 'помощь 🆘'
    menu(message)

    message.answer.assert_called_with('Выбери кнопку')


@pytest.mark
def help_test1():
    message = 'что ты умеешь?'
    help(message)

    message.answer.assert_called_with(text)

@pytest.mark
def help_test3():
    message = 'главное меню'
    help(message)

    message.answer.assert_called_with(quit(message))


@pytest.mark
def help_test4():
    message = Mock
    help(message)

    message.answer.assert_called_with('Ошибка, воспользуйся кнопками')


#валюты
@pytest.mark
def test_start():
    message = 'валюты 💸'
    menu(message)

    message.answer.assert_called_with(get('https://i.pinimg.com/564x/91/d0/56/91d05626656a100f22c9fb3fdfa4ae34.jpg').content)
    message.answer.assert_called_with('Введите сумму (целым числом) в той валюте, которую хотите перевести 🤑')


@pytest.mark
def test_start1():
    message = 'доллар'
    summa_next(message)

    message.answer.assert_called_with(text)

@pytest.mark
def test_start2():
    message = 'евро'
    summa_next(message)

    message.answer.assert_called_with(text)


@pytest.mark
def test_start3():
    message = 'главное меню'
    summa_next(message)


    message.answer.assert_called_with(quit(message))

@pytest.mark
def test_start4():
    message = Mock
    summa_next(message)

    message.answer.assert_called_with('Неверно - воспользуйся кнопками!')

@pytest.mark
def test_start5():
    message = 'перевести еще'
    step_on(message)

    message.answer.assert_called_with('https://i.pinimg.com/564x/91/d0/56/91d05626656a100f22c9fb3fdfa4ae34.jpg'.content)
    message.answer.assert_called_with('Введите сумму (целым числом) в той валюте, которую хотите перевести 🤑')


@pytest.mark
def test_start6():
    message = 'главное меню'
    step_on(message)

    message.answer.assert_called_with(quit(message))

#дедлайны
@pytest.mark
def dead_test():
    message = 'дедлайны 🚩'
    menu(message)

    message.answer.assert_called_with('Что требуется сделать?')

@pytest.mark
def dead_tes1():
    message = 'добавить дедлайн'
    dead(message)

    message.answer.assert_called_with('Введи задачу')

@pytest.mark
def dead_tes2():
    message = Mock
    dead2(message)

    message.answer.assert_called_with('Введи дату дедлайна')

@pytest.mark
def dead_tes3():
    message = Mock
    dead2(message)

    message.answer.assert_called_with('задача добавлена!')



@pytest.mark
def dead_tes4():
    message = 'удалить дедлайн'
    dead(message)

    message.answer.assert_called_with('Что ты хочешь сделать?')



@pytest.mark
def dead_tes5():
    message = 'очистить дедлайны'
    delete(message)

    message.answer.assert_called_with('Супер! - все дедлайны очищены')



@pytest.mark
def dead_tes6():
    message = 'назад'
    delete(message)


    message.answer.assert_called_with(get('https://i.pinimg.com/564x/df/e6/fd/dfe6fd9d64c7702febd24e50153525e3.jpg').content)
    message.answer.assert_called_with('Что требуется сделать?')





































