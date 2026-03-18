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

python3 "${VIRGO2_SCRIPT}" taxonomy \
    -i "${compiled}" \
    -o "${output_prefix}" \
    -b "${TAX_BACTERIA}" \
    -f "${TAX_FILTER}" \
    -r "${TAX_READCOUNTS}" \
    -m "${TAX_MULTIGENERA}"

if [[ -f "${output_prefix}.relAbund.csv" ]]; then
    species=$(tail -n +2 "${output_prefix}.relAbund.csv" | wc -l)
    echo ""
    echo "Taxonomy complete: ${species} species detected"
    echo "Output: ${output_prefix}.relAbund.csv"
else
    echo "Error: Taxonomy failed"
    exit 1
fi

# Convert to lineage format (L1-L7)
echo ""
echo "Converting to lineage format (L1-L7)..."

LINEAGE_SCRIPT="${VIRGO2_DIR}/VIRGO2_lineage/convert_to_lineage.py"
LINEAGE_MAPPING="${VIRGO2_DIR}/VIRGO2_lineage/virgo2_all_species_lineage_7levels_v3.tsv"
LINEAGE_OUTPUT="${VIRGO2_OUTDIR}/taxonomy/lineage_profile"

if [[ -f "${LINEAGE_SCRIPT}" && -f "${LINEAGE_MAPPING}" ]]; then
    python3 "${LINEAGE_SCRIPT}" \
        -i "${output_prefix}.relAbund.csv" \
        -m "${LINEAGE_MAPPING}" \
        -o "${LINEAGE_OUTPUT}"
    
    if [[ -d "${LINEAGE_OUTPUT}" ]]; then
        echo "Lineage conversion complete"
        echo "Output: ${LINEAGE_OUTPUT}/"
        ls -lh "${LINEAGE_OUTPUT}"/L*.tsv 2>/dev/null | awk '{print "  " $9}'
    else
        echo "Warning: Lineage conversion may have failed"
    fi
else
    echo "Warning: Lineage script or mapping file not found, skipping lineage conversion"
fi

echo ""
echo "End: $(date)"
