#drums_536
'''
    2010/11/21
    Employed gb2tab.py to extract CDS sequence from the genbank file of rna transcript. Among 99 unique position, three sequence with 
    97 position mapped.
'''
from datetime import date

from tempfile import NamedTemporaryFile
import urllib

import os, sys, urllib2, re, copy, subprocess
from BeautifulSoup import BeautifulSoup
sys.path.append('/home/zuofeng/projects/toc/ppMap')
from ppMapDB import ppMapMySQL
pp = ppMapMySQL('bminfo')

#sys.path.append('')
gb2tab_exe_path = '/home/zuofeng/biotools/sequences/gb2tab-1.2.1/gb2tab.py'

import xmlrpclib
s = xmlrpclib.Server('http://129.89.57.69:9681/')


hexentityMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
hexentityMassage = [(re.compile('&#x([^;]+);'), 
       lambda m: '&#%d' % int(m.group(1), 16))]

def convertHtmlEntities2Unicode(html):
    if not html:
        return 'na'
    return BeautifulSoup(html,
                convertEntities=BeautifulSoup.HTML_ENTITIES,
                markupMassage=hexentityMassage).contents[0].string


###########stndard operation##########################################################
def getSourceCode(url):
    html_src_folder = date.today().strftime("/home/zuofeng/data/mutation/lsdbs/%Y%m%d")
    latestFolder = "/home/zuofeng/data/mutation/lsdbs/latest"
    if not os.path.isdir(html_src_folder):
        os.mkdir(html_src_folder)
    page = urllib2.urlopen(drums_url)
    htmlsrc = page.read()
    lines = htmlsrc.split('\n')
    #decide wheterh the server works well.
    if len(lines) > 20:
        saveSrcTo = html_src_folder + '/drums' + drums_lsdb_id + '.html'
        open(saveSrcTo, 'w').write(htmlsrc)
    else: 
        htmlsrc = open(latestFolder + '/drums' + drums_lsdb_id + '.html', 'r')
    return htmlsrc
############################above is standard###############################################################

##################input##############
drums_lsdb_id = '536'
drums_url = 'http://www.bioinf.org.uk/cgi-bin/AndrewMartin/g6pd/g6pd.perl?selname=1&selclass=1&seldna=1&selaa=1&selref=1&selss=1&selcons=1&selif=1&class=All&mode=resnum&resnum=&resnam=Any&mutname=&mutnamematch=exact&refs='
mim_id = '305900'

