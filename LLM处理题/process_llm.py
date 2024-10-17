
import os
from openai import OpenAI
import re
from tqdm import tqdm
import json
import time

# 初始化OpenAI客户端
client = OpenAI(api_key="api-key", base_url="https://api.deepseek.com")


sys_prompt = """
### 任务描述
- **Task Description:** Each entry in the `input` column contains multiple "Yes" or "No" questions alongside their respective answers. Your task is to:

  - Develop a Python script to parse and separate each question and its answer from the entry.
  - Save each question-answer pair in a structured JSON format as follows:
    ```json
    {
      "id": "<unique_identifier>",
      "Headline":"<headline_text>",
      "Question": "<question_text>",
      "Answer": "<answer_text>"
    }
    ```

  - You are encouraged to introduce additional attributes if needed to preserve the integrity and completeness of the information. Adding relevant tag information is strongly recommended.
- **Automation Requirement:** The task must be completed using Python. Manual editing or data manipulation is strictly prohibited. Your script should efficiently handle variations in data format within the column.

### 输入输出文本示例
#### 示例输入
Headline: "Gold falls to Rs 30,800; silver down at Rs 41,200 per kg" Now answer this question: Does the news headline talk about price in the past? Yes Headline: "gold futures add to gains after adp data" Now answer this question: Does the news headline talk about price? Yes Headline: "Gold holds on to modest loss after data" Now answer this question: Does the news headline talk about price in the future? No Headline: "spot gold quoted at $417.50, down 20c from new york" Now answer this question: Does the news headline talk about a general event (apart from prices) in the past? No Headline: "gold hits new record high at $1,036.20 an ounce" Now answer this question: Does the news headline compare gold with any other asset? No Headline: "gold may hit rs 31,500, but pullback rally may not sustain for long: experts" Now answer this question: Does the news headline talk about price?
#### 示例输出
[
    {
        "id": "1",
        "Headline": "Gold falls to Rs 30,800; silver down at Rs 41,200 per kg",
        "Question": "Does the news headline talk about price in the past?",
        "Answer": "Yes",
        "Question Type": "Yes/No",
    },
    {
        "id": "2",
        "Headline": "gold futures add to gains after adp data",
        "Question": "Does the news headline talk about price?",
        "Answer": "Yes",
        "Question Type": "Yes/No",
    },
    {
        "id": "3",
        "Headline": "Gold holds on to modest loss after data",
        "Question": "Does the news headline talk about price in the future?",
        "Answer": "No",
        "Question Type": "Yes/No",
    },
    {
        "id": "4",
        "Headline": "spot gold quoted at $417.50, down 20c from new york",
        "Question": "Does the news headline talk about a general event (apart from prices) in the past?",
        "Answer": "No",
        "Question Type": "Yes/No",
    },
    {
        "id": "5",
        "Headline": "gold hits new record high at $1,036.20 an ounce",
        "Question": "Does the news headline compare gold with any other asset?",
        "Answer": "No",
        "Question Type": "Yes/No",
    },
    {
        "id": "6",
        "Headline": "gold may hit rs 31,500, but pullback rally may not sustain for long: experts",
        "Question": "Does the news headline talk about price?",
        "Answer": "",
        "Question Type": "Yes/No",
    }]


###指令
请直接返回输出的文本
"""


def process_text(text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"{text}"}
        ],
        stream=False
    )
    return response.choices[0].message.content

def main():
    output_list = []
    # ./test.json
    with open('./test.json', 'r', encoding='utf-8') as f:
        input_list = json.load(f)
    print(len(input_list))
    # 计算循环运行时间
    # start_time = time.time()
    for item in tqdm(input_list[:10]):
        other_info_dict = {}
        other_info_dict["item_id"] = item["id"]
        other_info_dict["gold_index"] = item["gold_index"]
        other_info_dict["class_id"] = item["class_id"]
        # temp_list = parse_input(item["input"], other_info_dict)
        # output_list.extend(temp_list)
        try:
            out_str = process_text(item["input"]).strip("```json").strip("```")
            out_list = eval(out_str)
            for i in range(len(out_list)):
                out_list[i].update(other_info_dict)
            output_list.extend(out_list)
        except:
            print("error in index ", item["id"])
            continue
        # end_time = time.time()
        # print("time cost:", end_time - start_time)
        
    print(len(output_list))
    with open('output_llm.json', 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()