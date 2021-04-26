from django.db import models

from project.settings import TEXT_LENGTH_CONSTRAINT


class Polls(models.Model):
    name = models.CharField(max_length=108, verbose_name='Название опроса')
    description = models.TextField(verbose_name='Описание опроса')
    start_time = models.DateTimeField(verbose_name='Дата и время начала опроса')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания опроса')

    def __str__(self):
        return f'[{self.name}] polls'


class Question(models.Model):
    ARBITRARY = 'AR'
    SINGLE_CHOICE = 'SC'
    MULTIPLE_CHOICE = 'MC'

    QUESTION_TYPE = [
        ('AR', 'Arbitrary answer'),
        ('SC', 'Choosing one answer from a set of variants'),
        ('MC', 'Choosing one or more answers from a set of variants'),
    ]

    polls = models.ForeignKey(
        Polls,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Опрос, к которому принадлежит вопрос'
    )
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE,
        verbose_name='Тип вопроса'
    )
    text = models.TextField(verbose_name='Текст вопроса')

    def __str__(self):
        return f'[{self.text[:TEXT_LENGTH_CONSTRAINT]}...] question'


class BaseAnswerForm(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='base_forms',
        verbose_name='Базовый шаблон ответа на вопрос'
    )

    def __str__(self):
        return f'[{self.pk}] base answer form for question: [{self.question}]'


class TextAnswerForm(models.Model):
    base_form = models.OneToOneField(
        BaseAnswerForm,
        on_delete=models.CASCADE,
        related_name='text_answers',
        verbose_name='Ответы опрашиваемых на вопрос открытого типа'
    )
    respondent = models.ForeignKey(
        Respondent,
        on_delete=models.CASCADE,
        related_name='text_answer',
        verbose_name='Ответ на вопрос открытого типа'
    )
    text = models.TextField(verbose_name='Развернутый ответ опрашиваемого')

    def __str__(self):
        return f'The answer of [{self.respondent} to the question: [{self.base_form.question}]'


class ChoiceAnswerForm(models.Model):
    base_form = models.OneToOneField(
        BaseAnswerForm,
        on_delete=models.CASCADE,
        related_name='choice_answer',
        verbose_name='Ответы опрашиваемых на вопрос выборного типа'
    )
    respondent = models.ManyToManyField(
        Respondent,
        related_name='choice_answers',
        verbose_name='Уникальные пользователи, которые выбрали этот вариант ответа на вопрос'
    )
    choice_text = models.TextField(verbose_name='Текстовое представление варианта ответа')

    def __str__(self):
        return f'The choice answer [{self.choice_text[:TEXT_LENGTH_CONSTRAINT]}] ' \
               f'for the question [{self.base_form.question}]'


class Respondent(models.Model):
    identity = models.BigIntegerField(
        unique=True,
        default=-1,
        verbose_name='ID уникального пользователя, "-1" обозначает анонимного пользователя'
    )

    def __str__(self):
        return f'The respondent with id {self.identity}'
