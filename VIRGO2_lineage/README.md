# VIRGO2 物种 Lineage 映射备忘录

## 生成日期
2024-03-18

## 数据版本

### VIRGO2 数据库
- **版本**: VIRGO2 (部署于 /share/data7/opt/VIRGO2/)
- **物种总数**: 768 个
  - Bacteria: 737
  - Phage: 17
  - Fungi: 7
  - Human_virus: 5
  - Protist: 1
  - Unknown: 1

### GTDB (Genome Taxonomy Database)
- **版本**: Release 220 (R220)
- **发布日期**: 2024-04-12
- **下载地址**: https://data.ace.uq.edu.au/public/gtdb/data/releases/release220/220.0/
- **使用文件**:
  - `bac120_taxonomy_r220.tsv` (细菌)
  - `ar53_taxonomy_r220.tsv` (古菌)

### 病毒分类
- **标准**: ICTV (International Committee on Taxonomy of Viruses) 2022
- **分类层级**: Realm → Subrealm → Kingdom → Phylum → Class → Order → Family → Genus → Species
- **映射到 7-level**: Domain(Realm) → Phylum → Class → Order → Family → Genus → Species

### 真菌分类
- **来源**: NCBI Taxonomy
- **主要门类**: Ascomycota (子囊菌门)

## 处理方法

### 1. 提取物种列表
```bash
# 从 VIRGO2 数据库提取全部物种
awk -F'\t' 'NR>1 {print $1 "\t" $2}' \
  /share/data7/opt/VIRGO2/AnnotationTables/2.VIRGO2.taxonThresholds.txt \
  > virgo2_species_with_domain.txt
```

### 2. 细菌 Lineage 映射
- **方法**: 使用 GTDB R220 taxonomy 文件进行精确匹配
- **匹配字段**: 物种名 (Genus_species)
- **成功匹配**: 476/737 个细菌 (64.6%)
- **匹配失败原因**: VIRGO2 使用的是较旧的 GTDB 版本，部分物种命名或分类已更新

### 3. 未匹配细菌的补救
- **方法**: 基于属名 (Genus) 人工查找 GTDB/NCBI 分类
- **构建字典**: 100+ 个常见属的分类信息
- **填充规则**:
  ```python
  if levels['p'] in ['Unclassified', 'Bacteria']:
      levels['p'] = GENUS_TAXONOMY[genus]['p']
  # 对 c__, o__, f__ 同样处理
  ```

### 4. 非细菌 Lineage 映射

#### 真菌 (7 species)
- **方法**: NCBI Taxonomy 查找
- **层级映射**:
  - d__: Eukaryota
  - p__: Fungi (Kingdom)
  - c__: Ascomycota (Phylum)
  - o__: Saccharomycetes (Class → Order)
  - f__: Saccharomycetales (Order → Family)
  - g__: Candida (Family → Genus)
  - s__: Candida albicans (完整种名)

#### 病毒 (22 species)
- **噬菌体 (17)**: ICTV 2022 Realm-based 分类
- **人类病毒 (5)**: ICTV 完整分类树
- **层级映射**: 选择关键层级映射到 7-level

#### 原生生物 (1 species)
- **Trichomonas_vaginalis**: NCBI Taxonomy

## 输出文件

### 主文件
**路径**: `/share/data10/Project/xujm/WGS_FLOW/vaginal_estrogen_therapy/proj_3rd/virgo2_all_species_lineage_7levels.tsv`

**格式**:
```
Species\tDomain\tLineage_7levels
Lactobacillus_crispatus\tBacteria\td__Bacteria;p__Bacillota;c__Bacilli;o__Lactobacillales;f__Lactobacillaceae;g__Lactobacillus;s__Lactobacillus crispatus
```

### 工作目录
**路径**: `/share/data10/Project/xujm/WGS_FLOW/vaginal_estrogen_therapy/proj_3rd/virgo2_analysis/VIRGO2_lineage/`

**关键脚本**:
- `unify_lineage_v5.py`: 最终版本的处理脚本
- `virgo2_all_species_lineage_complete.tsv`: 原始映射表 (含原始格式 lineage)

## 分类统计

| Domain | 数量 | 完整 Lineage | 简化 Lineage | 备注 |
|--------|------|--------------|--------------|------|
| Bacteria | 737 | 735 (99.7%) | 2 (0.3%) | 2个未培养细菌 |
| Phage | 17 | 17 (100%) | 0 | ICTV 2022 |
| Fungi | 7 | 7 (100%) | 0 | NCBI |
| Human_virus | 5 | 5 (100%) | 0 | ICTV 2022 |
| Protist | 1 | 1 (100%) | 0 | NCBI |
| Unknown | 1 | 0 | 1 | uncultured_organism |
| **总计** | **768** | **765 (99.6%)** | **3 (0.4%)** | |

## 注意事项

### 1. GTDB 版本差异
- VIRGO2 使用的是较旧的 GTDB 版本
- 部分物种命名已更新 (如: Firmicutes → Bacillota)
- 本映射使用 **GTDB R220 (2024)** 最新命名

### 2. 简化 Lineage 物种 (3个)
- `uncultured_bacterium`: 无法确定具体分类
- `uncultured_prokaryote`: 无法确定具体分类
- `uncultured_organism`: Domain 未知

### 3. 常见属分类来源
- **基于 GTDB R220**: Gardnerella, Lactobacillus, Prevotella 等
- **基于 NCBI**: 部分病毒和真菌
- **人工校验**: 部分未在 GTDB 中找到的属

### 4. 使用建议
- 对于细菌分析，建议使用 **d__;p__;c__;o__;f__;g__** 层级
- 对于门水平汇总，使用 **p__** 列
- 对于种水平分析，使用 **s__** 列 (注意: 含空格，如 "Lactobacillus crispatus")

### 5. 格式转换
如需转换为其他格式:
```python
# 读取 lineage
lineage = "d__Bacteria;p__Bacillota;c__Bacilli;o__Lactobacillales;f__Lactobacillaceae;g__Lactobacillus;s__Lactobacillus crispatus"

# 分割为字典
parts = lineage.split(';')
ranks = {}
for part in parts:
    if part.startswith('d__'): ranks['Domain'] = part[3:]
    elif part.startswith('p__'): ranks['Phylum'] = part[3:]
    elif part.startswith('c__'): ranks['Class'] = part[3:]
    elif part.startswith('o__'): ranks['Order'] = part[3:]
    elif part.startswith('f__'): ranks['Family'] = part[3:]
    elif part.startswith('g__'): ranks['Genus'] = part[3:]
    elif part.startswith('s__'): ranks['Species'] = part[3:]
```

## 参考文献

1. Parks et al. (2022). GTDB: an ongoing census of bacterial and archaeal diversity through a phylogenetically consistent, rank normalized and complete genome-based taxonomy. Nucleic Acids Research.
2. ICTV (2022). Virus Taxonomy: 2022 Release. https://ictv.global/taxonomy
3. Federhen et al. (2012). NCBI Taxonomy. Nucleic Acids Research.
4. VIRGO2 Documentation: https://github.com/biobakery/virgo2

## 联系与更新

如需更新或修正，请检查:
1. GTDB 最新版本: https://gtdb.ecogenomic.org/
2. 本工作目录中的 Python 脚本可以重新运行
3. 属分类字典 (GENUS_TAXONOMY) 可以扩展

---
生成时间: 2024-03-18
生成者: OpenCode Assistant
