from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QButtonGroup
from random import shuffle, randint


class Question():
    '''
    содержит вопрос, правильный ответ и три неправильных
    '''
    # все строки надо задать при создании объекта, они запоминаются в свойства
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


app = QApplication([]) # создаем приложение
window = QWidget() # создаем окно
window.setWindowTitle('Memory Card')
window.resize(400, 300)


main_question = QLabel('Какой национальности не существует?')
button = QPushButton('Ответить')

# создаем переключатели
rad_but_1 = QRadioButton('Энцы')
rad_but_2 = QRadioButton('Смурфы')
rad_but_3 = QRadioButton('Чулымцы')
rad_but_4 = QRadioButton('Алеуты')

# создаем вертикаальные лейауты
v_lay_1 = QVBoxLayout()
v_lay_2 = QVBoxLayout()

# создаем горизонтальный лейаут
h_lay = QHBoxLayout()

# прикрепляем кнопки к вертикальным лейаутам, по две на каждый
v_lay_1.addWidget(rad_but_1)
v_lay_1.addWidget(rad_but_2)
v_lay_2.addWidget(rad_but_3)
v_lay_2.addWidget(rad_but_4)

# прикрепляем вертикальные лейауты к горизонтальному
h_lay.addLayout(v_lay_1)
h_lay.addLayout(v_lay_2)

# создаем "панель" с кнопками (GroupBox)
but_group = QGroupBox()

# помещаем туда лейаут
but_group.setLayout(h_lay)

# создаем лейауты для расположения на них наших виджетов
line_lay_1 = QHBoxLayout()
line_lay_2 = QHBoxLayout()
line_lay_3 = QHBoxLayout()

# размещаем виджеты на лейаутах
line_lay_1.addWidget(main_question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
line_lay_2.addWidget(but_group)
line_lay_3.addWidget(button, alignment=Qt.AlignCenter)

# создаем главный вертикальный лейаут для всего окна
main_lay = QVBoxLayout()

# расположить на главном лейауте три предыдущих лейаута (лейауты с виджетами)

main_lay.addLayout(line_lay_1, stretch=2)
main_lay.addLayout(line_lay_2, stretch=8)
main_lay.addStretch(1)
main_lay.addLayout(line_lay_3, stretch=1)
main_lay.addStretch(1)

window.setLayout(main_lay)

result = QLabel('Правильно/Неправильно')
correct = QLabel('Тут будет ответ')


answ_lay = QVBoxLayout() # лейаут для группы 

# добавляем текст в группу
answ_lay.addWidget(result, alignment=(Qt.AlignTop | Qt.AlignLeft)) 
answ_lay.addWidget(correct, alignment=Qt.AlignCenter)

answer_group = QGroupBox() # группа для text_1 и text_2

answer_group.setLayout(answ_lay) # устанавливаем лейаут в группу
line_lay_2.addWidget(answer_group) # добавляем весь этот виджет на центральный горизонтальный лейаут (строка - 61)

answer_group.hide() # нам эта панель будет нужна не постоянно

def show_result():
    '''
    показать панель ответов
    '''

    but_group.hide() # – скрывать форму вопроса
    answer_group.show() # – отображать форму правильного ответа
    button.setText('Следующий вопрос') # – менять надпись на кнопке на «Следующий вопрос»

RadioGroup = QButtonGroup() 
RadioGroup.addButton(rad_but_1)
RadioGroup.addButton(rad_but_2)
RadioGroup.addButton(rad_but_3)
RadioGroup.addButton(rad_but_4)


def show_question():
    '''
    показать панель вопросов
    '''

    answer_group.hide() # – скрывать форму ответа
    but_group.show() # – показывать форму вопроса
    button.setText('Ответить') # – менять надпись «Следующий вопрос» на «Ответить»

    # – сбрасывать все переключатели
    RadioGroup.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rad_but_1.setChecked(False)
    rad_but_2.setChecked(False)
    rad_but_3.setChecked(False)
    rad_but_4.setChecked(False)
    RadioGroup.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана


answers = [rad_but_1, rad_but_2, rad_but_3, rad_but_4]

def ask(q): # - передача данных
    '''
    функция записывает значения вопроса и ответов в соответствующие виджеты, 
    при этом варианты ответов распределяются случайным образом
    '''

    shuffle(answers)

    # - расположение вариантов ответов в кнопках-переключателях
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)

    # - изменение текста вопроса
    main_question.setText(q.question)

    # - устанавливает в виджет с правильным овтетом правильный ответ
    correct.setText(q.right_answer)

    # - отображение формы вопроса
    show_question()



def check_answer():
    if answers[0].isChecked():
        '''
        если выбран переключатель answers[0],
        то вызывать функцию show_correct с аргументом «Правильно»
        '''
        window.score += 1

        print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
        print('Рейтинг: ', (window.score/window.total*100), '%')

        show_correct('Правильно')
    else:
        '''
        если выбран любой другой переключатель,
        то вызывать функцию show_correct с аргументом «Неверно»
        '''

        print('Рейтинг: ', (window.score/window.total*100), '%')

        show_correct('Неверно')

def show_correct(res):
    # установление текста-результата в форме ответа
    result.setText(res)

    # отображение формы ответа
    show_result()

# создаем список для вопросов
question_list = []

# создаем несколько вопросов
q1 = Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский')
q2 = Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий')
q3 = Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата')

# добавляем вопросы в список
question_list.append(q1)
question_list.append(q2)
question_list.append(q3)

# создаем функцию next_question()
def next_question():
    ''' задает следующий вопрос из списка '''
    
    window.total += 1

    print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)

    cur_question = randint(0, len(question_list) - 1)

    # взяли вопрос
    q = question_list[cur_question] # [window.cur_question] заменить на [cur_question]
    # спросили
    ask(q)

# создаем функцию click_OK()
def click_OK():
    '''
    определяет, надо ли показывать другой вопрос либо проверить ответ на этот
    '''

    # если кнопка == 'Ответить', то проверяем ответ
    if button.text() == 'Ответить':
        check_answer()
    # если кнопка == 'следующий вопрос', то переходим к следующему вопросу
    else:
        next_question()

# задаем обработку события кнопке
button.clicked.connect(click_OK)

window.score = 0
window.total = 0

next_question()

window.show()
app.exec_()