#!/usr/bin/env python3
"""
将物种丰度数据转换为L1-L7分类层级格式

用法:
    python3 convert_to_lineage.py -i input.csv -m lineage.tsv -o output_dir [选项]
    
示例:
    python3 convert_to_lineage.py \
        -i VIRGO2_taxonomy.relAbund.csv \
        -m virgo2_all_species_lineage_7levels_v3.tsv \
        -o ./lineage_profile
"""

import argparse
import pandas as pd
import sys
import os
from collections import defaultdict


def parse_lineage(lineage_str):
    """解析lineage字符串，返回各级别"""
    levels = lineage_str.split(';')
    while len(levels) < 7:
        levels.append('')
    return levels[:7]


def convert_lineage_to_kraken_format(levels):
    """将lineage转换为kraken格式 (d__ -> k__)"""
    result = {}
    current_path = []
    
    for i, level in enumerate(levels):
        if level:
            if level.startswith('d__'):
                level = 'k__' + level[3:]
            current_path.append(level)
        else:
            current_path.append('')
        
        path_parts = [p for p in current_path if p]
        result[f'L{i+1}'] = ';'.join(path_parts) if path_parts else ''
    
    return result


def load_lineage_mapping(lineage_file):
    """加载物种到lineage的映射"""
    lineage_df = pd.read_csv(lineage_file, sep='\t')
    species_to_lineage = {}
    
    for _, row in lineage_df.iterrows():
        species_name = row['Species']
        lineage_str = row['Lineage_7levels']
        species_to_lineage[species_name] = lineage_str
    
    return species_to_lineage


def process_abundance_data(abund_file, species_to_lineage, verbose=False):
    """处理丰度数据，返回层级数据和元信息"""
    abund_df = pd.read_csv(abund_file, index_col=0)
    
    sample_names = abund_df.index.tolist()
    species_names = abund_df.columns.tolist()
    
    level_data = {f'L{i}': defaultdict(lambda: defaultdict(float)) for i in range(1, 8)}
    unmatched_species = []
    
    for sample_idx, sample_name in enumerate(sample_names):
        if verbose and sample_idx % 50 == 0:
            print(f"  Processing sample {sample_idx+1}/{len(sample_names)}: {sample_name}")
        
        for species_idx, species_name in enumerate(species_names):
            abundance = abund_df.iloc[sample_idx, species_idx]
            
            if abundance == 0:
                continue
            
            if species_name not in species_to_lineage:
                if species_name not in unmatched_species:
                    unmatched_species.append(species_name)
                continue
            
            lineage_str = species_to_lineage[species_name]
            levels = parse_lineage(lineage_str)
            kraken_lineages = convert_lineage_to_kraken_format(levels)
            
            for level_name, lineage_path in kraken_lineages.items():
                if lineage_path:
                    level_data[level_name][lineage_path][sample_name] += abundance
    
    return level_data, sample_names, unmatched_species


def write_output_files(level_data, sample_names, output_dir):
    """写入输出文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    for level_name in [f'L{i}' for i in range(1, 8)]:
        output_file = os.path.join(output_dir, f"{level_name}.txt")
        data = level_data[level_name]
        
        rows = []
        for lineage_path in sorted(data.keys()):
            row = {'FeatureID': lineage_path}
            for sample_name in sample_names:
                row[sample_name] = data[lineage_path].get(sample_name, 0)
            rows.append(row)
        
        if rows:
            result_df = pd.DataFrame(rows)
            result_df = result_df[['FeatureID'] + sample_names]
            result_df.to_csv(output_file, sep='\t', index=False)
            print(f"  {level_name}: {len(rows)} unique taxa -> {output_file}")
        else:
            print(f"  {level_name}: No data")


def validate_output(level_data, sample_names):
    """验证输出数据的正确性"""
    print("\n=== Validation ===")
    
    sample_to_check = sample_names[0] if sample_names else None
    if sample_to_check:
        print(f"Abundance sum check for sample '{sample_to_check}':")
        for level_name in [f'L{i}' for i in range(1, 8)]:
            data = level_data[level_name]
            total = sum(data[lineage].get(sample_to_check, 0) for lineage in data)
            status = "OK" if abs(total - 1.0) < 0.01 else "WARN"
            print(f"  {level_name}: {total:.6f} [{status}]")


def main():
    parser = argparse.ArgumentParser(
        description='Convert species abundance to L1-L7 lineage format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python3 convert_to_lineage.py -i input.csv -m lineage.tsv -o output/

  # With verbose output and validation
  python3 convert_to_lineage.py -i input.csv -m lineage.tsv -o output/ -v --validate
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='Input abundance CSV file (samples as rows, species as columns)')
    parser.add_argument('-m', '--mapping', required=True,
                        help='Species to lineage mapping TSV file (columns: Species, Domain, Lineage_7levels)')
    parser.add_argument('-o', '--output', required=True,
                        help='Output directory for L1-L7 files')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--validate', action='store_true',
                        help='Validate output after conversion')
    
    args = parser.parse_args()
    
    # 验证输入文件存在
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.mapping):
        print(f"Error: Mapping file not found: {args.mapping}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Loading lineage mapping from: {args.mapping}")
    species_to_lineage = load_lineage_mapping(args.mapping)
    print(f"Loaded {len(species_to_lineage)} species lineage mappings")
    
    print(f"\nProcessing abundance data from: {args.input}")
    level_data, sample_names, unmatched = process_abundance_data(
        args.input, species_to_lineage, verbose=args.verbose
    )
    
    print(f"\nFound {len(sample_names)} samples")
    
    if unmatched:
        print(f"\nWarning: {len(unmatched)} species not found in lineage mapping")
        if args.verbose:
            for sp in unmatched[:20]:
                print(f"  - {sp}")
            if len(unmatched) > 20:
                print(f"  ... and {len(unmatched) - 20} more")
    
    print(f"\nWriting output files to: {args.output}")
    write_output_files(level_data, sample_names, args.output)
    
    if args.validate:
        validate_output(level_data, sample_names)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
