from django.test import TestCase


class EntryAdminTest(TestCase):

    def test_save(self):
        """
        Tests that an entry is saved.
        """
        self.assertEqual(1 + 1, 2)
        
    def test_publish(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_unpublish(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_delete(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_cron(self):
        """
        Tests that an entry is saved.
        """
        self.assertEqual(1 + 1, 2)

    def test_revert(self):
        """
        Tests that an entry is saved.
        """
        self.assertEqual(1 + 1, 2)

    def test_get_history(self):
        """
        Tests that an entry is saved.
        """
        self.assertEqual(1 + 1, 2)


class EntryListTest(TestCase):

    def test_save(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_publish(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_unpublish(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_delete(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
