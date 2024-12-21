import unittest
from LR8 import *
from unittest.mock import patch, MagicMock

class TestClientFunction(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_client_success(self, mock_popen):
        # Налаштування мок-об'єкта
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Test output", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        # Виклик функції
        output, error = client("127.0.0.1")

        # Перевірка результатів
        self.assertEqual(output, "Test output")
        self.assertEqual(error, "")
        mock_popen.assert_called_once_with(
            ["iperf", "-c", "127.0.0.1", "-i", "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    @patch('subprocess.Popen')
    def test_client_failure(self, mock_popen):
        # Налаштування мок-об'єкта для помилки
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("", "Error occurred")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        # Виклик функції
        output, error = client("192.168.1.1")

        # Перевірка результатів
        self.assertEqual(output, "")
        self.assertEqual(error, "Error occurred")

if __name__ == '__main__':
    unittest.main()