#options
#add known reference sequence
ref_dna_ids = ['NM_001042351.1']
#################end of input###############


    
htmlsrc = getSourceCode(drums_url)
#htmlsrc = convertHtmlEntities2Unicode(htmlsrc)
variants = {}
##################end of standar operation###################################
##################################
###########################################
######################################################
#http://www.hgvs.org/mutnomen/recs-prot.html
#minimum information
#LSDB minimal requirements (D3.4)
#http://www.gen2phen.org/post/lsdb-minimal-requirements-d34-compared-lovd-and-lsdb-xml-format
#this function should be customerized for each lsdb database.
def getDrumsEntry(dbid, var):
    '''
        var is unique mutation in a certain lsdb database.
    '''
    variant_fields = []
    #0. drums_lsdb_id
    variant_fields.append('536')
    #1. source_id/ dbid
    variant_fields.append(urllib.quote(dbid))
    #2. genome_source
    variant_fields.append('na')
    #3. genome_hgvs
    variant_fields.append('na')
    #4. transcript_source
    variant_fields.append(var.get('nucleotide') + ' ' + var.get('nucsubs'))
    #5. transcript_hgvs
    p = re.compile('([ATCG])-->([ATCG])')
    rlt = p.search(var.get('nucsubs'))
    cInfo = ''
    if rlt:
        cInfo = 'c.' + var.get('nucleotide') + rlt.group(1) + '>' +rlt.group(2)
    else:
        cInfo = 'not single point mutation'
    variant_fields.append(cInfo)
    #6. protein_source
    variant_fields.append(var.get('aminoacid') + ' ' + var.get('resnum') + ' ' + var.get('substitution'))
    #7. protein_hgvs
    variant_fields.append('p.' + var.get('aminoacid').title() + var.get('resnum') + var.get('substitution').title())
    #8. citation_source
    variant_fields.append(var.get('citation'))
    #9. pmid_info / publication/ reference
    lp = re.compile('(.*?)\\s+(\\d+)\\s*:\\s*(\\d+)-?(\\d+)?,?\\s*(\\d+)')
    rlt = lp.search(var.get('citation'))
    lInfo = 'need curation'
    if rlt:
        #try to get pmid
        url = 'http://www.ncbi.nlm.nih.gov/pubmed?term=' + rlt.group(1).replace(' ', '+') + '[Jour]'
        url += '+AND+' + rlt.group(2) + '[volume]+AND+'
        url += rlt.group(3) + '[page]+AND+' 
        url += rlt.group(5) + '[pdat]&cmd=detailssearch'
        lInfo = url
    variant_fields.append(lInfo)
    
    #10. HGNC gene Symbol
    variant_fields.append('G6PD')
    #11. Sharing policy 
    variant_fields.append('public')
    #12 User permission 
    variant_fields.append('na')
    #13 Exon
    variant_fields.append('na')
    #14 DNA remark: further information for genotype that could not classify to other fields.
    dna_remark = 'Secondary structure: ' + var.get('ss')
    dna_remark += 'Conservation: ' + var.get('cons')
    dna_remark += 'Location in interface? ' + var.get('interface')
    variant_fields.append(dna_remark)
    #15  template(s) used to detect the sequence variant; DNA = genomic DNA, RNA = RNA (cDNA), RNA+DNA = select both DNA and RNA
    #need extract such information from full text
    variant_fields.append('na')
    
    #16 Technique = technique(s) used to identify the sequence variants
    variant_fields.append('na')
    
    #17 RNA
    variant_fields.append('na')
    #18 alternative reports. Should be a list. could dynamically generated.
    variant_fields.append('na')
    
    #19 Frequency set 'na' always. seems not useful
    variant_fields.append('na')
    
    #20 field origin of variant allele, e.g. sporadic (no affected relatives besides brother/sister), de novo, familial
    variant_fields.append('na')
    
    #21 restriction enzyme recognition site created (+) or destroyed (-); e.g. BglII+, BamHI-
    #tool could analysis
    variant_fields.append('na')
    
    #22 Allele: refer to annother mutation.Always available???
    variant_fields.append('na')
    
    #variant-23 pathogencity: refers to the ability of an organism to cause disease
    #pathogenicity, in the format Reported/Concluded; '+' indicating the variant is pathogenic, '+?' probably pathogenic, '-' no known pathogenicity, '-?' probably no pathogenicity, '?' effect unknown.
    #The World Health Organization classifies G6PD genetic variants into five classes, the first three of which are deficiency states.
    #Ref: http://en.wikipedia.org/wiki/Glucose-6-phosphate_dehydrogenase_deficiency
    var_class = int(var.get('class'))
    if var_class <=3:
        variant_fields.append('+')
    else:
        variant_fields.append('-')  
    
    patient_fields = []
    #1. patient id
    patient_fields.append('na')
    #2. phenotype /disease
    patient_fields.append('D55.0')
    #3. phenotype remark, further information for the phenotype that could not classify to other fields.
    pheno_remark = 'g6pd variant name: ' + var.get('name')
    
    patient_fields.append(pheno_remark)
    
    #4. patient Origin/Geographic
    patient_fields.append('na')
    
    #5. Patient/Origin/Ethnic
    patient_fields.append('na')
    
    #6. Patient/Gender
    patient_fields.append('na')
    
    #7. ID_submitterid: submitter or the script used modify the data
    patient_fields.append('drums536.py')
    
    
    fields = variant_fields + patient_fields
    
    #variant-24 genome-reference
    fields.append('na')
    #variant-25 transcript reference
    fields.append('na')
    #protein-26 PROTEIN reference
    fields.append('na')
    #rna-27 RNA reference
    fields.append('na')
    
    
    
    #variant data status
    fields.append('init')
    return fields 

soup = BeautifulSoup(htmlsrc)
table = soup.table.extract()
trs = table.findAll(['tr'])
ths = trs[0].findAll(['th'])
if not ths:
    print 'something wrong 1'
    sys.exit()    

