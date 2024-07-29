import os
import chardet
import csv
from openai import OpenAI
from typing import Dict, List

# 创建OpenAI客户端，替换为自己的base_url、api_key
client = OpenAI(
    base_url="https://api.openai-proxy.live/v1",
    api_key="sk-YCxxx"
)

def get_files_recursion_from_dir(path: str) -> list:
    """
    从指定的文件夹中使用递归的方式，获取全部的文件列表
    @param path: 被判断的文件夹
    @return: 包含全部的文件，如果目录不存在或者无文件就返回一个空list
    """
    file_list = []
    if os.path.exists(path):
        for f in os.listdir(path):
            new_path = os.path.join(path, f)
            if os.path.isdir(new_path):
                # 进入这里，表明这个目录是文件夹不是文件
                file_list += get_files_recursion_from_dir(new_path)
            else:
                file_list.append(new_path)
    else:
        print(f"指定的目录{path}，不存在")
        return []

    return file_list

def read_string_with_path(path: str) -> str:
    """
    读取文本文件的内容
    @param path: 文件路径
    @return: 文本文件内容的字符串
    """
    with open(path, 'rb') as check_encoding_f:
        data = check_encoding_f.read()
        encoding = chardet.detect(data)['encoding']

    if encoding == 'GB2312':
        encoding = 'GBK'
    with open(path, "r", encoding=encoding) as read_f:
        text_content = read_f.read()
    return text_content

def check_text_with_openai(text: str) -> Dict[str, str]:
    """
    使用OpenAI API检查文本是否有错误
    @param text: 要检查的文本
    @return: 包含检查结果和原因的字典
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个中文语法和用词专家。你需要检查给定的中文文本是否有任何错误，包括语法、用词、标点等方面。"},
                {"role": "user", "content": f'请检查以下中文文本是否有任何错误：\n\n{text}\n\n如果有错误，请说明原因；如果没有错误，请直接回复"正确"。'}
            ]
        )
        
        result = response.choices[0].message.content.strip()
        
        if "正确" in result and len(result) < 10:  # 允许一些小的变化，比如"完全正确"
            return {"correct": "true", "reason": ""}
        else:
            return {"correct": "false", "reason": result}
    except Exception as e:
        return {"correct": "error", "reason": f"API调用出错：{str(e)}"}

def process_files(directory: str, output_file: str):
    """
    处理指定目录下的所有.txt文件，检查文本错误，并将结果输出到CSV文件
    @param directory: 要处理的目录
    @param output_file: 输出的CSV文件路径
    """
    files = get_files_recursion_from_dir(directory)
    txt_files = [f for f in files if f.lower().endswith('.txt')]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['文本路径', '检查结果', '错误原因', '文本内容']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for file_path in txt_files:
            content = read_string_with_path(file_path)
            result = check_text_with_openai(content)
            
            writer.writerow({
                '文本路径': file_path,
                '检查结果': '正确' if result['correct'] == 'true' else '错误',
                '错误原因': result['reason'],
                '文本内容': content
            })
            
            print(f"处理完成: {file_path}")

if __name__ == "__main__":
    input_directory = input("请输入要处理的文件夹路径: ")
    output_csv = input("请输入输出CSV文件的路径: ")
    
    process_files(input_directory, output_csv)
    print(f"处理完成，结果已保存到 {output_csv}")