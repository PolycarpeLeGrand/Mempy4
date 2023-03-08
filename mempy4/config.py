from pathlib import Path
from os import listdir

BASE_DATA_PATH = Path('C:/Users/Sanchez/Desktop/m4data/')
TEMP_DATA_PATH = Path('D:/m4temp')
ANALYSIS_PATH = BASE_DATA_PATH / 'analysis'
RESULTS_PATH = BASE_DATA_PATH / 'results'
CSV_PATH = BASE_DATA_PATH / 'csv_mappings'
MEMVIZ_DATA_PATH = BASE_DATA_PATH / 'memviz'

# DOCMODELS_PATH = BASE_DATA_PATH / 'docmodels'
DOCMODELS_PATH = TEMP_DATA_PATH / 'docmodels'

try:
    DOCMODEL_PATHS_LIST = [DOCMODELS_PATH / p for p in listdir(DOCMODELS_PATH)]
except FileNotFoundError:
    DOCMODEL_PATHS_LIST = None
    print('FileNotFoundError on DOCMODELS_PATH, operations requiring to load docmodels will not work')

TAGCOUNTERS_PATH = ANALYSIS_PATH / 'tagcounters'
LEXCOUNTS_PATH = ANALYSIS_PATH / 'lexcats'
COOCS_PATH = ANALYSIS_PATH / 'coocs'
LDA_PATH = ANALYSIS_PATH / 'lda'
KMEANS_PATH = ANALYSIS_PATH / 'kmeans'
LDA_OLD_PATH = ANALYSIS_PATH / 'lda_old'

# CSV Mappings paths
LEXICON_CSV_PATH = CSV_PATH / 'lexicon.csv'
DOCTYPE_CATS_CSV_PATH = CSV_PATH / 'doctype_cats.csv'
SECONDARY_SUBJECTS_CSV_PATH = CSV_PATH / 'secondary_subjects.csv'


RND_SEED = 2112

TOPIC_MAPPING = {'topic_0': 'Population-region',
                 'topic_1': 'Animal models',
                 'topic_2': 'Demographics',
                 'topic_3': 'Exposure factors',
                 'topic_4': 'Enzyme-production',
                 'topic_5': 'Plant genetics and species',
                 'topic_6': 'Genetic pathway',
                 'topic_7': 'Community health',
                 'topic_8': 'Survey-report',
                 'topic_9': 'Orthopaedic trauma',
                 'topic_10': 'Health research and policy',
                 'topic_11': 'Method-measurement',
                 'topic_12': 'Genetic transcription',
                 'topic_13': 'Hematology',
                 'topic_14': 'Infection-virus',
                 'topic_15': 'Test and prediction',
                 'topic_16': 'Genotype-phenotype',
                 'topic_17': 'Linguistic emphasis (jargon)',
                 'topic_18': 'Evolution and phylogenetics',
                 'topic_19': 'Bacteria',
                 'topic_20': 'Cell-oncology',
                 'topic_21': 'Chemical',
                 'topic_22': 'Mental health',
                 'topic_23': 'Rheumatology',
                 'topic_24': 'Mosquito-malaria',
                 'topic_25': 'Network-model',
                 'topic_26': 'Public health',
                 'topic_27': 'Physical activity',
                 'topic_28': 'Cell signaling',
                 'topic_29': 'Cell development',
                 'topic_30': 'PCR',
                 'topic_31': 'Nervous system',
                 'topic_32': 'Weight-obesity',
                 'topic_33': 'Screening',
                 'topic_34': 'Statistics',
                 'topic_35': 'Life cycle and reproduction',
                 'topic_36': 'Imaging-artery',
                 'topic_37': 'Food-consumption',
                 'topic_38': 'Genetic expression',
                 'topic_39': 'Sex and selection',
                 'topic_40': 'Cytology',
                 'topic_41': 'Malaria-parasite',
                 'topic_42': 'Cancer',
                 'topic_43': 'Infection resistance',
                 'topic_44': 'Maternity',
                 'topic_45': 'Muscle-motion',
                 'topic_46': 'Literature review',
                 'topic_47': 'Therapy',
                 'topic_48': 'Prognostic',
                 'topic_49': 'Medical training',
                 'topic_50': 'Cattle',
                 'topic_51': 'Cognitive performance',
                 'topic_52': 'Protein domain',
                 'topic_53': 'Cardiovascular conditions',
                 'topic_54': 'Method-model',
                 'topic_55': 'Change-effect',
                 'topic_56': 'Score-measure',
                 'topic_57': 'Surgery',
                 'topic_58': 'Healthcare',
                 'topic_59': 'Antibody-protein',
                 'topic_60': 'Cancer-tumor',
                 'topic_61': 'Respiratory',
                 'topic_62': 'Patient mortality',
                 'topic_63': 'Drug-treatment',
                 'topic_64': 'Diabetes',
                 'topic_65': 'Genetic expression rna',
                 'topic_66': 'Database-software',
                 'topic_67': 'Oxidative stress',
                 'topic_68': 'Immunology',
                 'topic_69': 'Clinical trials',
                 'topic_70': 'Diagnosis',
                 'topic_71': 'Loss-gain',
                 'topic_72': 'Brain',
                 'topic_73': 'Costs',
                 'topic_74': 'Genetic markers and traits',
                 'topic_75': 'Water-uptake',
                 'topic_76': 'Genetic sequence',
                 'topic_77': 'Childhood',
                 'topic_78': 'Genetic mutation',
                 'topic_79': 'Timelaps', }
