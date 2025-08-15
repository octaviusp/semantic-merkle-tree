# 🌳 Semantic Merkle Tree (SMT)

<div align="center">

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)

**A meaning-aware Merkle tree that understands semantic changes, not just byte-level differences**

</div>

---
## 🎯 THE CORE IDEA

**GENERALIZATION**: The core idea of SMT that you need to understand is, how we can avoid recomputation of process if something didn't change the latent-meaning? Particularly, in the code example, we use a merkle tree to hash a system-folder tree, and apply semantic integrity. But this similar concept could be applied to many ideas, so please, don't limit to this use case and share what you can create with this first-principle idea of semantic integrity!

**Mathematical Explanation**

For a more technical perspective, here's how semantic integrity generalizes the classic Merkle tree:

Traditional Merkle trees use hash functions that are **discrete** and ideally **injective**—meaning each unique input produces a unique output. In contrast, a Semantic Merkle Tree (SMT) introduces *approximate* or *fuzzy* hashing: different inputs with similar *meaning* can map to the same output. Thus, the SMT hash function is not strictly injective; multiple \( X \) can map to the same \( Y \) if their meanings are close enough.

Let $\varepsilon$ (epsilon) be the semantic similarity threshold, with $\varepsilon \in [0, 1]$:

- If $\varepsilon = 1$, we recover the classic Merkle tree: **any** change is significant.
- If $\varepsilon < 1$, we allow for *semantic equivalence*: only changes that alter the meaning beyond the threshold are considered significant.

**Formally:**

Given two versions of content, $\text{old\_content}$ and $\text{new\_content}$, we compute their semantic difference:

$$
a = \text{semantic\_difference}\!\left(\text{old\_content},\, \text{new\_content}\right)
$$

where $a \in [0, 1]$ (for example, $a = 1 - \cos(\theta)$ if using cosine similarity).

The update rule is:

$$
\text{If } a < \varepsilon:\ \text{do not recompute hash (treat as unchanged)}
$$
$$
\text{Else:}\ \text{recompute hash (treat as changed)}
$$

