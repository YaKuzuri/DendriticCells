from django.db import models

# Create your models here.
class Patient(models.Model):
    SEX_CHOISES = {
        1: 'Мужской',
        2: 'Женский'
    }

    CURE_ORDER = {
        1: 'Первичный пациент',
        2: 'Вторичный пациент'
    }

    PRRECID = {
        1: 'Рецидив',
        2: 'Регионарные метастазы',
        3: 'Отдаленные метастазы',
        4: 'Биохимический рецидив',
        5: 'Прогрессирование процесса',
        6: 'Местнораспространенный процесс',
        7: 'Трансформация',
    }

    STATENDYR = {
        1: 'Жив',
        2: 'Умер от осложнения лечения',
        3: 'Умер от основного заболевания',
        4: 'Умер от других заболеваний',
        5: 'Выехал',
        7: 'Диагноз не подтвердился',
        8: 'Снят с учета в связи с истечением срока наблюдения'
    }

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['fio']

    fio = models.CharField(max_length=100, null=True, blank=True, verbose_name='ФИО')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    sex = models.SmallIntegerField(choices=SEX_CHOISES, null=True, blank=True, verbose_name='Пол')
    cure_order = models.SmallIntegerField(choices=CURE_ORDER, null=True, blank=True, verbose_name='Первичный/вторичный')

    last_modified = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')
    actual_date = models.DateTimeField(null=True, blank=True, verbose_name='Вся информация о пациенте актуальна на: (дата)')

    last_contact_date = models.DateField(null=True, blank=True, verbose_name='Дата последнего контакта/смерти')
    statendyr = models.SmallIntegerField(choices=STATENDYR, null=True, blank=True, verbose_name='Состояние на данный момент')

    prrecid = models.SmallIntegerField(choices=PRRECID, null=True, blank=True, verbose_name='Возникший процесс')
    prrecid_date = models.DateField(null=True, blank=True, verbose_name='Дата возникновения процесса')

    datediag = models.DateField(null=True, blank=True, verbose_name='Дата возникновения процесса')
    mkb10 = models.CharField(max_length=20, null=True, blank=True, verbose_name='МКБ-10')
    txtdiag = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Диагноз текстом')
    stage = models.SmallIntegerField(null=True, blank=True, verbose_name='Стадия')
    t = models.SmallIntegerField(null=True, blank=True, verbose_name='T')
    n = models.SmallIntegerField(null=True, blank=True, verbose_name='N')
    m = models.SmallIntegerField(null=True, blank=True, verbose_name='M')
    g = models.SmallIntegerField(null=True, blank=True, verbose_name='G')
    p16 = models.SmallIntegerField(null=True, blank=True, verbose_name='p16')
    focus_size = models.FloatField(null=True, blank=True, verbose_name='Размер первичного очага, см')
    node_size = models.FloatField(null=True, blank=True, verbose_name='Размер л/у, см')

    note_txt = models.CharField(max_length=200, null=True, blank=True, verbose_name='Текстовая пометка')

    oper_date = models.DateField(null=True, blank=True, verbose_name='Дата операции')
    oper_txt = models.CharField(max_length=400, null=True, blank=True, verbose_name='Операция текстом')
    oper_complications = models.CharField(max_length=200, null=True, blank=True, verbose_name='Послеоперационные осложнения, текстом')

    dendritic = models.BooleanField(null=True, blank=True, verbose_name='Введение дендритных клеток')

    kindlech_txt = models.CharField(max_length=200, null=True, blank=True, verbose_name='Вид специального лечения')

    fk_after = models.CharField(max_length=200, null=True, blank=True, verbose_name='ФК после')
    fk_last = models.CharField(max_length=200, null=True, blank=True, verbose_name='ФК последнее')

    neut = models.FloatField(null=True, blank=True, verbose_name='Нейтрофилы')
    limph = models.FloatField(null=True, blank=True, verbose_name='Лимфоциты')
    plt = models.FloatField(null=True, blank=True, verbose_name='Тромбоциты')



