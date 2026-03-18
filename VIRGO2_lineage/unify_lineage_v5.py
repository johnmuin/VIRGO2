#!/usr/bin/env python3
import sys

# 扩展的属分类字典（基于 GTDB R220）
GENUS_TAXONOMY = {
    # Actinobacteria
    'Gardnerella': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Gardnerellales', 'f': 'Gardnerellaceae'},
    'Acetatifactor': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Eubacteriales', 'f': 'Eubacteriales_fa'},
    'Allisonella': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Acidaminococcales', 'f': 'Acidaminococcaceae'},
    'Alterileibacterium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Baileyella': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Oscillospirales', 'f': 'Oscillospiraceae'},
    'Bilifractor': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Oscillospirales', 'f': 'Oscillospiraceae'},
    'Actinomycetaceae': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Actinotignum': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Arachnia': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Arcanobacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Atopobacter': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Bifidobacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Bifidobacteriales', 'f': 'Bifidobacteriaceae'},
    'Brevibacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Mycobacteriales', 'f': 'Brevibacteriaceae'},
    'Collinsella': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Coriobacteriales', 'f': 'Coriobacteriaceae'},
    'Coriobacteriaceae': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Coriobacteriales', 'f': 'Coriobacteriaceae'},
    'Corynebacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Mycobacteriales', 'f': 'Corynebacteriaceae'},
    'Criibacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Coriobacteriales', 'f': 'Coriobacteriaceae'},
    'Cutibacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Propionibacteriales', 'f': 'Propionibacteriaceae'},
    'Dermabacter': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Dermabacterales', 'f': 'Dermabacteraceae'},
    'Fannyhessea': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Gulosibacter': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Mycobacteriales', 'f': 'Corynebacteriaceae'},
    'Mycobacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Mycobacteriales', 'f': 'Mycobacteriaceae'},
    'Olsenella': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Coriobacteriales', 'f': 'Atopobiaceae'},
    'Olegusella': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Mycobacteriales', 'f': 'Corynebacteriaceae'},
    'Pauljensenia': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Propionimicrobium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Propionibacteriales', 'f': 'Propionibacteriaceae'},
    'Rothia': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Micrococcales', 'f': 'Micrococcaceae'},
    'Slackia': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Coriobacteriales', 'f': 'Coriobacteriaceae'},
    'Trueperella': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Varibaculum': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Winkia': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    
    # Bacillota (Firmicutes)
    'Aerococcaceae': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Aerococcaceae'},
    'Anaerococcus': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Acidaminococcales', 'f': 'Anaerococcaceae'},
    'Blautia': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Bulleidia': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Acidaminococcales', 'f': 'Acidaminococcaceae'},
    'Catonella': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Dialister': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Acidaminococcales', 'f': 'Acidaminococcaceae'},
    'Eubacterium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Eubacteriales', 'f': 'Eubacteriaceae'},
    'Fenollaria': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Peptoniphilales', 'f': 'Peptoniphilaceae'},
    'Filifactor': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Peptoniphilaceae'},
    'Lactobacillus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Lactobacillaceae'},
    'Limosilactobacillus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Lactobacillaceae'},
    'Megasphaera': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Acidaminococcales', 'f': 'Acidaminococcaceae'},
    'Parvimonas': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Tissierellales', 'f': 'Peptoniphilaceae'},
    'Peptoniphilus': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Peptoniphilales', 'f': 'Peptoniphilaceae'},
    'Roseburia': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Ruminiclostridium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Ruminococcus': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Oscillospirales', 'f': 'Ruminococcaceae'},
    'Sodaliphilus': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Staphylococcus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Staphylococcales', 'f': 'Staphylococcaceae'},
    'Stomatobaculum': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Veillonellales', 'f': 'Selenomonadaceae'},
    'Streptococcus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Streptococcaceae'},
    'Veillonella': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Veillonellales', 'f': 'Veillonellaceae'},
    
    # Bacteroidota
    'Alloprevotella': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Prevotellaceae'},
    'Bacteroides': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'CAG-74': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'Cryptobacteroides': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Rikenellaceae'},
    'Porphyromonas': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Porphyromonadaceae'},
    'Prevotella': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Prevotellaceae'},
    'Tannerella': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Tannerellaceae'},
    
    # Campylobacterota
    'Campylobacter': {'p': 'Campylobacterota', 'c': 'Campylobacteria', 'o': 'Campylobacterales', 'f': 'Campylobacteraceae'},
    'Sutterella': {'p': 'Campylobacterota', 'c': 'Campylobacteria', 'o': 'Burkholderiales', 'f': 'Sutterellaceae'},
    
    # Fusobacteriota
    'Fusobacterium': {'p': 'Fusobacteriota', 'c': 'Fusobacteriia', 'o': 'Fusobacteriales', 'f': 'Fusobacteriaceae'},
    'Leptotrichia': {'p': 'Fusobacteriota', 'c': 'Fusobacteriia', 'o': 'Fusobacteriales', 'f': 'Leptotrichiaceae'},
    'Sneathia': {'p': 'Fusobacteriota', 'c': 'Fusobacteriia', 'o': 'Fusobacteriales', 'f': 'Leptotrichiaceae'},
    
    # Mycoplasmatota
    'Mycoplasma': {'p': 'Mycoplasmatota', 'c': 'Mollicutes', 'o': 'Mycoplasmatales', 'f': 'Mycoplasmataceae'},
    'Mycoplasmopsis': {'p': 'Mycoplasmatota', 'c': 'Mollicutes', 'o': 'Mycoplasmatales', 'f': 'Mycoplasmataceae'},
    'Ureaplasma': {'p': 'Mycoplasmatota', 'c': 'Mollicutes', 'o': 'Mycoplasmatales', 'f': 'Mycoplasmataceae'},
    
    # Pseudomonadota (Proteobacteria)
    'CAJPTP01': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Enterobacterales', 'f': 'Enterobacteriaceae'},
    'Citrobacter': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Enterobacterales', 'f': 'Enterobacteriaceae'},
    'Haemophilus': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Pasteurellales', 'f': 'Pasteurellaceae'},
    'W5053': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Enterobacterales', 'f': 'Enterobacteriaceae'},
    
    # Spirochaetota
    'Treponema': {'p': 'Spirochaetota', 'c': 'Spirochaetia', 'o': 'Treponematales', 'f': 'Treponemataceae'},
    
    # Other
    'Clostridium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Eubacteriales', 'f': 'Eubacteriaceae'},
    'Enterococcus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Enterococcaceae'},
    'UMGS822': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'Lachnospiraceae': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Caproicibacterium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Oscillospirales', 'f': 'Oscillospiraceae'},
    'Companilactobacillus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Lactobacillaceae'},
    
    # Additional genera to fix remaining problematic species
    'Escherichia': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Enterobacterales', 'f': 'Enterobacteriaceae'},
    'Klebsiella': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Enterobacterales', 'f': 'Enterobacteriaceae'},
    'Neisseria': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Neisseriales', 'f': 'Neisseriaceae'},
    'Lactococcus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Streptococcaceae'},
    'Proteus': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Enterobacterales', 'f': 'Enterobacteriaceae'},
    'Mogibacterium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Mogibacteriaceae'},
    'Gemella': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Staphylococcales', 'f': 'Gemellaceae'},
    'Peptostreptococcus': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Peptoniphilaceae'},
    'Erysipelotrichaceae': {'p': 'Bacillota_A', 'c': 'Erysipelotrichia', 'o': 'Erysipelotrichales', 'f': 'Erysipelotrichaceae'},
    'Ezakiella': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Peptoniphilaceae'},
    'Facklamia': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Aerococcaceae'},
    'Fastidiosipila': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Fastidiosipilaceae'},
    'Lancefieldella': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Lactobacillales', 'f': 'Streptococcaceae'},
    'Lawsonella': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Mycobacteriales', 'f': 'Nocardiaceae'},
    'Libanicoccus': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Oscillospirales', 'f': 'Oscillospiraceae'},
    'Mobiluncus': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Actinomycetales', 'f': 'Actinomycetaceae'},
    'Mordavella': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Muribaculaceae'},
    'Muribaculum': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Muribaculaceae'},
    'Paeniclostridium': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Peptostreptococcaceae'},
    'Peptoniphilaceae': {'p': 'Bacillota_C', 'c': 'Negativicutes', 'o': 'Peptoniphilales', 'f': 'Peptoniphilaceae'},
    'Propionibacterium': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Propionibacteriales', 'f': 'Propionibacteriaceae'},
    'Pseudoglutamicibacter': {'p': 'Actinomycetota', 'c': 'Actinomycetes', 'o': 'Micrococcales', 'f': 'Micrococcaceae'},
    'Pyramidobacter': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Pyramidobacteriaceae'},
    'RUG100': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'RUG11792': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Prevotellaceae'},
    'SY095': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'Johnsonella': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Tissierellales', 'f': 'Tissierellaceae'},
    'Mediterraneibacter': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Lachnospirales', 'f': 'Lachnospiraceae'},
    'Fermentimonas': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Marinilabiliaceae'},
    'Fictibacillus': {'p': 'Bacillota', 'c': 'Bacilli', 'o': 'Bacillales', 'f': 'Bacillaceae'},
    'Levyella': {'p': 'Bacillota_A', 'c': 'Clostridia', 'o': 'Oscillospirales', 'f': 'Oscillospiraceae'},
    'Malacoplasma': {'p': 'Mycoplasmatota', 'c': 'Mollicutes', 'o': 'Mycoplasmatales', 'f': 'Mycoplasmataceae'},
    'Haemophilum': {'p': 'Pseudomonadota', 'c': 'Gammaproteobacteria', 'o': 'Pasteurellales', 'f': 'Pasteurellaceae'},
    'JABCPO02': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'MultiGenera': {'p': 'Bacteroidota', 'c': 'Bacteroidia', 'o': 'Bacteroidales', 'f': 'Bacteroidaceae'},
    'Oligotropha': {'p': 'Pseudomonadota', 'c': 'Alphaproteobacteria', 'o': 'Rhizobiales', 'f': 'Nitrobacteraceae'},
}

