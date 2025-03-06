#!/bin/bash
# 设置路径变量
INPUT_DIR="/data/home/xiaomeng/IOM/Project/01_Micro/download"               # 替换为你的基因组文件夹父目录
OUTPUT_DIR="/data/home/xiaomeng/IOM/Project/01_Micro/download/GTDB"                      # 替换为输出目录
THREADS=20                                        # 设置线程数
# 创建输出目录
mkdir -p "$OUTPUT_DIR"
# 遍历每个基因组文件夹
for folder in "$INPUT_DIR"/*/; do
    # 提取文件夹名(不带路径)
    foldername=$(basename "$folder")
    
    # 创建每个样本对应的输出目录
    sample_outdir="$OUTPUT_DIR/$foldername"
    mkdir -p "$sample_outdir"
    
    # 运行GTDB-Tk分类流程
    gtdbtk classify_wf \
	--skip_ani_screen \
        --genome_dir "$folder" \
        --extension "fna" \
        --out_dir "$sample_outdir" \
        --cpus $THREADS \
        --tmpdir /tmp 2>&1 | tee "$sample_outdir/gtdbtk.log"
    
    echo "[完成] 样本 $foldername 处理完成"
done
echo "所有样本处理完成！结果保存在: $OUTPUT_DIR"

