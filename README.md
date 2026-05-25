# SenseNova U1 商品图智能解读 Skill

基于商汤开源 **SenseNova-U1-8B-MoT** 统一模型开发的自定义 Skill，实现：
- 从商品图片中自动提取 **品类、颜色、材质、风格** 等属性（理解）
- 基于属性生成 3 句不同角度的营销种草文案（生成）

## 特点

- **统一模型**：理解与生成共享同一潜在空间，协同增强
- **零训练成本**：通过 Skill 定义快速适配业务场景
- **开箱即用**：提供完整调用脚本，支持 4-bit 量化（单卡 24GB 可运行）

## 前置要求

- Python 3.10+
- 至少 24GB 显存的 GPU（或使用 CPU，但较慢）
- Hugging Face 账号（用于下载模型）

## 安装

```bash
git clone https://github.com/yourusername/sensenova-product-skill.git
cd sensenova-product-skill
pip install -r requirements.txt
