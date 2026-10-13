# Supplementary Information

**Pathology foundation models for rare disease diagnosis: data-efficient adaptation, cross-site robustness and the evidence gap**

Reference numbers in this document refer to the reference list of the main manuscript.

---

## Supplementary Methods: literature search and selection

### Databases and period

PubMed/MEDLINE, Web of Science Core Collection and arXiv (categories cs.CV, cs.LG, eess.IV and q-bio). Publication dates from 1 January 2020 to 11 October 2026. Journal websites and reference lists of included articles were also hand-searched.

### Query families

The query families below are templates. [Authors: replace them with the exact strings and run dates, and report the number of records retrieved for each database.]

**A. Pathology foundation models**
`("foundation model" OR "self-supervised" OR "vision-language" OR "vision transformer") AND (pathology OR histopathology OR "whole slide image*" OR "computational pathology")`

**B. Rare diseases and few-shot adaptation**
`(A) AND ("rare disease*" OR "rare cancer*" OR "rare tumo*" OR orphan OR sarcoma OR "paediatric tumo*" OR "pediatric tumo*" OR lymphoma OR "few-shot" OR "zero-shot" OR "prompt tuning" OR "low-rank adaptation" OR "multiple instance learning")`

**C. Domain generalization and clinical validation**
`(A) AND ("domain shift" OR "domain generali*" OR robustness OR "batch effect*" OR "stain normali*" OR "external validation" OR prospective OR "silent trial" OR calibration OR "conformal prediction" OR "reporting guideline*" OR regulat*)`

### Eligibility

- **Included:** original research, benchmarks, reporting guidelines and regulatory documents relevant to pathology foundation models or data-efficient adaptation, with at least one of (i) a rare disease application, (ii) a quantitative evaluation of cross-site robustness, or (iii) a clinical or prospective evaluation.
- **Excluded:** news articles, company press releases, blogs, and records lacking author and venue information. Conference abstracts were included only when they reported quantitative results, and they are labelled as such.

### Screening and data extraction

[Authors: report the number of records identified, screened, assessed in full text and included, for example as a flow diagram adapted from PRISMA 2020. Describe who screened records and how disagreements were resolved.]

### Reference verification

Every reference in the main manuscript was verified against Crossref (DOI metadata), arXiv (identifier, title, authors and abstract), journal websites (key quantitative statements) or ClinicalTrials.gov (registrations). The verification log is available from the authors on request.

---

## Supplementary Table 1 | Inventory of pathology foundation models

