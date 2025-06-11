import os

# Directory settings
INPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'inputs')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')

# Deduplication settings
THRESH = 85

# Column remapping per source
REMAP = {
    'ts_technologies': {'name':'product_name','description':'description','url':'source_url','category':'category'},
    'bd_technologies': {'product_name':'product_name','description':'description','seller_website':'source_url','categories':'category'}
}