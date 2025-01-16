from Comparison import Comparison
import json
import tempfile
import os

def compare_jsonl_files(file1_path: str, file2_path: str):
    """比较两个 jsonl 文件中对应行的 JSON 对象相似度"""
    similarities = []
    
    with open(file1_path, 'r', encoding='utf-8') as f1, \
         open(file2_path, 'r', encoding='utf-8') as f2:
        
        for line_num, (line1, line2) in enumerate(zip(f1, f2), 1):
            # 解析每行的 JSON
            try:
                json1 = json.loads(line1.strip())
                json2 = json.loads(line2.strip())
                
                # 创建临时文件来存储当前行的 JSON
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp1, \
                     tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp2:
                    
                    json.dump(json1, temp1)
                    json.dump(json2, temp2)
                    temp1_path = temp1.name
                    temp2_path = temp2.name

                # 使用临时文件路径进行比较
                comp = Comparison(temp1_path, temp2_path)
                similarity = comp.similarity
                
                # 删除临时文件
                os.unlink(temp1_path)
                os.unlink(temp2_path)
                
                print(f"第 {line_num} 行的相似度: {similarity:.2%}")
                similarities.append(similarity)
                
            except json.JSONDecodeError as e:
                print(f"第 {line_num} 行解析出错: {str(e)}")
            except Exception as e:
                print(f"第 {line_num} 行比较出错: {str(e)}")
    
    if similarities:
        avg_similarity = sum(similarities) / len(similarities)
        print("\n" + "=" * 50)
        print(f"平均相似度: {avg_similarity:.2%}")
        print("=" * 50)
    else:
        print("\n没有成功比较任何行")

if __name__ == "__main__":
    # 使用示例
    file1 = "/Users/kehaochen/Desktop/Work/MatirxSearch/resume_search_poc/benchmark/dataset/synthesized/resumes_0.jsonl"
    file2 = "/Users/kehaochen/Desktop/Work/MatirxSearch/resume_search_poc/benchmark/dataset/parsed/parsed_resumes.jsonl"
    compare_jsonl_files(file1, file2)
    # 单个文件比较示例
    # file1 = "example1.json"
    # file2 = "example2.json"
    # comp = Comparison(file1, file2)
    # print(comp.similarity)

