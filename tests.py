#encoding:utf-8
import unittest
from drums2.DrumsNLP import utils as drumsUtils
class DrumsNLP(unittest.TestCase):
    def test_getPubmedIDFromURL(self):
        url = 'http://www.ncbi.nlm.nih.gov/pubmed/17986308?itool=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_RVDocSum&ordinalpos=2'
        pmid = drumsUtils.getPubmedIDFromURL(url)
        self.assertEqual(pmid, '17986308' )

if __name__ == '__main__':
    unittest.main()