[Authors: complete this table from the developers' publications and model cards, and check licence terms on the date of submission.]

| Model | Developer | Backbone and parameters | Pretraining data | Objective | Weights available | Licence | Ref. |
|---|---|---|---|---|---|---|---|
| CTransPath | Sichuan Univ./Tencent | Swin-T + CNN | ~15 million tiles | SRCL | Yes | [ ] | 22 |
| UNI | Mass General Brigham | ViT-L | >100 million tiles; ~100,000 slides | DINOv2 | Yes (gated) | [ ] | 15 |
| Virchow / Virchow2 / Virchow2G | Paige | ViT-H (632M) / ViT-G (1.9B) | ~1.5M / 3.1M slides | DINOv2 (modified) | Partially | [ ] | 16, 24 |
| Prov-GigaPath | Providence / Microsoft | ViT-g + LongNet | 1.3 billion tiles; 171,189 slides | DINOv2 + MAE | Yes | [ ] | 17 |
| CHIEF | Harvard | CTransPath-based + slide aggregator | 60,530 slides (19 anatomical sites) | Unsupervised + weakly supervised | Yes | [ ] | 25 |
| Phikon / Phikon-v2 | Owkin | ViT-B / ViT-L | Public data | iBOT / DINOv2 | Yes | [ ] | 23, 18 |
| RudolfV / Atlas | Aignostics, Mayo Clinic, Charité | ViT-L / ViT-H | Multi-stain; ~1.2M slides (Atlas) | DINOv2-based | [ ] | [ ] | 19, 20 |
| Hibou | HistAI | ViT-B / ViT-L | [ ] | DINOv2 | Yes | [ ] | 21 |
| CONCH | Mass General Brigham | ViT + text encoder | 1.17 million image–caption pairs | Contrastive captioning | Yes (gated) | [ ] | 35 |
| PLIP | Stanford | ViT + text encoder | Public image–text pairs | CLIP-style | Yes | [ ] | 34 |
| KEEP | Shanghai Jiao Tong Univ. | Vision–language + knowledge graph | ~143,000 semantic groups | Knowledge-enhanced contrastive | [ ] | [ ] | 36 |
| MUSK | Stanford | Multimodal transformer | [ ] | Masked modelling + contrastive | [ ] | [ ] | 37 |
| PathChat | Mass General Brigham | UNI-based encoder + LLM | Instruction data | Instruction tuning | [ ] | [ ] | 38 |
| TITAN | Mass General Brigham | Slide encoder | 335,645 slides; 423,122 synthetic captions | SSL + vision–language | Yes (gated) | [ ] | 33 |
| PRISM | Paige | Perceiver + language decoder | Virchow tile embeddings | Report-supervised | [ ] | [ ] | 123 |
| GPFM | HKUST | ViT | [ ] | Unified knowledge distillation | [ ] | [ ] | 26 |

[ ] = to be completed by the authors. Reference numbers in the last column correspond to the main-text reference list and must be rechecked after final editing.

---

## Supplementary Table 2 | Domain-shift sources, mitigation strategies and strength of evidence

| Source of shift | Typical manifestation | Mitigation (examples) | Strength of evidence |
|---|---|---|---|
| Staining and reagents | Colour distribution, stain intensity, fading | Classical stain normalization (Reinhard, Macenko, Vahadane); generative normalization; self-supervised normalization without data transfer | Strong for colour shift (multicentre benchmark with tissue stained in 66 laboratories) |
| Scanners and acquisition | Texture, white balance, compression artefacts | Multi-scanner training data; GAN-based domain adaptation (crescent detection improved by up to 63.4% across scanners) | Moderate to strong |
| Centre and tissue processing | Institution-specific embedding signatures | More robust foundation models, vision–language alignment and post hoc robustification (reduces but does not eliminate errors); centre predictability from embeddings 88–98% | Strong (20 models, 34 centres) |
| Tissue type | Rare organs and morphologies under-represented in pretraining | Multi-tissue and multi-stain pretraining; H&E + Ki-67 fusion | Moderate |
| Disease spectrum and population | Long-tail subtypes; age, sex, ancestry and geographic shift | Knowledge-guided adaptation (FLEX); ontology-aligned vision–language pretraining (KEEP); subgroup reporting | Weak to moderate (little rare-disease-specific evidence) |

---

## Supplementary Table 3 | Trustworthiness dimensions, rare-disease-specific risks and actionable requirements

| Dimension | Rare-disease-specific risk | Actionable requirement | Current status |
|---|---|---|---|
| External validation | Mostly single-source retrospective data; wide confidence intervals | At least three centres, several scanners and stains; report ID and OOD performance and their difference | Uncommon (24% of studies in rare neurological disease AI) |
| Calibration | Overconfidence after few-shot adaptation; low prevalence lowers positive predictive value | Reliability diagrams and expected calibration error; per-patient calibration | Rarely reported |
| Uncertainty and abstention | Coverage guarantees may fail under distribution shift | Conformal prediction with abstention; distinguish marginal from conditional coverage | Methods exist; not yet evaluated in rare diseases |
| Bias and fairness | Centre signatures combined with very small subgroups | Subgroup performance and calibration audits; report centre predictability | Addressed in few studies |
| Generative risk | Fluent but wrong descriptions of unfamiliar entities | Clinically grounded evaluation; structured output; human review | Metrics proposed; not evaluated in rare diseases |
| Clinical utility | Discrimination does not equal benefit at low prevalence | Decision-curve analysis, net benefit, change in decisions, immunohistochemistry use, turnaround time | Essentially absent |
| Prospective evidence | Few cases per centre; slow accrual | Registry-based multicentre silent trials; randomized trials with workflow or patient end points | Prospective accuracy evaluation in two disease groups; no utility trials |
| Health economics | Unknown cost-effectiveness relative to referral and send-out testing | Cost-effectiveness analysis alongside prospective studies | Absent |
| Regulation and governance | Locked algorithms versus continual accrual of cases | Predetermined change control plans; model cards; withdrawal criteria; post-market surveillance | Frameworks exist; no rare disease histology authorization identified |

Sources for all entries are cited in the main text.
