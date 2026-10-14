# GerdQ高原肥胖GERD研究：统计分析包（供逐项核对）

本目录包含修改稿全部统计分析的输入数据、代码和输出图表。修改稿（`../02_修改稿全文_GerdQ高原肥胖GERD.docx`）中的表1~表7和图1~图5都由这里的代码直接生成。

## 一、数据来源与原则

- **唯一输入**：[`inputs/summary_data.json`](inputs/summary_data.json)。逐项录入原稿PDF已报告的汇总数据，每组数据的`source`字段注明原稿出处（表号或节号）。
- **没有原始个体数据**：全部分析都基于汇总数据，没有模拟或虚构任何个体数据。
- **可精确反推的例数**：例如各GerdQ分值的GERD阳性和阴性例数、各诊断路径的改善例数，都由原稿百分比唯一反推。每一项反推结果都与原稿其他报告值交叉核对，见第三部分。
- **无法复算的内容**：计量资料的组间检验（*H*、*U*值）、Spearman相关和Logistic回归的拟合本身都需要原始数据，因此照录原稿报告值。表注中均已说明。

## 二、运行方法

```bash
pip install -r requirements.txt     # numpy、scipy、matplotlib、openpyxl、pillow
cd code
python3 run_all.py                   # 依次运行01→02→03→04，约10秒
```

第4步生成Word汇总，需要另外安装`pypandoc`和`python-docx`；如果没有安装，会自动跳过。

## 三、代码文件（按运行顺序）

| 文件 | 作用 | 输出 |
|---|---|---|
| [`code/common.py`](code/common.py) | 公共函数，包括Wilson置信区间、χ²检验、Woolf法*OR*、Cochran-Armitage趋势检验、Cohen κ、分组数据AUC与DeLong标准误、Hanley-McNeil标准误、似然比、E值和表格写出 | — |
| [`code/01_reconstruct_check.py`](code/01_reconstruct_check.py) | 由原稿百分比反推各分值和各诊断路径的例数，并逐项核查原稿报告值，共121项 | `output/checks/一致性核查.csv`、`output/checks/reconstructed.json` |
| [`code/02_tables.py`](code/02_tables.py) | 生成表1~表7、附表S1~S6，以及Excel汇总 | `output/tables/*.csv`、`*.md`、`统计表汇总.xlsx` |
| [`code/03_figures.py`](code/03_figures.py) | 生成图1~图5，每幅图有PNG、TIFF（均为300 dpi）和PDF（矢量）三种格式 | `output/figures/` |
| [`code/04_export_docx.py`](code/04_export_docx.py) | 将全部图表汇总为一个Word文件 | `../06_统计图表汇总.docx` |
| [`code/run_all.py`](code/run_all.py) | 一键运行以上全部步骤 | — |

## 四、输出文件

### 4.1　一致性核查

[`output/checks/一致性核查.csv`](output/checks/一致性核查.csv)：列出每个核查项目、原稿报告值、重新计算值、结论和计算方法。121项全部一致。

### 4.2　表格

每张表都有CSV（可用Excel直接打开）和Markdown两种格式。全部表格另汇总在[`output/tables/统计表汇总.xlsx`](output/tables/统计表汇总.xlsx)中，每张表一个工作表，并附一致性核查表。

| 表号 | 内容 | 数据性质 |
|---|---|---|
| 表1 | 不同肥胖程度组基线资料 | χ²值和*P*值重新计算；计量资料照录原稿 |
| 表2 | 基线GerdQ条目得分分布 | 百分比、均数和标准差由频数重新计算；*r*ₛ照录原稿 |
| 表3 | 不同截断值的诊断效能 | 全部重新计算，新增灵敏度和特异度的95%CI |
| 表4 | 分层似然比及验后概率 | 新增分析 |
| 表5 | 治疗前后评分及体重变化 | Wilson法95%CI重新计算；改善者下降值为推算值 |
| 表6 | 症状改善组与未改善组比较 | χ²值和*P*值重新计算；计量资料照录原稿 |
| 表7 | 多因素Logistic回归 | Wald χ²、*OR*、95%CI和*P*值由*β*和*SE*重新计算 |
| 附表S1 | 重建的GerdQ总分×GERD交叉分布 | 反推例数、逐分似然比、趋势检验、AUC |
| 附表S2 | 不同诊断路径的GerdQ≥10分比例与疗效 | 新增分析 |
| 附表S3 | 单因素与多因素*OR*及E值 | 新增分析 |
| 附表S4 | PPI试验与4周症状改善的一致性 | 新增分析 |
| 附表S5 | 原列线图模型评价指标重估 | 新增分析 |
| 附表S6 | 后续研究样本量估算 | 新增分析 |

### 4.3　图件

所有图件都在`output/figures/`中，每幅图有`.png`、`.tif`和`.pdf`三种格式。

| 图号 | 内容 | 数据依据 |
|---|---|---|
| 图1 | 基线GerdQ总分分布（A）、条目得分构成（B）、条目-总分相关（C） | 附表S1；原稿表2 |
| 图2 | 各肥胖组GerdQ总分中位数（*Q*₁，*Q*₃）（A）；各组基线4GerdQ、下降值和减重幅度（B） | 原稿表1、2.3节、2.5节 |
| 图3 | GERD复合诊断的ROC曲线（A）和分层似然比（B） | 表3、表4 |
| 图4 | 治疗前后评分（A）、不同诊断路径的症状改善率（B）、PPI试验与4周疗效的一致性（C） | 表5、附表S2、附表S4 |
| 图5 | 症状改善相关因素的*OR*森林图 | 附表S3 |

原稿中有两幅散点图：BMI与GerdQ总分、减重幅度与4GerdQ下降值。这两幅图都需要个体数据，无法准确重绘，修改稿未纳入。如果找到原始数据，可补充到`inputs/`中，再扩展`03_figures.py`重新作图。

## 五、核对建议

1. 用原稿PDF逐项对照[`inputs/summary_data.json`](inputs/summary_data.json)，确认录入无误。
2. 打开`一致性核查.csv`，查看每个反推值与原稿报告值的对比。
3. 用Excel打开各表的CSV或`统计表汇总.xlsx`，与修改稿中的表格逐格对照。
4. 如果发现录入错误，修改JSON后重新运行`python3 run_all.py`，然后在`submission/gerdq_shiyong_yixue/`目录下运行以下命令，即可同步更新修改稿：

```bash
cd tools && python3 build.py manuscript_src.md ../02_修改稿全文_GerdQ高原肥胖GERD.md && cd ..
python3 tools/md2docx.py 02_修改稿全文_GerdQ高原肥胖GERD.md 02_修改稿全文_GerdQ高原肥胖GERD.docx
```
