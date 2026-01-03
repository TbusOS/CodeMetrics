# 💰 COCOMO 模型计算原理

## 📖 简介

**COCOMO** (Constructive Cost Model，构造性成本模型) 是由 **Barry Boehm** 于 1981 年提出的软件成本估算模型。该模型基于对 63 个软件项目的历史数据分析，建立了代码规模与开发工作量之间的数学关系。

CodeStats 工具采用 **Basic COCOMO** 模型进行成本估算。

---

## 🧮 核心公式

### 1. 工作量估算 (Effort)

```
E = a × (KLOC)^b
```

| 符号 | 含义 |
|------|------|
| **E** | 工作量，单位：人月 (Person-Months) |
| **KLOC** | 代码规模，千行代码 (Kilo Lines of Code) |
| **a, b** | 项目类型系数 |

### 2. 开发时间估算 (Duration)

```
D = c × (E)^d
```

| 符号 | 含义 |
|------|------|
| **D** | 开发时间，单位：月 |
| **E** | 工作量（人月） |
| **c, d** | 项目类型系数 |

### 3. 团队规模估算 (Team Size)

```
N = E / D
```

| 符号 | 含义 |
|------|------|
| **N** | 建议团队人数 |
| **E** | 工作量（人月） |
| **D** | 开发时间（月） |

---

## 📊 项目类型与系数

COCOMO 定义了三种项目类型，每种类型有不同的系数：

| 项目类型 | a | b | c | d | 描述 |
|----------|-----|------|------|------|------|
| **Organic** (简单) | 2.4 | 1.05 | 2.5 | 0.38 | 小团队，熟悉的技术栈，低复杂度 |
| **Semi-detached** (中等) | 3.0 | 1.12 | 2.5 | 0.35 | 中型团队，混合经验，中等复杂度 |
| **Embedded** (复杂) | 3.6 | 1.20 | 2.5 | 0.32 | 嵌入式/驱动/实时系统，高复杂度 |

### 项目类型选择指南

#### 🟢 Organic (简单项目)
- 小型团队（< 10 人）
- 团队对应用领域和技术非常熟悉
- 灵活的需求，宽松的约束
- 示例：内部工具、脚本、小型应用

#### 🟡 Semi-detached (中等项目)
- 中型团队（10-50 人）
- 团队有混合的经验水平
- 需求相对稳定，有一定约束
- 示例：Web 应用、企业系统、通用软件

#### 🔴 Embedded (复杂项目)
- 严格的硬件/软件约束
- 实时性能要求
- 高可靠性要求
- 示例：设备驱动、嵌入式系统、航空航天软件、医疗设备

---

## 📝 计算示例

假设我们有一个 **嵌入式驱动项目**，代码量为 **9,132 行**：

### Step 1: 计算 KLOC
```
KLOC = 9132 / 1000 = 9.132
```

### Step 2: 选择项目类型系数
项目类型: **Embedded**
- a = 3.6
- b = 1.20
- c = 2.5
- d = 0.32

### Step 3: 计算工作量 (人月)
```
E = a × (KLOC)^b
E = 3.6 × (9.132)^1.20
E = 3.6 × 14.22
E = 51.2 人月
```

### Step 4: 计算开发时间 (月)
```
D = c × (E)^d
D = 2.5 × (51.2)^0.32
D = 2.5 × 3.52
D = 8.8 个月
```

### Step 5: 计算团队规模
```
N = E / D
N = 51.2 / 8.8
N = 5.8 人
```

### Step 6: 计算成本
```
成本 (USD) = E × 人月成本
成本 (USD) = 51.2 × $5,000
成本 (USD) = $256,000

成本 (CNY) = E × 人月成本
成本 (CNY) = 51.2 × ¥30,000
成本 (CNY) = ¥1,536,000
```

---

## 🔧 CodeStats 中的实现

### 代码实现

```python
# COCOMO 系数表
COCOMO_PARAMS = {
    'organic':       {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
    'semi-detached': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
    'embedded':      {'a': 3.6, 'b': 1.20, 'c': 2.5, 'd': 0.32},
}

def calculate_cocomo(total_code_lines: int, project_type: str, config: dict) -> dict:
    """计算 COCOMO 成本估算"""
    
    # 转换为 KLOC (千行代码)
    kloc = total_code_lines / 1000.0
    
    # 获取项目类型系数
    params = COCOMO_PARAMS.get(project_type, COCOMO_PARAMS['semi-detached'])
    a, b, c, d = params['a'], params['b'], params['c'], params['d']
    
    # 计算工作量 (人月)
    effort = a * (kloc ** b)
    
    # 计算开发时间 (月)
    duration = c * (effort ** d)
    
    # 计算团队规模
    team_size = effort / duration if duration > 0 else 0
    
    # 计算成本
    cost_per_month_usd = config.get('cocomo', {}).get('cost_per_month_usd', 5000)
    cost_per_month_cny = config.get('cocomo', {}).get('cost_per_month_cny', 30000)
    
    return {
        'kloc': kloc,
        'effort': effort,           # 人月
        'duration': duration,       # 月
        'team_size': team_size,     # 人
        'cost_usd': effort * cost_per_month_usd,
        'cost_cny': effort * cost_per_month_cny,
        'project_type': project_type
    }
```

### 人月成本配置

可在 `config.json` 中自定义人月成本：

```json
{
  "cocomo": {
    "cost_per_month_usd": 5000,
    "cost_per_month_cny": 30000
  }
}
```

---

## 📈 不同项目类型的对比

以 10 KLOC 为例，三种项目类型的估算差异：

| 项目类型 | 工作量 (人月) | 开发时间 (月) | 团队规模 |
|----------|---------------|---------------|----------|
| Organic | 26.9 | 8.4 | 3.2 |
| Semi-detached | 39.5 | 8.0 | 4.9 |
| Embedded | 57.1 | 8.8 | 6.5 |

可以看到：
- **Embedded** 项目需要最多的工作量（是 Organic 的 2.1 倍）
- 开发时间差异较小（约 0.5 个月）
- **Embedded** 项目需要更大的团队

---

## ⚠️ 模型局限性

COCOMO 是一个经验模型，存在以下局限性：

1. **基于历史数据** - 基于 1981 年前的项目，现代工具和方法可能影响准确性
2. **仅考虑代码量** - 不考虑代码质量、复用、技术难度等因素
3. **估算范围** - 最适合 2K-512K 行代码的项目
4. **行业差异** - 不同行业、公司的生产力差异较大

### 建议

- 将 COCOMO 估算作为 **参考值**，而非精确预测
- 结合团队实际经验进行调整
- 对于小项目（<2K 行）可能高估
- 对于大项目（>500K 行）需要使用更复杂的模型

---

## 📚 参考文献

1. Boehm, B. W. (1981). *Software Engineering Economics*. Prentice-Hall.
2. Boehm, B. W. et al. (2000). *Software Cost Estimation with COCOMO II*. Prentice-Hall.

---

## 🔗 相关资源

- [COCOMO II Official Site](http://csse.usc.edu/csse/research/COCOMOII/)
- [Wikipedia: COCOMO](https://en.wikipedia.org/wiki/COCOMO)

