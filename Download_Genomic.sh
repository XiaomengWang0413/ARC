#!/bin/bash
# 安装 Entrez Direct 工具（若未安装）
# 从 https://www.ncbi.nlm.nih.gov/books/NBK179288/ 下载 edirect 并添加到 PATH
# 搜索并下载基因组文件
esearch -db assembly -query "PRJNA777757[BioProject]" |
efetch -format docsum |
xtract -pattern DocumentSummary -element FtpPath_GenBank |
while read -r ftp_path; do
    if [[ -n "$ftp_path" ]]; then
        dir_path="${ftp_path}/"
        fna_file="${dir_path}$(basename ${ftp_path})_genomic.fna.gz"
        echo "Downloading: $fna_file"
        wget -nc "${fna_file}"
        gunzip -f "$(basename ${fna_file})"  # 解压为 .fna
    fi
done

