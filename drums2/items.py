# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Drums2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class MiniVarInfo(scrapy.Item):
    # define the fields for your item here like:
    drums_db_uid = scrapy.Field()
    #0. drums_lsdb_id
    #1. source_id/ dbid
    #2. genome_source
    #3. genome_hgvs
    #4. transcript_source
    #5. transcript_hgvs
    #6. protein_source
    #7. protein_hgvs
    #8. citation_source
    #9. pmid_info / publication/ reference
    ###[pmid|]
    reference_info = scrapy.Field({})
    #10. HGNC gene Symbol
    #11. Sharing policy 
    #12 User permission 
    #13 Exon
    #14 DNA remark: further information for genotype that could not classify to other fields.
   #15  template(s) used to detect the sequence variant; DNA = genomic DNA, RNA = RNA (cDNA), RNA+DNA = select both DNA and RNA
    #need extract such information from full text   
    #16 Technique = technique(s) used to identify the sequence variants    
    #17 RNA
    #18 alternative reports. Should be a list. could dynamically generated.
    #19 Frequency set 'na' always. seems not useful    
    #20 field origin of variant allele, e.g. sporadic (no affected relatives besides brother/sister), de novo, familial
    #21 restriction enzyme recognition site created (+) or destroyed (-); e.g. BglII+, BamHI-
    #tool could analysis    
    #22 Allele: refer to annother mutation.Always available???
   #variant-23 pathogencity: refers to the ability of an organism to cause disease
    #pathogenicity, in the format Reported/Concluded; '+' indicating the variant is pathogenic, '+?' probably pathogenic, '-' no known pathogenicity, '-?' probably no pathogenicity, '?' effect unknown.
    #The World Health Organization classifies G6PD genetic variants into five classes, the first three of which are deficiency states.
    #Ref: http://en.wikipedia.org/wiki/Glucose-6-phosphate_dehydrogenase_deficiency
 
 
    