heads = []
for th in ths:
    heads.append(th.getText())
#point_mutations = []


for dbid in range(1, len(trs)):
    tr = trs[dbid]
    tds = tr.findAll(['td'])
    if len(tds) < 1:
        print 'something wrong 2'
        sys.exit(1)
    variance = {}
    for j in range(0, len(tds)):
        variance[heads[j]] = convertHtmlEntities2Unicode(tds[j].getText())
    
    dbid = str(tds)#use original string as unique id
    
    fields = getDrumsEntry(dbid, variance)
    variants[dbid] = fields

######################################################################################################
###The following is standar operation
#####################################
def three2single(thr):
    thr = thr.upper()
    if len(thr) == 1:
        return thr
        
    if thr == "PHE":
        return "F"
    elif  thr == "LEU":
        return "L"
    elif  thr == "ILE":
        return "I"
    elif  thr == "MET":
        return "M"
    elif  thr == "VAL":
        return "V"
    elif  thr == "SER":
        return "S"
    elif  thr == "PRO":
        return "P"
    elif  thr == "THR":
        return "T"
    elif  thr == "ALA":
        return "A"
    elif  thr == "TRP":
        return "W"
    elif  thr == "TYR":
        return "Y"
    elif  thr == "HIS":
        return "H"#Bug:G->H 200905141902
    elif  thr == "ASN":
        return "N"
    elif  thr == "LYS":
        return "K"
    elif  thr == "ASP":
        return "D"
    elif  thr == "GLU":
        return "E"
    elif  thr == "CYS":
        return "C"
    elif  thr == "GLN":#BUG:miss gln 200905180424
        return "Q"
    elif  thr == "ARG":
        return "R"
    elif  thr == "GLY":
        return "G"
    else:
         return "X"

hgvs_pm_dna = re.compile('c\\.(\\d+)([ACTG])>([ACTG])')
hgvs_pm_prn = re.compile('p\\.(.*?)(\\d+)(.*?)')

pms_rna = {}
pms_prn = {}
pms_positions_prn = []
for id in variants.keys():
    fields = variants[id]
    print fields[5] + '\t' + fields[7]
    #####################
    rlt = hgvs_pm_dna.search(fields[5])
    if rlt:
        pos = rlt.group(1)
        if not pms_rna.has_key(pos):
            pms_rna[pos] = rlt.group(2)
            continue
        if pms_rna.get(pos) == rlt.group(2):
            pass
        else:
            print 'conflict'
    #######################
    rlt = hgvs_pm_prn.search(fields[7])
    if rlt:
        pos = rlt.group(2)
        if not pms_prn.has_key(pos):
            pms_prn[pos] = rlt.group(1)
            pms_positions_prn.append(int(pos))
            continue
        if pms_prn.get(pos) == rlt.group(1):
            pass
        else:
            print 'conflict'
    
    #point_mutations.append(fields[7])

sql = 'select gene_id from MIM2GENE where type = "gene" and mim_number="' + mim_id + '"'
genes = pp.execute(sql)
gene_id = genes[0][0]

sql = 'select protein, rna from accession2geneid where geneid="' + gene_id + '"'
protein_rna_pairs = pp.execute(sql)



def checkVersions(ncbi_id):
    p_ncbi = re.compile('(.*)\\.(\\d+)')
    rlt = p_ncbi.search(ncbi_id)
    versionList = []
    if rlt:
        version = int(rlt.group(2))
        if version == 1:
            versionList.append(ncbi_id)
        else:
            for i in range(1,version +1):
                versionList.append(rlt.group(1) + '.' + str(i))
    else:
        print 'something wrong'
        sys.exit(3)    
    return versionList
    
protein_list = []
rna_list = []
for pair in protein_rna_pairs:
    protein_id = pair[0]
    rna_id = pair[1]
    rna_list +=checkVersions(rna_id)
    protein_list += checkVersions(protein_id)

print protein_list
print rna_list

#add known reference sequence
rna_list += ref_dna_ids

seqs_prn = {}
seqs_dna = {}

