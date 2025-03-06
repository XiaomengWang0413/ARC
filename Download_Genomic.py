from Bio import Entrez
import time
import os
Entrez.email = "1130103220@qq.com"  # 替换为您的邮箱
Entrez.api_key = "c1a10d1e19cbd1ac69ed472fc41556775708"          # 在NCBI申请API密钥
# 定义关键词集合（不区分大小写）
target_keywords = {
    "micrarchaeota",  # 覆盖大小写变体
    "micrarchaeia",
    "micrarchaeaceae"
}
search_term = "Micrarchaeota[Organism] AND latest[filter]"
db_type = "assembly"
output_dir = "./genomes/"
os.makedirs(output_dir, exist_ok=True)
print("正在搜索Micrarchaeota基因组...")
search_handle = Entrez.esearch(db=db_type, term=search_term, retmax=1000)
search_results = Entrez.read(search_handle)
search_handle.close()
id_list = search_results["IdList"]
count = int(search_results["Count"])
print(f"找到{count}条记录，开始关键词筛选...")
def get_bioproject(assembly_id):
    """通过Assembly ID获取对应的Bioproject ID"""
    try:
        handle = Entrez.elink(dbfrom="assembly", db="bioproject", id=assembly_id)
        record = Entrez.read(handle)
        handle.close()
        
        if record and record[0].get("LinkSetDb"):
            return record[0]["LinkSetDb"][0]["Link"][0]["Id"]
        return "unknown_bioproject"
    except Exception as e:
        print(f"获取Bioproject失败: {assembly_id} - {str(e)}")
        return "error_bioproject"
valid_count = 0
for i, assembly_id in enumerate(id_list):
    try:
        # 获取Assembly信息
        summary_handle = Entrez.esummary(db=db_type, id=assembly_id)
        summary = Entrez.read(summary_handle)
        summary_handle.close()
        
        # 提取信息
        doc_summary = summary["DocumentSummarySet"]["DocumentSummary"][0]
        organism = doc_summary.get("Organism", "").strip().lower()  # 转为小写
        ftp_path = doc_summary["FtpPath_GenBank"]
        
        # 关键词筛选（不区分大小写）
        if not any(keyword in organism for keyword in target_keywords):
            print(f"跳过({i+1}/{count}): {organism.title()} (不包含关键词)")
            continue
            
        # API请求间隔
        time.sleep(0.34) if Entrez.api_key else time.sleep(1)
        
        # 获取Bioproject ID
        bioproject_id = get_bioproject(assembly_id)
        project_dir = os.path.join(output_dir, bioproject_id)
        os.makedirs(project_dir, exist_ok=True)
        
        # 生成下载路径
        filename = ftp_path.split("/")[-1] + "_genomic.fna.gz"
        download_url = f"{ftp_path}/{filename}"
        
        # 二次请求间隔
        time.sleep(0.34) if Entrez.api_key else time.sleep(1)
        
        # 下载文件
        valid_count += 1
        print(f"正在下载 ({valid_count}): {filename}")
        print(f"分类信息: {organism.title()}")
        print(f"所属Bioproject: {bioproject_id}")
        os.system(f"wget -q -P {project_dir} {download_url}")
        
    except Exception as e:
        print(f"处理失败: {assembly_id} - {str(e)}")
print(f"\n下载完成，有效基因组数量: {valid_count}/{count}")
print("请检查输出目录:", os.path.abspath(output_dir))
