import numpy as np
import pickle
from django.db import models

class Applicant(models.Model):
    applicant_id = models.IntegerField()
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    phone_num = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    attempt = models.PositiveIntegerField()
    status = models.CharField(max_length=50, null=True, blank=True)
    base64 = models.TextField()
    array_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def set_array(self, array: np.ndarray):
        """Сериализует и сохраняет массив."""
        self.array_data = pickle.dumps(array)

    def get_array(self) -> np.ndarray:
        """Десериализует и возвращает массив."""
        return pickle.loads(self.array_data) if self.array_data else None

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_surname(self):
        return self.surname

    def set_surname(self, value):
        self.surname = value

    def get_phone_num(self):
        return self.phone_num

    def set_phone_num(self, value):
        self.phone_num = value

    def get_school(self):
        return self.school

    def set_school(self, value):
        self.school = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_best_result(self):
        return self.best_result

    def set_best_result(self, value):
        self.best_result = value


class BlackList(models.Model):
    applicant_id = models.IntegerField()
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    phone_num = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    base64 = models.TextField()
    array_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)


    def set_array(self, array: np.ndarray):
        """Сериализует и сохраняет массив."""
        self.array_data = pickle.dumps(array)

    def get_array(self) -> np.ndarray:
        """Десериализует и возвращает массив."""
        return pickle.loads(self.array_data)

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_surname(self):
        return self.surname

    def set_surname(self, value):
        self.surname = value

    def get_phone_num(self):
        return self.phone_num

    def set_phone_num(self, value):
        self.phone_num = value

    def get_school(self):
        return self.school

    def set_school(self, value):
        self.school = value

class Error(models.Model):
    applicant_id = models.IntegerField()
    base64 = models.TextField()
    array_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=256)

    def set_array(self, array: np.ndarray):
        """Сериализует и сохраняет массив."""
        self.array_data = pickle.dumps(array)

    def get_array(self) -> np.ndarray:
        """Десериализует и возвращает массив."""
        return pickle.loads(self.array_data)