from Bio import SeqIO
'''
    genbank: gb
'''
def getCDSSeqs(type, ncbi_id_list, format = 'gb'):
    eutil_protein = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&complexity=1&rettype=' + format + '&id='
    eutil_rna = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&complexity=1&rettype=' + format + '&id='

    seqs = {}
    url = ''
    if type == 'protein':
        url = eutil_protein
    else:
        url = eutil_rna
    print url    
    for id in ncbi_id_list:
        link = url + id
        page = urllib2.urlopen(link)
        gb_seq = page.read()
        fin = NamedTemporaryFile(delete = False)
        fin.write(gb_seq)
        tmpFileName =fin.name
        fin.close()
    
        gb2tab_cmd = ['python',gb2tab_exe_path, tmpFileName]
        __p__ = subprocess.Popen(gb2tab_cmd, stdout=subprocess.PIPE)
        rltLines = __p__.stdout.readlines()
        
        '''
            The extracted sequences are streamed to STDOUT with one 
            entry per line in the following format (tab separated):
            name	seq	ann	com
        '''
        seqs[id] = rltLines[0].split('\t')[1]
    return seqs
    
    
'''
    fasta: fasta

'''
def getFastaSeqs(type, ncbi_id_list, format = 'fasta'):
    eutil_protein = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&complexity=1&rettype=' + format + '&id='
    eutil_rna = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&complexity=1&rettype=' + format + '&id='

    seqs = {}
    url = ''
    if type == 'protein':
        url = eutil_protein
    else:
        url = eutil_rna
    print url    
    for id in ncbi_id_list:
        link = url + id
        page = urllib2.urlopen(link)
        seqs[id] = SeqIO.parse(page, format).next()
    return seqs
    
seqs_prn =  getFastaSeqs('protein', protein_list)
seqs_dna = getFastaSeqs('dna', rna_list)
seqs_cds = getCDSSeqs('dna', rna_list)


for p in protein_list:
    print seqs_prn[p].id
    print seqs_prn[p].seq
    
print rna_list
print seqs_dna

print 'reference consistency analysis (RSCA)'
print 'RSCA-1: direct matching-DNA'
print pms_rna
for id in rna_list:
    matchRlt =[]
    count = 0
    for pos in pms_rna.keys():
        ipos = int(pos) - 1
        if seqs_dna[id].seq[ipos] == pms_rna[pos]:
            matchRlt.append('1')
            count += 1
        else:
            matchRlt.append('0')
    print id + '\t' + str(count) + '/' + str(len(pms_rna.keys())) + '\t' + ' '.join(matchRlt)
    
print 'RSCA-1: direct matching-CDS'
for id in rna_list:
    matchRlt =[]
    count = 0
    for pos in pms_rna.keys():
        ipos = int(pos) - 1
        if seqs_cds[id][ipos] == pms_rna[pos]:
            matchRlt.append('1')
            count += 1
        else:
            matchRlt.append('0')
    print id + '\t' + str(count) + '/' + str(len(pms_rna.keys())) + '\t' + ' '.join(matchRlt)

print 'RSCA-1: direct matching-Protein'
'''
    In this case, through direct matching, we 
'''

for id in protein_list:
    matchRlt =[]
    count = 0
    for pos in pms_prn.keys():
        ipos = int(pos) - 1
        aa = three2single(pms_prn[pos])
        print pos + '\t' + pms_prn[pos] + '\t' + aa + '\t' + str(ipos) + '\t' + seqs_prn[id].seq[ipos-1] + seqs_prn[id].seq[ipos] + seqs_prn[id].seq[ipos+1] + '\t',
        if seqs_prn[id].seq[ipos] == aa:
            matchRlt.append('1')
            count += 1
            print '+'
        else:
            matchRlt.append('0')
            print '-'
    print id + '\t' + str(count) + '/' + str(len(pms_prn.keys())) + '\t' + ' '.join(matchRlt)
pms_positions_prn = sorted(pms_positions_prn)
start = pms_positions_prn[0]
end = pms_positions_prn[-1]



print 'RSCA-2: signalp offset protein'

from tempfile import NamedTemporaryFile
import subprocess
THIRD_PART_TOOLS_FOLDER = '/home/zuofeng/projects/platform/bminfo/bminfo/tools'