> **Note:** GitHub now supports native math rendering in Markdown using `$...$` for inline and `$$...$$` for block math, so the above will render correctly on GitHub ([see announcement](https://github.blog/news-insights/product-news/math-support-in-markdown/)).

This approach allows the Merkle tree to ignore changes that do not alter the *latent meaning* of the content, thus reducing unnecessary recomputation and propagation.

| **Aspect** | **In One Sentence** |
|------------|---------------------|
| **What it is** | A hierarchical map of embeddings (latent-meaning vectors) arranged like a Merkle tree, where each node also stores a conventional hash |
| **What it does** | After an edit, it decides whether the node's meaning moved beyond a threshold δ; if not, it leaves the original hash and cached documentation untouched, preventing needless upstream work |
| **What problem it solves** | Eliminates expensive or time-wasting reactions to purely cosmetic changes (typos, whitespace, re-ordering) while still catching genuine semantic drift |

---

## 🎯 The Problem

Traditional Merkle trees and file monitoring systems treat **any** change as significant:

(In this following example, just we add ''.'' in the end.)
```diff
- The quick brown fox jumps over the lazy dog
+ The quick brown fox jumps over the lazy dog.
```

☝️ **One period added** → Entire CI/CD pipeline triggered → Thousands of dollars in compute costs

**Semantic Merkle Tree says:** *"Wait, the meaning didn't change!"*

---

## 💡 How It Works (This particular case is SMT applied to file-system tree, but could be generalized!)

### 🧠 The Magic Behind SMT

1. **📝 Content Analysis**: Each file is converted into a semantic embedding vector using AI models
2. **🔍 Similarity Check**: When files change, SMT compares the *meaning* using cosine similarity
3. **⚡ Smart Updates**: Only propagates changes when semantic similarity drops below threshold `θ` (default: 0.70)
4. **🌲 Tree Structure**: Maintains traditional Merkle tree benefits while adding semantic awareness

---


## 🛠️ Installation

### Prerequisites
- **Python 3.12+**
- **Poetry** (recommended) or pip

### Quick Install

```bash
# Clone the repository
git clone https://github.com/octaviusp/semantic-merkle-tree.git
cd semantic-merkle-tree

# Install dependencies
poetry install
```

### Dependencies
- `sentence-transformers` - AI embeddings
- `numpy` - Vector operations
- `tqdm` - Progress bars
---

## 🚀 Quick Start

### 1️⃣ Build Your First SMT

```bash
python main.py build example_folder/
```

**Output:**
```
building: 100%|████████████| 2/2 [00:01<00:00,  1.23it/s]
Build complete. root_hash = a1b2c3d4e5f6...
```

### 2️⃣ Make Some Changes

Edit a file in `example_folder/`:

```bash
echo "I was running down the street" > example_folder/1.txt
```

### 3️⃣ Verify Semantic Changes

```bash
python main.py verify example_folder/
```

**Output:**
```
verifying: 100%|████████████| 2/2 [00:01<00:00,  1.45it/s]
Cosine similarity for 'example_folder/1.txt': 0.892156
No semantic changes.
root_hash = a1b2c3d4e5f6...
```

🎉 **Notice**: Despite the text change ("in" → "down"), the similarity (0.89) is above our threshold (0.70), so SMT considers it semantically equivalent!

---

## 📊 Real-World Use Cases

### 🔄 CI/CD Pipeline Optimization
**💰 Cost Savings**: Skip expensive operations when only formatting changes!

### 📚 LLM Documentation Generation
<summary><strong>🤖 Smart Documentation Updates</strong></summary>

**📈 Results**: 70-90% reduction in LLM API costs for documentation workflows!

</details>

### 🏢 Enterprise Knowledge Management

<details>
<summary><strong>📋 Policy Document Tracking</strong></summary>

| **Scenario** | **Traditional System** | **With SMT** |
|--------------|------------------------|---------------|
| Typo fix in policy | 🚨 Alert sent to legal team | ✅ No alert (semantic similarity: 0.98) |
| Formatting change | 🚨 Full review process triggered | ✅ Ignored (cosmetic change) |
| Actual policy change | 🚨 Alert sent | 🚨 Alert sent (semantic similarity: 0.45) |

**⏱️ Time Saved**: Legal teams focus on substance, not formatting!

</details>

---

## ⚙️ Configuration

### 🎛️ Adjusting Sensitivity

The semantic threshold `θ` (theta) controls sensitivity:

```python
# In main.py
THETA = 0.70  # Default: 70% similarity required

# More sensitive (catches smaller changes)
THETA = 0.85  # 85% similarity required

# Less sensitive (ignores more changes)
THETA = 0.50  # 50% similarity required
```

### 🧠 Embedding Models

SMT uses `all-MiniLM-L6-v2` by default, but you can swap models:

```python
# Faster, smaller model
MODEL = SentenceTransformer("all-MiniLM-L12-v2")

# More accurate, larger model
MODEL = SentenceTransformer("all-mpnet-base-v2")

# Multilingual support
MODEL = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
```

---

## IMPROVEMENTS AND LIMITATIONS

1) False detections:
Regardless of being a good technique for some use-cases, there are open challenge problems, like, what would happen if you have false positives, you need to use a extremely well trained semantic criteria for critic use-cases, we recommend to use state-of-the-art embedding models to lowest probability of errors. 

2) Epsilon search:
Is very hard to search a perfect epsilon threshold for every application, so for your use case, you need to try-&-error how to finetune this hyperparameter to seek the best trade-off.


---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Sentence Transformers** team for simple and fast embedding models
- **Merkle Tree** inventors for the foundational data structure
- **Open source community** for inspiration and feedback

---

## 📞 Support

- **📧 Email**: octaviopavon7@gmail.com
- **🐛 Issues**: [GitHub Issues](https://github.com/octaviusp/semantic-merkle-tree/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/octaviusp/semantic-merkle-tree/discussions)

---

<div align="center">

**⭐ Star this repo if SMT helped you save compute costs! ⭐**

Made with ❤️ by [octaviopavon](https://github.com/octaviusp)

</div> 
