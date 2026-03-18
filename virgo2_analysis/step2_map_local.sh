#!/bin/bash
# Step 2: VIRGO2 Map (Local Mode)
# 本地运行map比对

CONFIG_FILE="${1:-config.sh}"
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "Error: Config file not found: ${CONFIG_FILE}"
    exit 1
fi

source "${CONFIG_FILE}"

# Set PATH to use virgo2 environment
export PATH="${CONDA_BASE}/envs/${CONDA_ENV}/bin:${PATH}"

echo "========================================"
echo "Step 2: VIRGO2 Map (Local)"
echo "========================================"
echo "Start: $(date)"
echo ""

mkdir -p "${VIRGO2_OUTDIR}/map_results"

samples=$(ls "${VIRGO2_OUTDIR}/merged_reads"/*.merged.fastq.gz 2>/dev/null | \
    xargs -n1 basename | sed 's/.merged.fastq.gz//')

total=$(echo "${samples}" | wc -l)
echo "Samples to process: ${total}"
echo ""

count=0
for sample in ${samples}; do
    count=$((count + 1))
    input="${VIRGO2_OUTDIR}/merged_reads/${sample}.merged.fastq.gz"
    output_prefix="${VIRGO2_OUTDIR}/map_results/${sample}"
    
    if [[ -f "${output_prefix}.out" ]]; then
        echo "[${count}/${total}] ${sample} - already done"
        continue
    fi
    
    echo "[${count}/${total}] ${sample} - mapping..."
    
    python3 "${VIRGO2_SCRIPT}" map \
        -r "${input}" \
        -c "${MAP_COV}" \
        -p "${MAP_THREADS}" \
        -o "${output_prefix}" \
        -b 0 \
        > "${VIRGO2_OUTDIR}/logs/${sample}.map.log" 2>&1
    
    if [[ -f "${output_prefix}.out" ]]; then
        echo "  Done"
    else
        echo "  Failed"
    fi
done

echo ""
echo "Map complete: $(date)"
