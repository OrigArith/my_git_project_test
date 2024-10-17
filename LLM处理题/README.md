# 这是一个对AdaptLLM数据集的子集的提取测试

## 正则化方法

共提取10254对问答对

具体看代码process_regex.py

在原需求的基础上添加了关于问答的来源信息，示例如下:

```json
{
        "id": "1",
        "Headline": "Gold falls to Rs 30,800; silver down at Rs 41,200 per kg",
        "Question": "Does the news headline talk about price in the past?",
        "Answer": "Yes",
        "Question Type": "Yes/No",
        "item_id": 0,
        "gold_index": 1,
        "class_id": 0
    }
```

处理20k条数据使用时间小于1s（大致使用了0.6s）

## LLM方法

使用deepseek的api，具体代码和prompt见process_llm.py

未使用多线程处理10条数据用时3:39

使用多线程时处理10条数据用时23s