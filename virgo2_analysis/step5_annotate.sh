#!/bin/bash
# Step 5: Add Annotations
# 合并所有功能注释

CONFIG_FILE="${1:-config.sh}"
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "Error: Config file not found: ${CONFIG_FILE}"
    exit 1
fi

source "${CONFIG_FILE}"
export PATH="${CONDA_BASE}/envs/${CONDA_ENV}/bin:${PATH}"

echo "========================================"
echo "Step 5: Add Annotations"
echo "========================================"
echo "Start: $(date)"
echo ""

input="${VIRGO2_OUTDIR}/compiled/VIRGO2_compiled.summary.NR.txt"
output_prefix="${VIRGO2_OUTDIR}/annotation/VIRGO2_annotated"

if [[ ! -f "${input}" ]]; then
    echo "Error: Input file not found: ${input}"
    exit 1
fi

mkdir -p "${VIRGO2_OUTDIR}/annotation"

echo "Input: ${input}"
echo "Output: ${output_prefix}_all_annotations.csv"
echo ""

# Get script directory
MERGE_ANN_SCRIPT="${VIRGO2_DIR}/AccessoryScripts/merge_annotations.py"
python3 "${MERGE_ANN_SCRIPT}" \
    "${input}" \
    "${output_prefix}"

echo ""
echo "Complete: $(date)"
