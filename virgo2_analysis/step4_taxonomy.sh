#!/bin/bash
# Step 4: VIRGO2 Taxonomy
# 物种组成分析

CONFIG_FILE="${1:-config.sh}"
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "Error: Config file not found: ${CONFIG_FILE}"
    exit 1
fi

source "${CONFIG_FILE}"
export PATH="${CONDA_BASE}/envs/${CONDA_ENV}/bin:${PATH}"

echo "========================================"
echo "Step 4: VIRGO2 Taxonomy"
echo "========================================"
echo "Start: $(date)"
echo ""

mkdir -p "${VIRGO2_OUTDIR}/taxonomy"

compiled="${VIRGO2_OUTDIR}/compiled/VIRGO2_compiled.summary.NR.txt"
output_prefix="${VIRGO2_OUTDIR}/taxonomy/VIRGO2_taxonomy"

if [[ ! -f "${compiled}" ]]; then
    echo "Error: Compiled file not found: ${compiled}"
    exit 1
fi

# 1. 计算相对丰度 (Relative Abundance)
echo "Calculating relative abundance (-r 0)..."
python3 "${VIRGO2_SCRIPT}" taxonomy \
    -i "${compiled}" \
    -o "${output_prefix}" \
    -b "${TAX_BACTERIA}" \
    -f "${TAX_FILTER}" \
    -r 0 \
    -m "${TAX_MULTIGENERA}"

# 2. 计算reads数 (Read Counts)
echo "Calculating read counts (-r 1)..."
python3 "${VIRGO2_SCRIPT}" taxonomy \
    -i "${compiled}" \
    -o "${output_prefix}" \
    -b "${TAX_BACTERIA}" \
    -f "${TAX_FILTER}" \
    -r 1 \
    -m "${TAX_MULTIGENERA}"

if [[ -f "${output_prefix}.relAbund.csv" && -f "${output_prefix}.readCount.csv" ]]; then
    species=$(tail -n +2 "${output_prefix}.relAbund.csv" | wc -l)
    echo ""
    echo "Taxonomy complete: ${species} species detected"
    echo "Output relAbund: ${output_prefix}.relAbund.csv"
    echo "Output readCount: ${output_prefix}.readCount.csv"
else
    echo "Error: Taxonomy failed (one or both output files are missing)"
    exit 1
fi

# Convert to lineage format (L1-L7)
echo ""
echo "Converting to lineage format (L1-L7)..."

LINEAGE_SCRIPT="${VIRGO2_DIR}/VIRGO2_lineage/convert_to_lineage.py"
LINEAGE_MAPPING="${VIRGO2_DIR}/VIRGO2_lineage/virgo2_all_species_lineage_7levels_v3.tsv"
LINEAGE_OUTPUT_RELABUND="${VIRGO2_OUTDIR}/taxonomy/lineage_profile_relAbund"
LINEAGE_OUTPUT_READCOUNT="${VIRGO2_OUTDIR}/taxonomy/lineage_profile_readCount"

if [[ -f "${LINEAGE_SCRIPT}" && -f "${LINEAGE_MAPPING}" ]]; then
    echo "  -> Processing relative abundance..."
    python3 "${LINEAGE_SCRIPT}" \
        -i "${output_prefix}.relAbund.csv" \
        -m "${LINEAGE_MAPPING}" \
        -o "${LINEAGE_OUTPUT_RELABUND}"
        
    echo "  -> Processing read counts..."
    python3 "${LINEAGE_SCRIPT}" \
        -i "${output_prefix}.readCount.csv" \
        -m "${LINEAGE_MAPPING}" \
        -o "${LINEAGE_OUTPUT_READCOUNT}"
    
    if [[ -d "${LINEAGE_OUTPUT_RELABUND}" && -d "${LINEAGE_OUTPUT_READCOUNT}" ]]; then
        echo "Lineage conversion complete"
        echo "Output relAbund: ${LINEAGE_OUTPUT_RELABUND}/"
        echo "Output readCount: ${LINEAGE_OUTPUT_READCOUNT}/"
    else
        echo "Warning: Lineage conversion may have failed"
    fi
else
    echo "Warning: Lineage script or mapping file not found, skipping lineage conversion"
fi

echo ""
echo "End: $(date)"
