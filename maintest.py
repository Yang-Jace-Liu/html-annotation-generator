import unittest

import main


class TestGetFileOutputPath(unittest.TestCase):
    def test_success_unix_path(self):
        param = "/home/test/Downloads/test.csv"
        expected = "/home/test/Downloads/test.out.csv"
        self.assertEqual(expected, main.get_file_output_path(param))

    def test_success_windows_path(self):
        param = "C:\\Users\\test\\Downloads\\test.csv"
        expected = "C:\\Users\\test\\Downloads\\test.out.csv"
        self.assertEqual(expected, main.get_file_output_path(param))

    def test_invalid_extension(self):
        param = "C:\\Users\\test\\Downloads\\test"
        with self.assertRaises(ValueError):
            main.get_file_output_path(param)


class TestIsToReplace(unittest.TestCase):
    def test_true_pattern1(self):
        param = "君の名は|(1,kimi)(3,na)"
        self.assertTrue(main.is_to_replace(param))

    def test_true_pattern2(self):
        param = "君の名は|(1-3,kiminona)(4,wa)"
        self.assertTrue(main.is_to_replace(param))

    def test_true_pattern3(self):
        param = "君の名は|(1-3,kiminona)"
        self.assertTrue(main.is_to_replace(param))

    def test_true_pattern4(self):
        param = "君の名は|(12-33,kiminona)"
        self.assertTrue(main.is_to_replace(param))

    def test_false_pattern1(self):
        param = "君の名は|()"
        self.assertFalse(main.is_to_replace(param))

    def test_false_pattern2(self):
        param = "君の名は(1-3,kiminona)(4,wa)"
        self.assertFalse(main.is_to_replace(param))

    def test_false_pattern3(self):
        param = "君の名は|(,kiminona)(4,wa)"
        self.assertFalse(main.is_to_replace(param))

    def test_false_pattern4(self):
        param = "君の名は|"
        self.assertFalse(main.is_to_replace(param))


class TestBuildRuby(unittest.TestCase):
    def test_pattern1(self):
        text = "君"
        annotation = "kimi"
        self.assertEqual("<ruby>君<rt>kimi</rt></ruby>", main.build_ruby(text, annotation))


class TestReplaceText(unittest.TestCase):
    def test_pattern1(self):
        text = "君の名は|(1,kimi)(3,na)"
        expected = "<ruby>君<rt>kimi</rt></ruby>の<ruby>名<rt>na</rt></ruby>は"
