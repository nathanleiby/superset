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

if __name__ == '__main__':
    unittest.main()
