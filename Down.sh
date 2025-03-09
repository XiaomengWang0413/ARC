#!/bin/bash

# 定义帮助信息函数
usage() {
    echo "用法: \$0 [-h] -p <BioProject ID> [-o 输出目录]"
    echo "选项:"
    echo "  -h           显示此帮助信息"
    echo "  -p PROJECT   指定NCBI BioProject ID (例如: PRJNA777757)"
    echo "  -o OUTPUT    指定下载文件输出目录 (默认为当前目录)"
    echo ""
    echo "示例:"
    echo "  \$0 -p PRJNA777757 -o ./genome_data"
    exit 0
}

# 初始化变量
project_id=""
output_dir="."

# 解析命令行参数
while getopts ":hp:o:" opt; do
    case $opt in
        h)
            usage
            ;;
        p)
            project_id="$OPTARG"
            ;;
        o)
            output_dir="$OPTARG"
            ;;
        \?)
            echo "错误: 无效选项 -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "错误: 选项 -$OPTARG 需要参数" >&2
            exit 1
            ;;
    esac
done

# 检查必要参数
if [[ -z "$project_id" ]]; then
    echo "错误: 必须使用 -p 指定 BioProject ID" >&2
    exit 1
fi

# 创建输出目录
mkdir -p "$output_dir" || exit 1

# 主下载流程
esearch -db assembly -query "${project_id}[BioProject]" |
efetch -format docsum |
xtract -pattern DocumentSummary -element FtpPath_GenBank |
while read -r ftp_path; do
    if [[ -n "$ftp_path" ]]; then
        # 从FTP路径构建文件名
        fna_file="${ftp_path}/$(basename "${ftp_path}")_genomic.fna.gz"
        filename=$(basename "${fna_file}")
        
        echo "下载: $filename"
        
        # 下载到指定目录并解压
        wget -nc -P "$output_dir" "$fna_file"
        gunzip -f "${output_dir}/${filename}"
    fi
done

echo "下载完成！文件保存在: ${output_dir}"