def signalp(protein_fasta):
    f = NamedTemporaryFile(delete=False)
    f.write(protein_fasta)
    tmpFileName = f.name
    f.close()
    
    signalp3_exe = THIRD_PART_TOOLS_FOLDER + '/signalp-3.0/signalp'
    signalp_cmd = [signalp3_exe,'-t', 'euk', tmpFileName]
    
    __p__ = subprocess.Popen(signalp_cmd, stdout=subprocess.PIPE)
    content = ''.join(__p__.stdout.readlines())
    print content;
    '''
        >P10643.0
        Prediction: Signal peptide
        Signal peptide probability: 0.990
        Signal anchor probability: 0.000
        Max cleavage site probability: 0.623 between pos. 22 and 23
    '''
    sp = {}
    sp['version'] = 3.0
    prob = re.compile('Signal peptide probability: (.*)')
    site = re.compile('Max cleavage site probability: (.*) between pos. (.*) and (.*)')
    rlt = prob.search(content)
    if rlt:
        sp['sp_prob'] = float(rlt.group(1))
    rlt2 = site.search(content)
    if rlt2:
        sp['site_prob'] = float(rlt2.group(1))
        sp['site_left'] = int(rlt2.group(2))
        sp['site_right'] = int(rlt2.group(3))
    return sp

for id in protein_list:
    matchRlt =[]
    count = 0
    
    protein = seqs_prn[id]
    
    protein_fasta = '>' + id + '\n' + str(protein.seq)
    print protein_fasta
    
    #sp = s.sequence.signalp(protein_fasta)
    sp = signalp(protein_fasta)
     
    print sp
    if sp['sp_prob'] >= 0.85 and sp('site_left') > 0:
        sp_offset = sp('site_left')
        for pos in pms_prn.keys():
            ipos = int(pos) + sp_offset - 1 
            aa = three2single(pms_prn[pos])
            print pos + '\t' + pms_prn[pos] + '\t' + aa + '\t' + str(ipos) + '\t' + seqs_prn[id].seq[ipos-1] + seqs_prn[id].seq[ipos] + seqs_prn[id].seq[ipos+1]
            if seqs_prn[id].seq[ipos] == aa:
                matchRlt.append('1')
                count += 1
            else:
                matchRlt.append('0')
        print id + '\t' + str(count) + '/' + str(len(pms_prn.keys())) + '\t' + ' '.join(matchRlt)
    else:
        print 'Signalp offset does not applicable'


print 'RSCA-X: signalp offset protein'
pms_positions_prn = sorted(pms_positions_prn)
start = pms_positions_prn[0]
end = pms_positions_prn[-1]
newSeq = ''
for pos in range(start, end+1):
    if pos in pms_positions_prn:
        sPos = str(pos)
        newSeq += three2single(pms_prn[sPos])
    else:
        newSeq += '-'
print newSeq
print pms_positions_prn

#final results
 

date_stamp = date.today().strftime("%Y-%m-%d")
sql_insert_root = 'INSERT INTO GENOTYPE_PHENOTYPE (drum_lsdb_id ,dbid ,genome_source ,genome_hgvs ,transcript_source ,transcript_hgvs ,protein_source ,protein_hgvs ,citation_source ,pmid_info ,hgnc_gene_Symbol ,sharing_policy ,user_permission ,exon_index ,genotype_remark ,detection_template ,detection_technique ,rna_hgvs ,alternatives ,frequency ,origin_of_variant_allele ,restr_enzyme_recogn_site ,allele ,pathogencity ,patient_id ,phenotype_or_disease ,phenotype_remark ,    patient_geographic_origin ,patient_ethnic_origin ,gender ,submitter_id ,  genome_ref , transcript_ref,protein_ref,rna_ref ,data_status ,date_stamp) VALUES("'

for dbid in variants.keys():
    v = variants[dbid]
    sql_check = 'SELECT * from GENOTYPE_PHENOTYPE WHERE dbid="' + v[1] + '"'''
    lines = pp.execute(sql_check)
    if lines:
        continue

    #print len(v)
    nor_v = []
    for field in v:
        nor_v.append(field.replace('"', '\''))
    
    sql_insert = sql_insert_root + '","'.join(nor_v).encode('utf-8') + '"'
    sql_insert += ',"' + date_stamp + '")'
    pp.insert(sql_insert)



    