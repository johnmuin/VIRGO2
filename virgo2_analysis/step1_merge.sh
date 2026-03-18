#!/bin/bash
#===============================================================================
# Step 1: Merge Reads
# 合并双端测序数据为单端
#===============================================================================

# 加载配置
CONFIG_FILE="${1:-config.sh}"
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "错误: 配置文件不存在: ${CONFIG_FILE}"
    echo "用法: bash $0 [config_file]"
    exit 1
fi

source "${CONFIG_FILE}"

echo "========================================"
echo "Step 1: Merge Reads"
echo "========================================"
echo "配置文件: ${CONFIG_FILE}"
echo "输入目录: ${INPUT_DIR}"
echo "输出目录: ${VIRGO2_OUTDIR}/merged_reads"
echo "开始时间: $(date)"
echo ""

# 检查并创建目录
check_directories

# 获取样品列表
samples=$(get_samples)
total=$(echo "${samples}" | wc -l)

echo "找到 ${total} 个样品"
echo ""

# 合并每个样品
count=0
for sample in ${samples}; do
    count=$((count + 1))
    
    R1="${INPUT_DIR}/${sample}.rmhost_R1.fastq.gz"
    R2="${INPUT_DIR}/${sample}.rmhost_R2.fastq.gz"
    OUTPUT="${VIRGO2_OUTDIR}/merged_reads/${sample}.merged.fastq.gz"
    
    # 跳过已存在的
    if [[ -f "${OUTPUT}" ]]; then
        echo "[${count}/${total}] ${sample} - 已存在，跳过"
        continue
    fi
    
    echo "[${count}/${total}] ${sample} - 合并中..."
    
    # 检查R1是否存在
    if [[ ! -f "${R1}" ]]; then
        echo "  错误: ${R1} 不存在"
        continue
    fi
    
    # 合并R1和R2（如果R2存在）
    if [[ -f "${R2}" ]]; then
        zcat "${R1}" "${R2}" | pigz -p 4 > "${OUTPUT}"
    else
        echo "  警告: ${R2} 不存在，仅使用R1"
        zcat "${R1}" | pigz -p 4 > "${OUTPUT}"
    fi
    
    # 验证输出
    if [[ -f "${OUTPUT}" ]]; then
        reads=$(zcat "${OUTPUT}" 2>/dev/null | wc -l)
        reads=$((reads / 4))
        echo "  完成: ${reads} reads"
    else
        echo "  错误: 合并失败"
    fi
done

echo ""
echo "========================================"
echo "Merge 完成: $(date)"
echo "输出目录: ${VIRGO2_OUTDIR}/merged_reads"
echo "========================================"
