import numpy as np
import pickle
from django.db import models

class NumpyArrayModel(models.Model):
    image_name = models.TextField()
    base64 = models.TextField()
    array_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)


    def set_array(self, array: np.ndarray):
        """Сериализует и сохраняет массив."""
        self.array_data = pickle.dumps(array)

    def get_array(self) -> np.ndarray:
        """Десериализует и возвращает массив."""
        return pickle.loads(self.array_data)
