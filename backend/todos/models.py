"""Django models for Todo application."""
from django.db import models


class Todo(models.Model):
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "auth.User", related_name="todos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text

    class Meta:
        db_table = "todos_todo"
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
        # ordering = ["-created_at"]
