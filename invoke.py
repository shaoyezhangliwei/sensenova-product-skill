#!/usr/bin/env python3
"""
SenseNova U1 Product Skill Invoker

用法:
    python invoke.py --image /path/to/image.jpg --skill skill.json
"""

import argparse
import json
import sys
from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoProcessor

def load_skill(skill_path):
    with open(skill_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_prompt(skill_config):
    # 直接使用 prompt_template，模型会根据图片理解内容
    return skill_config["prompt_template"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="输入商品图片路径")
    parser.add_argument("--skill", default="skill.json", help="Skill JSON 配置文件")
    parser.add_argument("--model_path", default="sensenova/SenseNova-U1-8B-MoT", help="模型路径或HF名称")
    parser.add_argument("--max_new_tokens", type=int, default=512)
    args = parser.parse_args()

    print("加载模型中...")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        trust_remote_code=True,
        load_in_4bit=True,
        device_map="auto",
        torch_dtype=torch.float16
    )
    processor = AutoProcessor.from_pretrained(args.model_path, trust_remote_code=True)
    print("模型加载完成")

    skill_config = load_skill(args.skill)
    prompt = build_prompt(skill_config)
    image = Image.open(args.image).convert("RGB")

    inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=args.max_new_tokens)
    result = processor.decode(outputs[0], skip_special_tokens=True)

    # 尝试提取 JSON 部分（模型可能输出额外文字）
    try:
        # 找到第一个 { 和最后一个 }
        start = result.find('{')
        end = result.rfind('}') + 1
        if start != -1 and end != 0:
            json_part = result[start:end]
            data = json.loads(json_part)
            print("\n===== 提取的属性 =====")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            # 输出剩余部分作为文案
            remaining = result[end:].strip()
            if remaining:
                print("\n===== 生成的文案 =====")
                print(remaining)
        else:
            print("\n===== 完整输出 =====")
            print(result)
    except json.JSONDecodeError:
        print("\n===== 完整输出（非JSON格式）=====")
        print(result)

if __name__ == "__main__":
    main()