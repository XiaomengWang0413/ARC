import os
import shutil
from pathlib import Path

# 需要修改的配置参数
base_dir = "/data/home/xiaomeng/IOM/Project/01_Micro/download/End/1"  # 替换为您的总目录路径
annotation_suffix = ".tsv"             # 注释文件后缀（如：.tsv, .summary等）
genome_suffix = ".fna"                # 基因组文件后缀（如.fna, .fasta等）
target_taxonomy = "d__Archaea;p__Micrarchaeota"

def process_bioprojects():
    # 遍历基础目录下的所有子目录
    for bioproject_dir in Path(base_dir).iterdir():
        if not bioproject_dir.is_dir():
            continue
        
        print(f"Processing: {bioproject_dir.name}")
        
        # 寻找注释文件
        annotation_files = list(bioproject_dir.glob(f"*{annotation_suffix}"))
        if not annotation_files:
            print(f"  No annotation file found in {bioproject_dir.name}")
            continue
        
        # 创建目标文件夹
        mic_dir = bioproject_dir / "Mic"
        mic_dir.mkdir(exist_ok=True)
        
        # 处理每个注释文件
        for ann_file in annotation_files:
            with open(ann_file, 'r') as f:
                headers = f.readline().strip().split('\t')
                
                try:
                    tax_col = headers.index("classification")
                    genome_col = headers.index("user_genome")
                except ValueError:
                    print(f"  Missing required columns in {ann_file.name}")
                    continue
                
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) < max(tax_col, genome_col)+1:
                        continue
                    
                    taxonomy = parts[tax_col]
                    genome_id = parts[genome_col]
                    
                    if target_taxonomy in taxonomy:
                        # 构建基因组文件路径
                        src_path = bioproject_dir / f"{genome_id}{genome_suffix}"
                        
                        # 检查文件是否存在
                        if not src_path.exists():
                            print(f"  Missing genome: {src_path.name}")
                            continue
                        
                        # 复制文件
                        dest_path = mic_dir / src_path.name
                        shutil.copy(src_path, dest_path)
                        print(f"  Copied: {src_path.name} -> Mic/")

if __name__ == "__main__":
    process_bioprojects()