def normalize_lineage(species, domain, lineage):
    """统一 lineage 为 7-level 格式"""
    
    levels = {
        'd': 'Unclassified',
        'p': 'Unclassified', 
        'c': 'Unclassified',
        'o': 'Unclassified',
        'f': 'Unclassified',
        'g': 'Unclassified',
        's': 'Unclassified'
    }
    
    if not lineage or lineage in ['Unknown', 'Not_available']:
        parts = species.split('_')
        if len(parts) >= 2:
            levels['g'] = parts[0]
            levels['s'] = species.replace('_', ' ')
        else:
            levels['s'] = species
        return format_lineage(levels)
    
    raw_parts = lineage.split(';')
    genus = species.split('_')[0] if '_' in species else species
    
    # 细菌
    if domain == 'Bacteria' or lineage.startswith('d__'):
        for part in raw_parts:
            part = part.strip()
            if part.startswith('d__'): levels['d'] = part[3:]
            elif part.startswith('p__'): levels['p'] = part[3:]
            elif part.startswith('c__'): levels['c'] = part[3:]
            elif part.startswith('o__'): levels['o'] = part[3:]
            elif part.startswith('f__'): levels['f'] = part[3:]
            elif part.startswith('g__'): levels['g'] = part[3:]
            elif part.startswith('s__'): levels['s'] = part[3:]
        
        # 使用属字典填充缺失的中间等级
        if genus in GENUS_TAXONOMY:
            tax = GENUS_TAXONOMY[genus]
            if levels['p'] in ['Unclassified', 'Bacteria']:
                levels['p'] = tax['p']
            if levels['c'] in ['Unclassified', 'Bacteria']:
                levels['c'] = tax['c']
            if levels['o'] in ['Unclassified', 'Bacteria']:
                levels['o'] = tax['o']
            if levels['f'] in ['Unclassified', 'Bacteria']:
                levels['f'] = tax['f']
    
    # 真菌
    elif domain == 'Fungi':
        if len(raw_parts) >= 1: levels['d'] = raw_parts[0]
        if len(raw_parts) >= 2: levels['p'] = raw_parts[1]
        if len(raw_parts) >= 4: levels['c'] = raw_parts[3]
        if len(raw_parts) >= 6: levels['o'] = raw_parts[5]
        if len(raw_parts) >= 7: levels['f'] = raw_parts[6]
        if len(raw_parts) >= 9: levels['g'] = raw_parts[8]
        if len(raw_parts) >= 10: levels['s'] = raw_parts[9].replace('_', ' ')
        elif len(raw_parts) >= 9: levels['s'] = raw_parts[8].replace('_', ' ')
    
    # 病毒
    elif domain in ['Phage', 'Human_virus']:
        if len(raw_parts) >= 1: levels['d'] = raw_parts[0]
        if len(raw_parts) >= 2: levels['p'] = raw_parts[1]
        if len(raw_parts) >= 4: levels['c'] = raw_parts[3]
        if len(raw_parts) >= 6: levels['o'] = raw_parts[5]
        if len(raw_parts) >= 7: levels['f'] = raw_parts[6]
        if len(raw_parts) >= 9: levels['g'] = raw_parts[8]
        if len(raw_parts) >= 10: levels['s'] = raw_parts[9].replace('_', ' ')
        elif len(raw_parts) >= 8:
            if '_phage' in raw_parts[-1]:
                levels['g'] = raw_parts[-1].split('_')[0]
                levels['s'] = raw_parts[-1].replace('_', ' ')
    
    # 原生生物
    elif domain == 'Protist':
        if len(raw_parts) >= 1: levels['d'] = raw_parts[0]
        if len(raw_parts) >= 2: levels['p'] = raw_parts[1]
        if len(raw_parts) >= 3: levels['c'] = raw_parts[2]
        if len(raw_parts) >= 4: levels['o'] = raw_parts[3]
        if len(raw_parts) >= 5: levels['f'] = raw_parts[4]
        if len(raw_parts) >= 8: levels['g'] = raw_parts[7]
        if len(raw_parts) >= 9: levels['s'] = raw_parts[8].replace('_', ' ')
    
    # 填充缺失的层级
    if levels['p'] in ['Unclassified', 'Bacteria']:
        levels['p'] = levels['d']
    if levels['c'] in ['Unclassified', 'Bacteria', levels['p']]:
        levels['c'] = levels['p'] + '_class' if levels['p'] != 'Unclassified' else 'Unclassified'
    if levels['o'] in ['Unclassified', 'Bacteria', levels['c']]:
        levels['o'] = levels['c'] + '_order' if levels['c'] != 'Unclassified' else 'Unclassified'
    if levels['f'] in ['Unclassified', 'Bacteria', levels['o']]:
        levels['f'] = levels['o'] + '_family' if levels['o'] != 'Unclassified' else 'Unclassified'
    if levels['g'] == 'Unclassified':
        levels['g'] = genus
    if levels['s'] == 'Unclassified':
        levels['s'] = species.replace('_', ' ')
    
    return format_lineage(levels)

def format_lineage(levels):
    return f"d__{levels['d']};p__{levels['p']};c__{levels['c']};o__{levels['o']};f__{levels['f']};g__{levels['g']};s__{levels['s']}"

def main():
    input_file = 'virgo2_all_species_lineage_complete.tsv'
    output_file = 'virgo2_all_species_lineage_7levels_v3.tsv'
    
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        fout.write("Species\tDomain\tLineage_7levels\n")
        header = fin.readline()
        
        for line in fin:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 3:
                continue
            
            species = parts[0]
            domain = parts[1]
            lineage = parts[2] if len(parts) > 2 else ""
            
            new_lineage = normalize_lineage(species, domain, lineage)
            fout.write(f"{species}\t{domain}\t{new_lineage}\n")
    
    print(f"已生成统一格式的 lineage 表: {output_file}")
    
    # 统计问题物种数量
    problematic = 0
    with open(output_file, 'r') as f:
        for line in f:
            if 'p__Bacteria;c__Bacteria' in line or 'p__Unclassified' in line:
                problematic += 1
    
    print(f"\n仍有问题的物种数: {problematic}")

if __name__ == '__main__':
    main()
