import unittest
import os

import vision

class TestVision(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_game(self):
        """ Verify vision can extract multiple cards out of full game view """
        dirname='./images/game/'
        games = [
            {
                'image': 'game001.jpg',
                'num_cards': 12,
            },
            {
                'image': 'game002.jpg',
                'num_cards': 5,
            },
            {
                'image': 'game003.jpg',
                'num_cards': 12,
            }
        ]
        for g in games:
            print("TEST: Checking number of cards for {}".format(g))
            imgpath= os.path.join(dirname, g['image'])
            cards = vision.findCards(imgpath)
            self.assertEqual(len(cards), g['num_cards'])

    def test_single_card(self):
        """ Verify vision can analyze a single card """
        dirname='./images/single-card/'
        errors = ["foo",]
        total = 0
        for filename in os.listdir(dirname):
          if not filename.endswith('.png'):
            continue
          fullpath = os.path.join(dirname, filename)
          expected = vision.determine_expected(filename)
          actual = vision.analyze(fullpath, expected)
          if expected != actual:
            errors.append(filename)

          # self.assertDictEqual(actual, expected)

        if len(errors) > 0:
          self.assertTrue(len(errors) == 0, "Errors: {}".format(errors))



if __name__ == '__main__':
    unittest.main()
