import unittest
from anonymizer import Anonymizer

class TestLocalAnonymizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa la clase y asegura la descarga de modelos si faltan
        cls.anonymizer = Anonymizer(model="es_core_news_lg")

    def test_anonymize_email(self):
        text = "Contactame a juan@example.com para mas detalles."
        result = self.anonymizer.anonymize(text)
        self.assertIn("[EMAIL]", result)
        self.assertNotIn("juan@example.com", result)

    def test_anonymize_phone(self):
        text = "Mi teléfono es +34 600 123 456, llamame pronto."
        result = self.anonymizer.anonymize(text)
        self.assertIn("[TELEFONO]", result)
        self.assertNotIn("+34 600 123 456", result)

    def test_anonymize_person_name(self):
        text = "Carlos Martinez es el nuevo gerente."
        result = self.anonymizer.anonymize(text)
        self.assertIn("[NOMBRE]", result)
        self.assertNotIn("Carlos Martinez", result)

    def test_combined(self):
        text = "El candidato Juan Perez, con email jperez@mail.com y teléfono +34 600 123 456, solicita el puesto."
        result = self.anonymizer.anonymize(text)
        self.assertIn("[NOMBRE]", result)
        self.assertIn("[EMAIL]", result)
        self.assertIn("[TELEFONO]", result)
        self.assertNotIn("Juan Perez", result)
        self.assertNotIn("jperez@mail.com", result)
        self.assertNotIn("+34 600 123 456", result)

if __name__ == "__main__":
    unittest.main()
