import re
import json
from tqdm import tqdm

global_index = 0

def parse_input(input_text,other_info_dict = {}):
    global global_index
    # 使用正则表达式匹配已回答的问题
    answered_pattern = re.compile('Headline:\s*"([^"]+)"\s*Now answer this question:\s*(.*?)\s*(Yes|No)', re.IGNORECASE)
    answered_matches = answered_pattern.findall(input_text)
    
    # 将input_text中已经被匹配过的部分删除
    input_text = re.sub(answered_pattern, '', input_text)
    
    # 使用正则表达式匹配未回答的问题
    unanswered_pattern = re.compile('Headline:\s*"([^"]+)"\s*Now answer this question:\s*(.*?)\s*(?=Headline:|$)', re.IGNORECASE)
    unanswered_matches = unanswered_pattern.findall(input_text)
    
    # 初始化结果列表
    result = []
    
    # 处理已回答的问题
    for i, (headline, question, answer) in enumerate(answered_matches):
        entry = {
            "id": str(global_index + 1),
            "Headline": headline.strip(),
            "Question": question.strip(),
            "Answer": answer.strip(),
            "Question Type": "Yes/No"
        }
        result.append(entry)
        global_index+=1

    # 处理未回答的问题
    # 注意：在id上继续累加
    unanswered_start_id = len(answered_matches) + 1
    for i, (headline, question) in enumerate(unanswered_matches):
        entry = {
            "id": str(global_index+1),
            "Headline": headline.strip(),
            "Question": question.strip(),
            "Answer": "",  # 答案留空
            "Question Type": "Yes/No"
        }
        result.append(entry)
        global_index+=1
    
    # 遍历result，将other_info_dict中的信息解包并添加
    for i in range(len(result)):
        result[i].update(other_info_dict)
    
    return result



def main():
    output_list = []
    # ./test.json
    with open('./test.json', 'r', encoding='utf-8') as f:
        input_list = json.load(f)
    print(len(input_list))
    for item in tqdm(input_list):
        other_info_dict = {}
        other_info_dict["item_id"] = item["id"]
        other_info_dict["gold_index"] = item["gold_index"]
        other_info_dict["class_id"] = item["class_id"]
        temp_list = parse_input(item["input"], other_info_dict)
        output_list.extend(temp_list)
    print(len(output_list))
    with open('output_regex.json', 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()