#!/bin/bash
# Step 3: VIRGO2 Compile
# 合并所有样品结果

CONFIG_FILE="${1:-config.sh}"
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "Error: Config file not found: ${CONFIG_FILE}"
    exit 1
fi

source "${CONFIG_FILE}"
export PATH="${CONDA_BASE}/envs/${CONDA_ENV}/bin:${PATH}"

echo "========================================"
echo "Step 3: VIRGO2 Compile"
echo "========================================"
echo "Start: $(date)"
echo ""

mkdir -p "${VIRGO2_OUTDIR}/compiled"

map_dir="${VIRGO2_OUTDIR}/map_results"
output_prefix="${VIRGO2_OUTDIR}/compiled/VIRGO2_compiled"

completed=$(ls "${map_dir}"/*.out 2>/dev/null | wc -l)
echo "Detected ${completed} map results"

if [[ ${completed} -eq 0 ]]; then
    echo "Error: No map results found"
    exit 1
fi

python3 "${VIRGO2_SCRIPT}" compile \
    -i "${map_dir}" \
    -o "${output_prefix}"

if [[ -f "${output_prefix}.summary.NR.txt" ]]; then
    rows=$(wc -l < "${output_prefix}.summary.NR.txt")
    cols=$(head -1 "${output_prefix}.summary.NR.txt" | awk -F'\t' '{print NF}')
    echo ""
    echo "Complete: ${rows} genes x ${cols} samples"
else
    echo "Error: Compile failed"
    exit 1
fi

echo "End: $(date)"
