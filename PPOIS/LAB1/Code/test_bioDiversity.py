import unittest
from unittest.mock import patch
from io import StringIO
from bioDiversity import BioDiversity


class TestBioDiversity(unittest.TestCase):
    def setUp(self):
        self.biodiversity = BioDiversity()

    def test_initial_state(self):
        """Тестирование начального состояния"""
        self.assertEqual(self.biodiversity.numberOfPlantsVariety, [])
        self.assertEqual(self.biodiversity.numberOfAnimalsVariety, [])

    def test_add_new_plant_variety(self):
        """Тестирование добавления нового вида растения"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.biodiversity.addPlantVariety("Oak")
            self.assertIn("Oak", self.biodiversity.numberOfPlantsVariety)
            self.assertIn("Added new plant variety: Oak", fake_out.getvalue())

    def test_add_duplicate_plant_variety(self):
        """Тестирование добавления дубликата растения"""
        self.biodiversity.addPlantVariety("Pine")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.biodiversity.addPlantVariety("Pine")
            self.assertEqual(self.biodiversity.numberOfPlantsVariety.count("Pine"), 1)
            self.assertIn("already exists", fake_out.getvalue())

    def test_add_new_animal_variety(self):
        """Тестирование добавления нового вида животного"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.biodiversity.addAnimalVariety("Lion")
            self.assertIn("Lion", self.biodiversity.numberOfAnimalsVariety)
            self.assertIn("Added new animal variety: Lion", fake_out.getvalue())

    def test_add_duplicate_animal_variety(self):
        """Тестирование добавления дубликата животного"""
        self.biodiversity.addAnimalVariety("Tiger")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.biodiversity.addAnimalVariety("Tiger")
            self.assertEqual(self.biodiversity.numberOfAnimalsVariety.count("Tiger"), 1)
            self.assertIn("already exists", fake_out.getvalue())

    def test_show_info_empty(self):
        """Тестирование отображения информации при пустых списках"""
        expected_output = """
=== Biodiversity Information ===
Total plant varieties: 0
Total animal varieties: 0
Plant varieties: No plant varieties added.
Animal varieties: No animal varieties added.
===============================
""".strip()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.biodiversity.showInfo()
            self.assertEqual(fake_out.getvalue().strip(), expected_output)

    def test_show_info_with_data(self):
        """Тестирование отображения информации с данными"""
        self.biodiversity.addPlantVariety("Oak")
        self.biodiversity.addPlantVariety