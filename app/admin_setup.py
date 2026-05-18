from flask import redirect, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import db
from app.models import Exercise, Goal, ProgramExercise, ProgressLog, TrainingProgram, User, UserProfile


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "is_admin", False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))


class UserAdminView(SecureModelView):
    column_list = ("id", "email", "is_admin", "created_at")
    column_searchable_list = ("email",)
    form_columns = ("email", "is_admin")
    can_delete = True
    can_create = False


class UserProfileAdminView(SecureModelView):
    column_list = ("id", "user", "height_cm", "weight_kg", "age_years", "activity_level", "goal_code")
    column_searchable_list = ("goal", "goal_code")
    form_columns = (
        "user",
        "height_cm",
        "weight_kg",
        "age_years",
        "is_male",
        "activity_level",
        "goal",
        "goal_code",
        "assigned_program",
    )
    column_labels = {
        "user": "Пользователь",
        "height_cm": "Рост (см)",
        "weight_kg": "Вес (кг)",
        "age_years": "Возраст",
        "is_male": "Мужской пол",
        "activity_level": "Активность",
        "goal": "Комментарий цели",
        "goal_code": "Код цели",
        "assigned_program": "Назначенная программа",
    }


class ExerciseAdminView(SecureModelView):
    column_list = ("id", "name", "muscle_group", "equipment", "difficulty")
    column_searchable_list = ("name", "muscle_group", "equipment", "difficulty")
    form_columns = ("name", "description", "muscle_group", "equipment", "difficulty")
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "muscle_group": "Группа мышц",
        "equipment": "Инвентарь",
        "difficulty": "Сложность",
    }


class TrainingProgramAdminView(SecureModelView):
    column_list = ("id", "name", "goal_type", "difficulty", "duration_weeks")
    column_searchable_list = ("name", "goal_type", "difficulty")
    form_columns = ("name", "description", "goal_type", "difficulty", "duration_weeks")
    column_labels = {
        "name": "Название",
        "description": "Описание",
        "goal_type": "Тип цели",
        "difficulty": "Сложность",
        "duration_weeks": "Длительность (нед.)",
    }


class ProgramExerciseAdminView(SecureModelView):
    column_list = ("id", "program", "exercise", "day_number", "order_in_day", "sets", "reps")
    column_searchable_list = ("reps",)
    form_columns = ("program", "exercise", "day_number", "order_in_day", "sets", "reps", "notes")
    column_labels = {
        "program": "Программа",
        "exercise": "Упражнение",
        "day_number": "День",
        "order_in_day": "Порядок",
        "sets": "Подходы",
        "reps": "Повторения",
        "notes": "Заметки",
    }


class GoalAdminView(SecureModelView):
    """Админ-представление для целей по весу/телу."""
    column_list = ("id", "user", "goal_type", "current_value", "target_value", "unit", "deadline")
    column_searchable_list = ("goal_type", "unit")
    form_columns = ("user", "goal_type", "current_value", "target_value", "unit", "deadline", "notes")
    column_labels = {
        "user": "Пользователь",
        "goal_type": "Тип цели",
        "current_value": "Текущее значение",
        "target_value": "Целевое значение",
        "unit": "Единица измерения",
        "deadline": "Срок",
        "notes": "Заметки"
    }
    can_delete = True
    can_create = True


class ProgressLogAdminView(SecureModelView):
    """Админ-представление для логирования прогресса."""
    column_list = ("id", "user", "goal", "log_date", "value", "created_at")
    column_searchable_list = ()
    form_columns = ("user", "goal", "log_date", "value", "notes")
    column_labels = {
        "user": "Пользователь",
        "goal": "Цель",
        "log_date": "Дата логирования",
        "value": "Значение",
        "notes": "Заметки",
        "created_at": "Создано"
    }
    can_delete = True
    can_create = True


def init_admin(app):
    admin = Admin(app, name="Админ-панель", template_mode="bootstrap4", url="/admin")

    admin.add_view(UserAdminView(User, db.session, name="Пользователи", endpoint="admin_users"))
    admin.add_view(
        UserProfileAdminView(UserProfile, db.session, name="Профили", endpoint="admin_profiles")
    )
    admin.add_view(
        ExerciseAdminView(Exercise, db.session, name="Упражнения", endpoint="admin_exercises")
    )
    admin.add_view(
        TrainingProgramAdminView(TrainingProgram, db.session, name="Программы тренировок", endpoint="admin_programs")
    )
    admin.add_view(
        ProgramExerciseAdminView(
            ProgramExercise, db.session, name="Упражнения в программах", endpoint="admin_program_exercises"
        )
    )
    admin.add_view(
        GoalAdminView(Goal, db.session, name="Цели", endpoint="admin_goals")
    )
    admin.add_view(
        ProgressLogAdminView(ProgressLog, db.session, name="Логирование прогресса", endpoint="admin_progress_logs")
    )

