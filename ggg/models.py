from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone

# Расширение стандартной модели пользователя
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name="Номер телефона")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название плана")
    duration_days = models.PositiveIntegerField(verbose_name="Продолжительность (дней)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"

    def __str__(self):
        return f"{self.name} ({self.duration_days} дней)"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    membership = models.ForeignKey(
        MembershipPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Абонемент"
    )
    membership_start = models.DateField(null=True, blank=True, verbose_name="Начало действия абонемента")
    membership_end = models.DateField(null=True, blank=True, verbose_name="Окончание действия абонемента")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"Клиент: {self.user.get_full_name() or self.user.username}"


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    specialty = models.CharField(max_length=100, verbose_name="Специализация")
    experience_years = models.PositiveIntegerField(verbose_name="Опыт (лет)")

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return f"Тренер: {self.user.get_full_name() or self.user.username}"


class WorkoutSession(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тренировки")
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, verbose_name="Тренер")
    start_time = models.DateTimeField(verbose_name="Время начала")
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(10)],
        verbose_name="Продолжительность (минут)"
    )
    max_participants = models.PositiveIntegerField(verbose_name="Максимум участников")

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} с {self.trainer} ({self.start_time.strftime('%d.%m.%Y %H:%M')})"


class Attendance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, verbose_name="Тренировка")
    attended = models.BooleanField(default=False, verbose_name="Присутствовал")
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name="Время отметки")

    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"
        unique_together = ('client', 'workout_session')

    def __str__(self):
        return f"{self.client} — {self.workout_session} ({'был' if self.attended else 'не был'})"