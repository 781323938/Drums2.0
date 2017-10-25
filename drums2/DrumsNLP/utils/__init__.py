import regex as re
def getPubmedIDFromURL(url):
    #http://www.ncbi.nlm.nih.gov/pubmed/17986308?itool=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_RVDocSum&ordinalpos=2
    rlt = re.search('www.ncbi.nlm.nih.gov/pubmed/(\d+)', url)
    if rlt:
        return rlt.group(1)
    else:
        return None