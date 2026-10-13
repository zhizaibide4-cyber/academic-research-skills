---
title: "Pathology foundation models for rare disease diagnosis: data-efficient adaptation, cross-site robustness and the evidence gap"
article_type: Review
target_journal: Nature Medicine
version: Revised draft R1 (prepared for presubmission enquiry)
date: 13 October 2026
---

# Pathology foundation models for rare disease diagnosis: data-efficient adaptation, cross-site robustness and the evidence gap

**Authors:** [Author 1]<sup>1</sup>, [Author 2]<sup>2</sup>, … , [Corresponding author]<sup>1,✉</sup>

<sup>1</sup>[Department, Institution, City, Country].

<sup>2</sup>[Department, Institution, City, Country].

✉ e-mail: [corresponding.author@institution.org]

> Placeholder: Nature Portfolio journals do not accept AI tools as authors. The previous by-line ("ClawsGO Science Agent / ClawsGO Science Harness") must be replaced by the accountable human authors, and AI assistance must be described in the Methods-equivalent statement at the end of this Review.

---

## Abstract

Histopathology is the diagnostic step for many rare tumours and some non-neoplastic rare diseases, yet few of these conditions have the case numbers that supervised learning requires. Pathology foundation models, pretrained on up to millions of whole-slide images, promise representations that can be adapted with few labelled cases. Here we review work published between 2020 and 2026 that tests this promise. We compare adaptation strategies, from zero-shot prompting and case retrieval to parameter-efficient and full fine-tuning, and summarize evidence that site, scanner and staining signatures remain encoded in current models. Grading disease-specific applications on an explicit evidence scale, we find that most remain retrospective; prospective evaluation has been reported for central nervous system tumours and autoimmune hepatitis, but no study has yet shown improved patient outcomes. We close with the calibration, bias, reporting and regulatory requirements that rare disease models must meet before they can change care.

---

## Introduction

Rare diseases are individually uncommon but collectively frequent. An analysis of the Orphanet database estimated a cumulative point prevalence of 3.5–5.9%, corresponding to 263–446 million people worldwide, across 6,172 clinically defined conditions, 71.9% of which are genetic and 69.9% of which have exclusively paediatric onset<sup>1</sup>. The number of distinct conditions depends on how diseases are counted and exceeds 7,000 in some ontologies<sup>2</sup>. Diagnosis is slow: in a Rare Barometer survey of 6,507 people living with 1,675 rare diseases in 41 European countries, the average total diagnosis time was 4.7 years<sup>3</sup>. Genomic sequencing has shortened this path for many families, but the 100,000 Genomes Project pilot reached a molecular diagnosis in only 25% of probands<sup>4</sup>, and most patients evaluated in dedicated undiagnosed-disease programmes remain without a definitive diagnosis after exome or genome sequencing<sup>5</sup>.

Tissue examination is the diagnostic step for a substantial fraction of rare conditions. Rare cancers, defined in Europe as those with an incidence below 6 per 100,000 per year, together account for 20–25% of all malignancies and for more than 70% of cancers in paediatric oncology<sup>6,7</sup>. Morphological classification of these tumours is difficult. In a population-based study of sarcomas in three European regions, the initial diagnosis was fully concordant with expert review in only 56% of cases<sup>8</sup>. Molecular classifiers such as DNA methylation profiling have changed practice for central nervous system (CNS) tumours and sarcomas<sup>9,10</sup>, but they require tissue, time and infrastructure that many centres lack. Access to pathology services is severely limited in many low- and middle-income countries<sup>11</sup>, so the expertise needed to recognize a rare entity is often absent where the patient is seen.

Computational pathology has moved from task-specific models trained on curated annotations to foundation models: large encoders pretrained on unlabelled histology that can be adapted to many downstream tasks<sup>12,13</sup>. The attraction for rare diseases is obvious. If a representation learned from hundreds of thousands of slides already separates morphological patterns that are diagnostically relevant, a rare entity might be recognized after exposure to a handful of labelled cases rather than thousands. Whether this works in practice depends on three conditions that are the organizing axes of this Review: whether the representation encodes long-tail morphology at all (section 'Building blocks'); which adaptation strategy extracts that information most efficiently when labels are counted in single digits (section 'Data-efficient adaptation'); and whether the adapted model remains reliable in a hospital other than the one that supplied the training cases (section 'Cross-site robustness'). We then grade the disease-specific evidence (section 'Applications') and discuss what is needed for clinical translation (section 'From discrimination to clinical evidence').

We searched PubMed/MEDLINE, Web of Science and arXiv for work published between 1 January 2020 and 11 October 2026 using three query families (pathology foundation models; rare disease and few-shot adaptation; domain generalization and clinical validation). The full search strings, screening criteria and the list of included studies are provided in Supplementary Information. This is a narrative review rather than a systematic review: we did not perform formal risk-of-bias assessment or meta-analysis, and quantitative results are reported as published by the original authors. Preprints and conference abstracts are identified as such in the reference list, and peer-reviewed evidence is weighted more heavily throughout. Definitions of the terms and of the evidence-maturity levels used here are given in Box 1.

> **Box 1 | Definitions and evidence-maturity levels used in this Review**
>
> **Foundation model.** A model pretrained on large, mostly unlabelled data that can be adapted to many downstream tasks. In pathology, the term covers tile (patch) encoders, slide encoders that aggregate tile embeddings, and vision–language models.
>
> **k-shot setting.** Adaptation in which k labelled examples (here, usually slides or patients) per class are available. We use 'few-shot' for k ≤ 10 and 'ultra-rare' for entities with fewer than five available cases.
>
> **In-distribution (ID) and out-of-distribution (OOD) performance.** Performance on data from the same sources as the training data, and on data from sources not seen during training (different hospital, scanner, staining protocol or population).
>
> **Evidence-maturity levels.** We classify each disease-specific application by the strongest validation reported:
> - **L0, inferred feasibility:** no disease-specific model; feasibility inferred from general-purpose models or neighbouring diseases.
> - **L1, internal retrospective validation:** single-source data with random or cross-validated splits, including conference abstracts.
> - **L2, independent external validation:** retrospective validation on at least one centre, scanner or cohort not used for training.
> - **L3, prospective evaluation:** prospective accuracy assessment in routine workflow (including silent deployment) or a reader study embedded in prospective care.
> - **L4, demonstrated clinical utility or authorization:** randomized or controlled evidence of benefit to patients or workflow, or regulatory authorization for clinical use.
>
> These levels describe the design of the validation, not the size of the reported metric. A study at L1 with an area under the curve (AUC) of 0.99 provides weaker evidence than a study at L2 with an AUC of 0.85.

## Building blocks of pathology foundation models

### Self-supervised objectives and tile encoders

Almost all current pathology encoders are vision transformers pretrained with self-supervised objectives. Contrastive and self-distillation methods, most commonly DINOv2<sup>14</sup>, which combines self-distillation with masked image modelling, have become the dominant recipe, used by UNI, Virchow, Prov-GigaPath, Phikon-v2, RudolfV, Atlas and Hibou among others<sup>15–21</sup>. Earlier encoders such as CTransPath used semantically relevant contrastive learning on about 15 million tiles<sup>22</sup>, and purely masked-reconstruction objectives have generally underperformed on discriminative tasks<sup>23</sup>.

Table 1 summarizes representative models. UNI, a ViT-L model pretrained on more than 100 million tiles from about 100,000 diagnostic haematoxylin and eosin (H&E) slides covering 20 major tissue types, was evaluated on 34 tasks and demonstrated few-shot slide classification with class prototypes<sup>15</sup>. Virchow, a 632-million-parameter ViT-H model trained on about 1.5 million slides, achieved a specimen-level AUC of 0.950 for pan-cancer detection across nine common and seven rare cancers, and 0.937 on the rare cancers alone, with performance that was not uniform across individual rare types<sup>16</sup>. Virchow2 extended training to 3.1 million slides from diverse tissues, institutions and stains<sup>24</sup>. Prov-GigaPath was pretrained on 1.3 billion tiles from 171,189 slides of real-world data<sup>17</sup>, and CHIEF combined unsupervised tile pretraining with weakly supervised slide-level pretraining across 19 anatomical sites<sup>25</sup>. Distillation-based frameworks aim to combine the strengths of several teacher models in a single encoder<sup>26</sup>.

### Does scale help rare diseases?

The relationship between pretraining scale and downstream performance is contested, and the distinction matters for rare diseases. The developers of Virchow2 concluded that data diversity and domain-specific methods can outperform models that scale only in parameter count, although on average performance benefited from combining all three<sup>24</sup>. Atlas reported state-of-the-art results on 21 public benchmarks without being the largest model by parameters or training set size<sup>20</sup>, and a lymphoma-specialized encoder outperformed general-purpose models pretrained on 10–100 times more images on lymphoma tasks<sup>27</sup>. Independent benchmarks are more sceptical. An evaluation of 19 foundation models on 13 patient cohorts (6,818 patients, 9,528 slides) found that data diversity outweighed data volume<sup>28</sup>, and a benchmark of 32 general and pathology-specific models found that model size and pretraining dataset scale did not consistently predict downstream performance, with small and task-dependent differences among the top models<sup>29</sup>. By contrast, the PathoROB benchmark observed a strong rank correlation between the number of pretraining slides and robustness to non-biological variation across 20 models (Spearman ρ = 0.692)<sup>30</sup>. Taken together, these results suggest that scale may buy robustness more reliably than it buys average accuracy, and that coverage of tissue types, institutions and stains is the more relevant property for long-tail diseases. None of these benchmarks, however, was designed around rare entities, so the question of whether scale improves the encoding of rare morphology specifically remains open (Box 3).

Benchmark design itself is a confounder. The ranking of feature extractors depends on the downstream aggregator and its configuration, and the performance ranges of leading models overlap substantially<sup>28,29,31</sup>. Claims that a single model is uniformly superior should therefore be read with caution.

### Slide-level and multimodal models

Tile embeddings must be aggregated to produce a slide-level prediction. HIPT parameterized this aggregation hierarchically by self-distillation on 10,678 gigapixel slides<sup>32</sup>; Prov-GigaPath encoded tens of thousands of tiles jointly with a long-context transformer<sup>17</sup>; and TITAN combined visual self-supervision on 335,645 slides with alignment to pathology reports and 423,122 synthetic captions generated by PathChat, producing slide representations that can be used without fine-tuning<sup>33</sup>. Notably, the benchmark of 19 foundation models found that slide encoders did not outperform multiple-instance learning applied to tile embeddings, and that the advantage of the best overall model (CONCH) was less pronounced in low-data scenarios and for low-prevalence tasks, which are the typical conditions for rare diseases<sup>28</sup>.

Language provides a cheap and abundant prior for rare entities, because textbooks and reports describe many diseases for which few digitized slides exist. PLIP showed that contrastive image–text pretraining on publicly shared pathology images was feasible<sup>34</sup>, and CONCH, trained on 1.17 million image–caption pairs, enabled zero-shot classification, retrieval and captioning across 14 benchmarks<sup>35</sup>. KEEP addressed a specific weakness of naive contrastive learning, in which captions of related diseases are treated as unrelated negatives: it used a knowledge graph of 11,454 diseases and 139,143 attributes to reorganize image–text pairs into about 143,000 ontology-aligned semantic groups, and reported its largest gains on rare subtypes across four institutional rare cancer datasets (926 cases)<sup>36</sup>. Other vision–language models, including MUSK, extend this approach to multimodal precision oncology<sup>37</sup>. PathChat coupled a pathology vision encoder with a large language model and instruction tuning to support interactive differential diagnosis<sup>38</sup>. Generative assistants of this kind could make rare disease reasoning more transparent, but they introduce the hallucination risks discussed below.

> **Table 1 | Representative pathology foundation models and their relevance to rare diseases** (see Display items; the full version with licensing information is provided as Supplementary Table 1).

## Data-efficient adaptation for rare diseases

### Why rare diseases are an extreme few-shot problem

Rare disease adaptation differs from textbook few-shot learning in two respects. First, the label space is large and the number of examples per class is tiny: in PathPT, which assembled eight rare and three common cancer datasets spanning 56 subtypes and 3,958 slides, the 30-subtype EBRAINS brain tumour task was evaluated with 5 or 10 slides per class<sup>7,39</sup>. Second, rare classes coexist with common ones in the same label space, so aggregate metrics can conceal poor performance on the rarest classes. For example, a lymphoma-specialized foundation model reported in abstract form achieved a mean AUC of 0.98 for six-class lymphoma subtyping on internal test folds, but class-wise recall was 92.0% for diffuse large B-cell lymphoma and only 77.2% and 70.8% for marginal zone and mantle cell lymphoma, respectively<sup>27</sup>. Class-wise recall, not only macro-averaged metrics, should therefore be reported.

Figure 2 places the main adaptation strategies on a common scale of labelling budget and trainable parameters. The appropriate strategy changes as the number of labelled cases grows.

### Zero-shot prompting, prototypes and retrieval

At the lowest labelling budgets, models can be used without any parameter updates. MI-Zero introduced zero-shot slide classification by computing similarity between tile embeddings and text prompts and pooling the top-scoring tiles<sup>40</sup>, an approach later adopted by CONCH<sup>35</sup>. Prototype methods average the embeddings of a few labelled slides per class and classify new slides by nearest neighbour<sup>15</sup>.

Retrieval may be better suited than classification to rare diseases because it returns reference cases that a pathologist can compare against, which mirrors how rare entities are recognized in practice. Self-supervised slide search engines such as Yottixel, SMILY and SISH demonstrated scalable whole-slide retrieval before the foundation-model era<sup>41–43</sup>. TITAN evaluated rare cancer retrieval on a database of 43 rare and 143 common cancer types without fine-tuning<sup>33</sup>, and RudolfV was explicitly designed with reference-case retrieval as a use case<sup>19</sup>. The obvious limitation is coverage: retrieval cannot return a diagnosis that is absent from the reference library, and ultra-rare diseases are the least likely to be represented.

### Linear probing and weakly supervised multiple-instance learning

Linear probing, in which a linear classifier is trained on frozen embeddings, is cheap, reproducible and hard to overfit, and it is the appropriate first baseline<sup>44</sup>. In a multicentre Swedish paediatric brain tumour cohort, linear probes on UNI and CONCH features substantially outperformed an ImageNet-pretrained ResNet-50<sup>45</sup>. Multiple-instance learning (MIL) aggregators such as attention-based MIL, CLAM and TransMIL learn slide-level predictions from slide-level labels alone<sup>46–49</sup>. In rare diseases, the main benefit of MIL is to reduce the annotation unit from regions to slides rather than to increase accuracy. A multicentre benchmark of five foundation models with MIL aggregators for lymphoma subtyping illustrates the limits: balanced accuracy exceeded 80% in distribution but fell to about 60% on out-of-distribution test sets<sup>50</sup>.

Foundation models are not universally superior. In mitotic figure classification, end-to-end trained convolutional networks matched or exceeded classifiers built on foundation-model features<sup>51</sup>, and a benchmark of 11 foundation models on 11 kidney pathology tasks found consistent performance declines for tasks that require fine-grained microstructural discrimination<sup>52</sup>. Where diagnostic criteria are pixel-level and well defined, task-specific models remain competitive.

### Parameter-efficient fine-tuning and prompt tuning

Parameter-efficient fine-tuning (PEFT) inserts a small number of trainable parameters into a frozen encoder. Low-rank adaptation (LoRA) adds trainable low-rank matrices to attention layers<sup>53</sup>; visual prompt tuning and context optimization learn input prompts on the visual and text side, respectively<sup>54,55</sup>. In a benchmark of adaptation strategies across 20 datasets, PEFT was both efficient and effective for classification<sup>44</sup>, and LoRA-adapted UNI, Virchow and Virchow2 encoders have been compared for atypical mitotic figure classification<sup>56</sup>. Prompt-guided tuning has been proposed specifically to address domain shift<sup>57</sup>. PEFT improves adaptation efficiency, but there is little evidence that it improves robustness to unseen sites.

PathPT is the most directly relevant study for rare tumours. It converts slide-level supervision into tile-level guidance and tunes task-specific prompts for a vision–language backbone. Across eight rare and three common cancer datasets, it outperformed contemporary MIL methods in data-scarce settings; with KEEP as backbone, it reached a balanced accuracy of 0.679 on the 30-subtype EBRAINS task in the 10-shot setting, while also localizing tumour regions<sup>7</sup>. The improvement in both accuracy and spatial grounding is important because interpretability is a precondition for adoption in diseases that pathologists rarely see.

### When to fine-tune the full model

Full fine-tuning remains the strongest option when thousands of labelled cases from the target distribution are available<sup>58</sup>, but it is rarely appropriate for rare diseases. It has the most trainable parameters, the highest compute cost and the greatest capacity to fit centre-specific signatures. In our assessment, the evidence supports a stepwise approach: start with linear probes and retrieval, add PEFT or prompt tuning when tens of labelled cases per class are available, and reserve full fine-tuning for settings with large, multicentre labelled cohorts.

## Cross-site robustness

### Sources of domain shift and why rare diseases amplify them

Domain shift in computational pathology arises at five levels: staining and reagents; scanners and image acquisition; centre-specific tissue processing; tissue type; and disease spectrum and population (Fig. 3a). Site-specific digital histology signatures can be learned by deep learning models and can bias their accuracy, as shown in The Cancer Genome Atlas<sup>59</sup>, and stain variability has long been recognized as a source of failure<sup>60,61</sup>.

Rare diseases amplify these effects through a simple mechanism. When few cases are available, they usually come from one or two centres; the model can then learn the centre signature as a proxy for the label, and performance collapses unpredictably elsewhere. A rare disease model is also more likely to be used precisely where local expertise to catch its errors is lacking.

### Quantified out-of-distribution losses

PathoROB systematically evaluated 20 pathology foundation models on four datasets covering 28 biological classes from 34 medical centres and found robustness deficits in all models<sup>30</sup>. The medical centre of origin could be predicted from the embeddings with mean accuracies of 88–98%, and non-robust representations caused major diagnostic errors in downstream tasks; more robust models, vision–language alignment and post hoc robustification reduced but did not eliminate these errors<sup>30</sup>. Earlier analyses reached similar conclusions using a related robustness index and batch-effect analyses<sup>62,63</sup>.

Evidence specific to rare lesions is scarce but sobering. In kidney biopsies from 22 hospitals and three scanner types, detection precision for rare lesions such as crescents and segmental sclerosis, which made up only 2–3% of annotations, fell by up to 70.3% across domains. Combining semi-supervised learning with CycleGAN-based domain adaptation reduced the mean Fréchet inception distance between institutions from 55.9 to 20.2 and improved crescent detection by up to 63.4% in cross-scanner settings<sup>64</sup>. In lymphoma subtyping, balanced accuracy dropped from more than 80% to about 60% out of distribution<sup>50</sup>. Figure 3b summarizes these reported losses; because the underlying metrics differ (relative versus absolute changes), they should not be compared directly.

### Mitigation strategies

Mitigation operates at four levels (Supplementary Table 2). At the image level, classical stain normalization methods (Reinhard, Macenko, Vahadane) are fast and training-free, and generative methods offer better visual consistency at higher computational cost; a benchmark of eight methods on a dataset in which the same tissue was stained in 66 laboratories favoured generative approaches overall<sup>65</sup>. Self-supervised stain normalization can be learned without transferring data between centres<sup>66</sup>. Image normalization addresses colour, not section thickness, tissue architecture or population differences.

At the representation level, knowledge-guided adaptation (FLEX) aligns image features with domain-specific visual and textual concepts and improved both cross-domain generalization and demographic fairness across 16 clinical tasks<sup>67</sup>. At the model and inference level, test-time adaptation can improve robustness, for example when combined with uncertainty decomposition and causal modelling in colorectal cancer<sup>68</sup>, and continual-learning approaches allow new centres to be added to a retrieval index without rebuilding it<sup>69</sup>. A large benchmark of test-time adaptation, however, found that explanation drift increased with adaptation strength, which suggests that adaptation may trade interpretability for accuracy<sup>70</sup>. At the data level, diversity of centres, scanners, stains and diseases is the most consistent lever<sup>24,28</sup>; RudolfV, for example, included immunohistochemistry and special stains in pretraining<sup>19</sup>, and fusion of H&E and Ki-67 images improved paediatric brain tumour classification<sup>71</sup>.

### Minimum requirements for robustness evidence

We suggest three minimum requirements for any claim of generalizability in a rare disease model (Box 2): reporting of in-distribution and out-of-distribution performance and their difference; data splits by patient, centre and scanner rather than by tile or slide; and assessment of explanation stability alongside performance<sup>70,72</sup>. Robustness metrics and centre predictability from embeddings should be reported when foundation models are released<sup>30,73</sup>.

> **Box 2 | Minimum reporting checklist for rare disease computational pathology studies**
>
> 1. Number of patients, slides and contributing centres per class, including the rarest class.
> 2. Split unit (patient, centre, scanner) and confirmation that no patient contributes to more than one split.
> 3. Class-wise sensitivity and specificity with 95% confidence intervals, not only macro-averaged metrics.
> 4. In-distribution and out-of-distribution performance and their difference, with the source of each test set.
> 5. Labelling budget–performance curve (for example, k = 1, 2, 5, 10, 25 cases per class) rather than a single k.
> 6. Calibration (reliability diagram, expected calibration error) and, where applicable, abstention rate and coverage.
> 7. Positive predictive value at a realistic prevalence for the intended use.
> 8. Subgroup performance by age, sex, centre and scanner where sample size allows, and an explicit statement where it does not.
> 9. Reference standard used (expert consensus, molecular test) and its own known error rate.
> 10. The reporting guideline followed (TRIPOD+AI, STARD-AI, DECIDE-AI, CONSORT-AI or TRIPOD-LLM)<sup>74–78</sup>.

## Applications in rare diseases

We grouped disease-specific applications by organ system and assigned each to an evidence-maturity level (Box 1, Fig. 4 and Table 2). Three caveats apply. Several studies are available only as preprints or conference abstracts; the levels describe the validation design reported, not our independent assessment of its quality; and we did not attempt to pool performance metrics across studies.

### Rare tumours

**CNS tumours.** CNS tumours provide the most mature evidence. Hetairos predicts 102 methylation-based CNS tumour subtypes from H&E slides. It was built and validated on 9,606 patients and more than 11,000 slides from 11 centres on four continents, identified 50–70% of cases with high confidence with an accuracy of 0.87 for its highest-rated predictions, outperformed five board-certified neuropathologists in a histology-only comparison (0.68 versus 0.30), and was evaluated prospectively in routine diagnostics, where it reduced turnaround from 12 days for molecular testing to 12 minutes<sup>79</sup>. This is, to our knowledge, the first rare tumour histology model with prospective evaluation (L3), although it does not yet establish improved patient outcomes. Paediatric brain tumours have also served as a methodological testbed for few-shot adaptation (PathPT)<sup>7</sup>, for foundation-model linear probes in a multicentre cohort<sup>45</sup> and for multi-stain fusion<sup>71</sup>.

**Bone and soft-tissue sarcomas.** Sarcomas comprise more than 100 subtypes and have high rates of diagnostic discordance<sup>8</sup>. A multicentre study integrating slides from three medical centres and the Children's Oncology Group used foundation-model features to distinguish rhabdomyosarcoma from non-rhabdomyosarcoma soft-tissue sarcomas and to subtype rhabdomyosarcoma, currently available as a preprint (L2)<sup>80</sup>. Single-centre studies of uterine leiomyosarcoma report near-perfect metrics (L1)<sup>81</sup>. Very high performance in single-source data should be interpreted cautiously; methylation-based sarcoma classification showed how diagnostic yield can differ between curated reference sets and routine practice<sup>10,82</sup>.

**Lymphomas.** Lymphoma subtyping illustrates how aggregate metrics conceal rare-class weaknesses (see 'Data-efficient adaptation')<sup>27</sup>. For peripheral T-cell lymphomas, a weakly supervised model using UNI features was trained on 223 slides from a national registry and validated on an independent cohort of 118 patients, reported in abstract form (L2)<sup>83</sup>. The multicentre MIL benchmark covered four common subtypes and explicitly identified rare subtypes as a gap<sup>50</sup>.

**Rare renal tumours and cancers of unknown primary.** Zero-shot classification of renal neoplasms including rare entities using foundation-model embeddings has been reported in abstract form (L1)<sup>84</sup>. Related work on predicting the origin of cancers of unknown primary demonstrates how histology models can narrow differential diagnoses when the primary site is not evident<sup>85</sup>.

### Non-neoplastic rare diseases

**Kidney.** The 22-hospital study of rare glomerular lesions described above is both an application and a robustness study (L2)<sup>64</sup>. For Fabry nephropathy, a lysosomal storage disorder, the ZEBRA tool quantified podocyte inclusions ('zebra bodies'), and its score distinguished cases from controls and correlated with clinical markers (L1)<sup>86</sup>. The benchmark of 11 foundation models showed that fine-grained renal microstructure remains challenging<sup>52</sup>.

**Liver.** For autoimmune hepatitis, a multiple-instance model (AIOLI) trained on 170 untreated cases and 232 controls achieved an AUC of 0.92 in the training data but 0.74 on an external dataset, with poor discrimination from hepatitis B (AUC 0.42); it was also tested prospectively in routine practice in 2025 (L3)<sup>87</sup>. This study shows that prospective evaluation of a non-neoplastic rare disease model is feasible, and also that external performance can fall well below development performance.

**Inflammatory bowel disease.** Inflammatory bowel disease is not rare, but it shares the problem of inter-observer variability in histological scoring. Multicentre deployment of an artificial intelligence (AI) tool for the Nancy Histopathology Index<sup>88</sup> and activity classification on whole-slide images<sup>89</sup> provide useful translational templates for rare inflammatory conditions with similar scoring systems.

A scoping review of AI in rare neurological diseases found that only 24% of studies reported external validation and that ultra-rare conditions were almost absent<sup>90</sup>, consistent with the pattern we observe in histopathology.

### Rare infectious and parasitic diseases

Parasitic infections differ technically from tumours because the diagnostic target is a discrete structure such as an egg or a parasite, for which object-detection networks are well suited. Detection of *Schistosoma* eggs in bladder histopathology has been reported (L1)<sup>91</sup>. For bacterial infections with nonspecific granulomatous histology, we found no disease-specific validated histopathology models (L0).

### What the evidence shows

Three observations stand out (Fig. 4 and Table 2). First, the evidence is concentrated in rare tumours, and specifically in subtyping tasks; non-neoplastic and infectious rare diseases are sparsely represented. Second, reported performance and evidence level are not aligned: some of the highest metrics come from single-source studies at L1, whereas several studies with modest metrics have external validation. Third, prospective evaluation has now been reported for CNS tumours<sup>79</sup> and autoimmune hepatitis<sup>87</sup>, but we found no randomized or controlled study of clinical utility (L4) for any rare disease histology model.

## From discrimination to clinical evidence

### Discrimination is not utility

Most rare disease AI studies report discrimination metrics. At low prevalence, discrimination translates poorly into clinical value. If a condition has a prevalence of 1% in the tested population, a model with 95% sensitivity and 95% specificity has a positive predictive value of about 16%, so roughly five of six positive flags are false. Evaluations must therefore include calibration, clinical utility (for example, net benefit in decision-curve analysis or the proportion of changed decisions) and workflow effects such as reading time, use of immunohistochemistry and turnaround time.

### External validation, calibration and uncertainty

External validation remains the exception in this field (see 'Applications') and in rare disease AI more broadly<sup>90</sup>. The updated PROBAST+AI tool provides a structured way to assess risk of bias and applicability<sup>92</sup>. Few-shot models tend to be overconfident on out-of-distribution inputs. Conformal prediction offers finite-sample coverage guarantees and a principled basis for abstention; it has been applied to prostate pathology<sup>93</sup> and to leukaemia classification, where it reduced errors in the predictions that were retained<sup>94</sup>. TRUECAM combined uncertainty-aware modelling with conformal prediction across several foundation models for non-small-cell lung cancer diagnosis<sup>95</sup>. Coverage guarantees are, however, marginal over calibration sets and can fail for an unlucky calibration sample or under distribution shift, and they require reliably labelled calibration data<sup>96</sup>. Because tiles and slides from one patient are correlated, we recommend that calibration and coverage be assessed per patient. For rare diseases, where calibration sets are themselves small, the stability of coverage across sites must be demonstrated rather than assumed.

### Bias and fairness

Computational pathology models can show demographic disparities in misdiagnosis<sup>97</sup>, and the centre signatures described above provide a structural source of bias: if a disease is systematically over- or under-diagnosed at one centre, a model may learn the centre's habits rather than the disease<sup>30,59</sup>. The smallest subgroups are often those for which accurate diagnosis matters most. Mitigation includes knowledge-guided adaptation<sup>67</sup>, subgroup reporting of performance and calibration, and audits within model cards and post-market surveillance<sup>98</sup>.

### Additional risks of generative models

When foundation models generate reports or answer questions, errors become fluent text. The REG 2025 benchmark, built on about 10,500 slide–report pairs from five institutions, identified instability in quantitative attribute estimation ('numeric hallucination') and a tendency towards diagnostic overspecification<sup>99</sup>. Surface-overlap metrics such as BLEU and ROUGE are poor proxies for clinical correctness, and reference-free consistency measures have been proposed<sup>100</sup>. For rare diseases, a plausible but incorrect description is particularly dangerous because the reader is less likely to recognize the error.

### Reporting guidelines, regulation and prospective evidence

Reporting standards now cover most study designs: TRIPOD+AI for prediction models<sup>74</sup>, STARD-AI for diagnostic accuracy studies<sup>75</sup>, DECIDE-AI for early clinical evaluation<sup>76</sup>, SPIRIT-AI and CONSORT-AI for trials<sup>77,101</sup> and TRIPOD-LLM for studies using large language models<sup>78</sup>. Regulatory pathways for pathology AI exist. The first De Novo authorization for an AI product in digital pathology was granted in 2021 to an assistive prostate cancer detection system<sup>102,103</sup>, and the US Food and Drug Administration has issued final guidance on predetermined change control plans, which allow pre-specified modifications such as additional scanners without a new submission<sup>104</sup>. In the European Union, the AI Act classifies most diagnostic AI as high risk and imposes requirements for risk management, data governance, transparency and human oversight<sup>105</sup>. Current authorizations are for locked algorithms with assistive labelling, which fits poorly with rare disease models that need to be updated as cases accumulate.

Prospective evidence is emerging outside rare diseases. In the randomized MASAI trial of more than 100,000 women, AI-supported mammography screening increased cancer detection while reducing radiologist screen-reading workload<sup>106,107</sup>. In pathology, a fine-tuned foundation model for EGFR mutation detection in lung adenocarcinoma was deployed in a real-world silent trial, showing how prospective evaluation can be organized without affecting care<sup>58</sup>, and prospective evaluations of Hetairos for CNS tumours and AIOLI for autoimmune hepatitis are the first such examples in rare disease histopathology<sup>79,87</sup>. Randomized trials of AI-assisted pathology have also been registered, including a multicentre trial of AI-assisted pathologist performance (estimated enrolment 1,000), a trial of a human–AI workflow for breast cancer with an extensive intraductal component (estimated 480) and a trial of AI-predicted gene mutations to guide care in non-small-cell lung cancer (estimated 950)<sup>108–110</sup>; none addresses a rare disease. Expert surveys anticipate wider integration of foundation and agentic AI into pathology workflows but highlight persistent translational gaps<sup>111</sup>. Figure 5 sets out a staged evidence pathway from technical validation to clinical utility, with the failure modes that typically halt progress at each gate.

## Outlook

### Federated and multicentre collaboration

No single centre sees enough cases of most rare diseases to train or validate a reliable model, which makes federated learning a natural organizational form. The FeTS initiative trained a glioblastoma boundary detection model across 71 sites on six continents without sharing data<sup>112</sup>, and a review of federated learning in computational pathology identified system heterogeneity rather than client numbers as the main technical challenge<sup>113</sup>. In a related microscopy modality, federated training on collagen VI immunofluorescence images of patient-derived fibroblasts from two international organizations improved classification of collagen VI-related dystrophies (F1 score 0.82 versus 0.57–0.75 for single-organization models)<sup>114</sup>. The main barriers are now governance and incentives rather than algorithms.

### Molecular and textual supervision

In many rare tumours, molecular labels such as fusion genes, methylation classes or germline variants are more reproducible than morphological labels, whose definitions change as molecular understanding evolves<sup>9,10</sup>. Using molecularly confirmed cases to supervise morphological models, as Hetairos does for methylation classes<sup>79</sup>, shifts supervision from the least reliable to the most reliable labels and could bring molecular-level stratification to settings where molecular testing is unavailable. Spatial transcriptomic datasets and models that link morphology with gene expression (HEST-1k, MISO, STPath, Multi-Embed) provide technical building blocks for this approach<sup>115–118</sup>.

### Knowledge graphs and agentic reasoning

Outside pathology, rare disease diagnosis has benefited from structured knowledge. SHEPHERD used a knowledge graph of diseases, phenotypes and genes for few-shot, phenotype-driven diagnosis of rare genetic diseases<sup>119</sup>, and RareCollab integrated more than 100 genomic, transcriptomic and phenotypic evidence signals with large language models; in a benchmark of 890 patients, including 119 Undiagnosed Diseases Network probands with paired DNA and RNA data, it ranked 94% of diagnostic genes within the top ten candidates (preprint)<sup>120</sup>. Neither system uses histology. Incorporating morphological evidence from pathology foundation models into such multimodal reasoning is a largely unexplored direction.

### Rare diseases as a stress test for foundation models

Rare diseases are not only potential beneficiaries of foundation models; they are also among the most informative tests of them. Long-tail classes, data scattered across centres and scarce labels correspond to the weaknesses that average benchmark metrics on common cancers conceal: collapse of rare-class recall<sup>27</sup>, out-of-distribution performance loss<sup>30,50</sup> and miscalibration after adaptation<sup>96</sup>. Including rare disease tasks in the standard evaluation of new foundation models would serve both rare disease patients and the broader field<sup>121</sup>.

### Global access

In low- and middle-income settings, the shortage of pathologists coincides with limited scanning capacity and connectivity<sup>11</sup>. Lightweight models, edge deployment and low-cost imaging are therefore as important as accuracy. An AI-assisted cervical cytology screening system using a compact microscope illustrates the feasibility of this approach in resource-limited regions<sup>122</sup>. For parasitic diseases with well-defined morphological targets, the main barriers are infrastructure, cost, data-sharing policy and local regulatory capacity rather than algorithms.

> **Box 3 | Priority open questions**
>
> 1. **Benchmarks.** What would a shared rare disease benchmark look like, with performance reported as a function of cases per class, class-wise recall with confidence intervals and patient- and centre-level splits?
> 2. **Labelling budgets.** At what number of labelled cases per class do returns diminish for each adaptation strategy, and how should multicentre collection efforts be allocated accordingly?
> 3. **Ultra-rare entities.** For diseases with fewer than five available cases, should models defer to retrieval and expert consultation rather than output a class label, and how should this be evaluated?
> 4. **Scale versus coverage.** Does pretraining scale improve the encoding of rare morphology specifically, or mainly robustness to technical variation?
> 5. **Disentangling shift and rarity.** How can performance losses due to domain shift be separated from those due to under-representation of rare classes?
> 6. **Calibration across sites.** Under what conditions do calibration and conformal coverage transfer between centres when calibration sets are small?
> 7. **Prospective designs.** How can registry-based, multicentre silent trials be organized to accrue enough rare disease cases for prospective evaluation, and which end points (time to diagnosis, immunohistochemistry use, consultation turnaround) should be primary?
> 8. **Regulation of evolving models.** Can predetermined change control plans accommodate the iterative updates that rare disease models require as new cases accrue?

## Conclusions

Pathology foundation models have changed the rare disease problem from collecting enough data to train a model for each disease to adapting a general representation to a disease with few examples. The evidence reviewed here shows that this change shifts the decisive factors to adaptation strategy, cross-site reliability and clinical evidence rather than model size. Lightweight strategies, including prototypes, retrieval and prompt tuning, are the most efficient when only a handful of cases per class are available, but their gains narrow in low-prevalence and out-of-distribution settings. Current models encode the medical centre of origin strongly enough that it can be predicted from their embeddings, and detection of rare lesions can degrade sharply across sites. Most disease-specific evidence remains retrospective, although prospective evaluations in CNS tumours and autoimmune hepatitis show that the next level of evidence is achievable, and the hepatitis study also shows how much performance can fall outside the development cohort. Moving the field forward will depend less on larger models than on shared benchmarks, multicentre and federated collaboration, molecular supervision and prospective studies with clinically meaningful end points.

---

## Display items

### Figure 1 | From pathology foundation models to rare disease diagnosis: an overall framework.
Pretraining corpora (public cohorts, institutional real-world archives, pathology reports, rare disease registries and spatial or molecular omics; bottom) are used to train general-purpose pathology foundation models (self-supervised tile encoders, vision–language models and slide encoders; middle). A data-efficient adaptation layer (zero-shot prompting, prototype retrieval, linear probing and multiple-instance learning, parameter-efficient fine-tuning and full fine-tuning; upper) connects these models to clinical end points (top). The column on the right lists seven constraints that apply across all layers: label scarcity, domain shift, disease-spectrum shift, population bias, miscalibration, evidence gaps and access.

### Figure 2 | Data-efficient adaptation strategies for rare disease computational pathology.
**a**, Strategies positioned by labelling budget for the target disease (cases per class, log scale) and fraction of trainable parameters (log scale). The dashed arrow indicates how the most cost-effective strategy shifts as labelled cases accumulate. **b**, Qualitative comparison of strategies on six dimensions: labelling requirement, trainable parameters, cross-site robustness, interpretability, deployment cost and suitability for rare diseases. Ratings summarize the cited literature and are not measured on a common benchmark.

### Figure 3 | Domain shift in rare disease computational pathology.
**a**, Five sources of domain shift (staining and reagents, scanners and acquisition, centre and tissue processing, tissue type, and disease spectrum and population) and the mechanism by which scarce cases amplify their effect: few cases come from few centres; the model learns centre signatures as shortcuts; performance degrades unpredictably elsewhere. **b**, Reported out-of-distribution performance losses, distinguishing relative and absolute changes. Values are as reported in the original studies<sup>30,50,64</sup> and are not directly comparable across studies.

### Figure 4 | Evidence landscape for rare disease applications.
**a**, Disease group by evidence-maturity level (L0–L4; Box 1). Filled circles, independent external validation or prospective evaluation; open squares, internal retrospective validation only; grey crosses, feasibility inferred without disease-specific validation. Entries in the L0 band must not be described as established results. The L3 column contains two entries (CNS tumours<sup>79</sup> and autoimmune hepatitis<sup>87</sup>); the L4 column is empty. **b**, Key results by disease group with evidence level.

### Figure 5 | A staged pathway to trustworthy clinical translation.
Stages S0–S5 (technical development; internal validation; external validation; prospective silent evaluation; controlled evaluation of clinical utility; authorization, deployment and surveillance) are separated by gates annotated with typical failure modes. The rising staircase indicates that evidence strength and cost of translation increase together. Reporting guidelines, regulation and governance form a baseline across all stages. For rare disease histology, S3 has been reached for two disease groups, and S4–S5 have not yet been reached.

### Table 1 | Representative pathology foundation models

| Model | Type and backbone | Pretraining objective | Pretraining data (as reported) | Relevance to rare diseases |
|---|---|---|---|---|
| CTransPath<sup>22</sup> | Swin transformer + CNN tile encoder | Semantically relevant contrastive learning | ~15 million tiles | Early transfer baseline |
| UNI<sup>15</sup> | ViT-L tile encoder | DINOv2 | >100 million tiles from ~100,000 H&E slides, 20 tissue types | Few-shot prototype classification |
| Virchow / Virchow2<sup>16,24</sup> | ViT-H tile encoder (Virchow2G, 1.9 billion parameters) | DINOv2 with pathology-specific modifications | ~1.5 million / 3.1 million slides | Reported rare cancer detection (AUC 0.937 across seven rare cancers) |
| Prov-GigaPath<sup>17</sup> | ViT tile encoder + LongNet slide encoder | DINOv2 (tiles), masked autoencoding (slides) | 1.3 billion tiles from 171,189 slides | Whole-slide modelling on real-world data |
| Phikon / Phikon-v2<sup>18,23</sup> | ViT-B / ViT-L | iBOT / DINOv2 | Public data | Open, reproducible baselines |
| RudolfV / Atlas<sup>19,20</sup> | ViT | DINOv2-based | Includes immunohistochemistry and special stains; Atlas ~1.2 million slides | Reference-case retrieval; multi-stain coverage |
| CONCH<sup>35</sup> | ViT + text encoder | Contrastive captioning | 1.17 million image–caption pairs | Zero-shot classification and retrieval |
| KEEP<sup>36</sup> | Vision–language with disease knowledge graph | Knowledge-enhanced contrastive learning | ~143,000 semantic groups; 11,454 diseases | Largest gains on rare subtypes |
| PathChat<sup>38</sup> | Vision encoder + large language model | Instruction tuning | Image–text pairs and instructions | Interactive differential diagnosis |
| TITAN<sup>33</sup> | Slide encoder | Visual self-supervision + report and synthetic caption alignment | 335,645 slides; 423,122 synthetic captions | Rare cancer retrieval without fine-tuning |
| PRISM<sup>123</sup> | Slide encoder + language decoder | Report-supervised contrastive captioning | Built on Virchow tile embeddings | Slide-level zero-shot classification and report generation |

Pretraining data are as reported by the developers. Model weights, licences and parameter counts are listed in Supplementary Table 1.

### Table 2 | Evidence matrix for rare disease applications (ordered by evidence level)

| Disease group | Representative work | Data (as reported) | Task and key result | Level |
|---|---|---|---|---|
| CNS tumours | Hetairos<sup>79</sup> | 9,606 patients, >11,000 slides, 11 centres, 4 continents | 102 methylation subtypes from H&E; accuracy 0.87 for highest-rated predictions; prospective routine evaluation, turnaround 12 days → 12 min | L3 |
| Rare glomerular lesions | Semi-supervised + domain adaptation<sup>64</sup> | 22 hospitals, 3 scanner types | Up to 70.3% loss of rare-lesion precision across domains; up to 63.4% recovery | L2 |
| Paediatric and rare cancers (incl. CNS) | PathPT with KEEP<sup>7</sup> | 11 datasets, 56 subtypes, 3,958 slides | Balanced accuracy 0.679 on 30-subtype EBRAINS, 10-shot | L1–L2 |
| Paediatric brain tumours | Foundation-model linear probes<sup>45</sup>; multi-stain fusion<sup>71</sup> | Multicentre Swedish cohort; CBTN | Foundation models ≫ ImageNet baseline; H&E + Ki-67 fusion improves accuracy | L2 (preprints) |
| Paediatric soft-tissue sarcoma | Multicentre foundation-model features<sup>80</sup> | 3 centres + Children's Oncology Group | Rhabdomyosarcoma vs non-rhabdomyosarcoma; alveolar vs embryonal | L2 (preprint) |
| Autoimmune hepatitis | AIOLI<sup>87</sup> | 402 development cases; external set of 185 | AUC 0.92 (development) vs 0.74 (external); prospective real-life testing | L3 |
| Peripheral T-cell lymphoma | UNI + transformer MIL<sup>83</sup> | 223 training slides; external cohort of 118 patients | Subtyping of ALCL, TFH, PTCL-NOS with independent validation | L2 (abstract) |
| Common lymphoma subtypes | MIL benchmark<sup>50</sup> | Multicentre | Balanced accuracy >80% ID → ~60% OOD | L2 (preprint) |
| B-cell lymphoma subtypes | LymphoVision<sup>27</sup> | 31,211 slides (pretraining) | Six-class AUC 0.98; recall 70.8% (MCL), 77.2% (MZL) | L1 (abstract) |
| Uterine leiomyosarcoma | Hybrid-view adaptive learning<sup>81</sup> | Single source | Near-perfect metrics | L1 |
| Rare renal tumours | Zero-shot classification<sup>84</sup> | Abstract | Multiclass zero-shot classification | L1 |
| Fabry nephropathy | ZEBRA<sup>86</sup> | Kidney biopsies | Score separates cases from controls; correlates with clinical markers | L1 |
| Urogenital schistosomiasis | Object detection<sup>91</sup> | Bladder histopathology | Egg detection | L1 |
| Bacterial granulomatous infections; ultra-rare paediatric tumours; ultra-rare lymphoma subtypes | — | — | No disease-specific validated models identified | L0 |

Results are as reported by the original authors and have not been re-analysed. Levels are defined in Box 1.

---

## References

1. Nguengang Wakap, S. et al. Estimating cumulative point prevalence of rare diseases: analysis of the Orphanet database. *Eur. J. Hum. Genet.* **28**, 165–173 (2020).
2. Haendel, M. et al. How many rare diseases are there? *Nat. Rev. Drug Discov.* **19**, 77–78 (2020).
3. Faye, F. et al. Time to diagnosis and determinants of diagnostic delays of people living with a rare disease: results of a Rare Barometer retrospective patient survey. *Eur. J. Hum. Genet.* **32**, 1116–1126 (2024).
4. 100,000 Genomes Project Pilot Investigators. 100,000 Genomes pilot on rare-disease diagnosis in health care — preliminary report. *N. Engl. J. Med.* **385**, 1868–1880 (2021).
5. Marwaha, S., Knowles, J. W. & Ashley, E. A. A guide for the diagnosis of rare and undiagnosed disease: beyond the exome. *Genome Med.* **14**, 23 (2022).
6. Gatta, G. et al. Burden and centralised treatment in Europe of rare tumours: results of RARECAREnet—a population-based study. *Lancet Oncol.* **18**, 1022–1039 (2017).
7. He, D. et al. Boosting pathology foundation models via few-shot prompt-tuning for rare cancer subtyping. *Nat. Commun.* **17**, 5058 (2026).
8. Ray-Coquard, I. et al. Sarcoma: concordance between initial diagnosis and centralized expert review in a population-based study within three European regions. *Ann. Oncol.* **23**, 2442–2449 (2012).
9. Capper, D. et al. DNA methylation-based classification of central nervous system tumours. *Nature* **555**, 469–474 (2018).
10. Koelsche, C. et al. Sarcoma classification by DNA methylation profiling. *Nat. Commun.* **12**, 498 (2021).
11. Wilson, M. L. et al. Access to pathology and laboratory medicine services: a crucial gap. *Lancet* **391**, 1927–1938 (2018).
12. Moor, M. et al. Foundation models for generalist medical artificial intelligence. *Nature* **616**, 259–265 (2023).
13. Song, A. H. et al. Artificial intelligence for digital and computational pathology. *Nat. Rev. Bioeng.* **1**, 930–949 (2023).
14. Oquab, M. et al. DINOv2: learning robust visual features without supervision. *Trans. Mach. Learn. Res.* https://openreview.net/forum?id=a68SUt6zFt (2024).
15. Chen, R. J. et al. Towards a general-purpose foundation model for computational pathology. *Nat. Med.* **30**, 850–862 (2024).
16. Vorontsov, E. et al. A foundation model for clinical-grade computational pathology and rare cancers detection. *Nat. Med.* **30**, 2924–2935 (2024).
17. Xu, H. et al. A whole-slide foundation model for digital pathology from real-world data. *Nature* **630**, 181–188 (2024).
18. Filiot, A. et al. Phikon-v2, a large and public feature extractor for biomarker prediction. Preprint at https://arxiv.org/abs/2409.09173 (2024).
19. Dippel, J. et al. RudolfV: a foundation model by pathologists for pathologists. Preprint at https://arxiv.org/abs/2401.04079 (2024).
20. Alber, M. et al. Atlas: a novel pathology foundation model by Mayo Clinic, Charité, and Aignostics. Preprint at https://arxiv.org/abs/2501.05409 (2025).
21. Nechaev, D., Pchelnikov, A. & Ivanova, E. Hibou: a family of foundational vision transformers for pathology. Preprint at https://arxiv.org/abs/2406.05074 (2024).
22. Wang, X. et al. Transformer-based unsupervised contrastive learning for histopathological image classification. *Med. Image Anal.* **81**, 102559 (2022).
23. Filiot, A. et al. Scaling self-supervised learning for histopathology with masked image modeling. Preprint at *medRxiv* https://doi.org/10.1101/2023.07.21.23292757 (2023).
24. Zimmermann, E. et al. Virchow2: scaling self-supervised mixed magnification models in pathology. Preprint at https://arxiv.org/abs/2408.00738 (2024).
25. Wang, X. et al. A pathology foundation model for cancer diagnosis and prognosis prediction. *Nature* **634**, 970–978 (2024).
26. Ma, J. et al. A generalizable pathology foundation model using a unified knowledge distillation pretraining framework. *Nat. Biomed. Eng.* **10**, 545–564 (2026).
27. Seheult, J. et al. LymphoVision: a lymphoma-specialized foundation model for histology-based lymphoma classification and subtyping. *Blood* **146**, 117 (2025) (conference abstract).
28. Neidlinger, P. et al. Benchmarking foundation models as feature extractors for weakly supervised computational pathology. *Nat. Biomed. Eng.* **10**, 1113–1123 (2026).
29. Bareja, R. et al. A benchmark study of vision and pathology foundation models for computational pathology. *Nat. Commun.* **17**, 9012 (2026).
30. Kömen, J. et al. Towards robust foundation models for digital pathology. *Nat. Commun.* **17**, 5218 (2026).
31. Campanella, G. et al. A clinical benchmark of public self-supervised pathology foundation models. *Nat. Commun.* **16**, 3640 (2025).
32. Chen, R. J. et al. Scaling vision transformers to gigapixel images via hierarchical self-supervised learning. In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition* 16144–16155 (2022).
33. Ding, T. et al. A multimodal whole-slide foundation model for pathology. *Nat. Med.* **31**, 3749–3761 (2025).
34. Huang, Z., Bianchi, F., Yuksekgonul, M., Montine, T. J. & Zou, J. A visual–language foundation model for pathology image analysis using medical Twitter. *Nat. Med.* **29**, 2307–2316 (2023).
35. Lu, M. Y. et al. A visual-language foundation model for computational pathology. *Nat. Med.* **30**, 863–874 (2024).
36. Zhou, X. et al. Knowledge-enhanced pretraining for vision-language pathology foundation model on cancer diagnosis. *Cancer Cell* **44**, 777–791.e7 (2026).
37. Xiang, J. et al. A vision–language foundation model for precision oncology. *Nature* **638**, 769–778 (2025).
38. Lu, M. Y. et al. A multimodal generative AI copilot for human pathology. *Nature* **634**, 466–473 (2024).
39. Roetzer-Pejrimovsky, T. et al. The Digital Brain Tumour Atlas, an open histopathology resource. *Sci. Data* **9**, 55 (2022).
40. Lu, M. Y. et al. Visual language pretrained multiple instance zero-shot transfer for histopathology images. In *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition* 19764–19775 (2023).
41. Kalra, S. et al. Yottixel – An Image Search Engine for Large Archives of Histopathology Whole Slide Images. *Med. Image Anal.* **65**, 101757 (2020).
42. Hegde, N. et al. Similar image search for histopathology: SMILY. *npj Digit. Med.* **2**, 56 (2019).
43. Chen, C. et al. Fast and scalable search of whole-slide images via self-supervised deep learning. *Nat. Biomed. Eng.* **6**, 1420–1434 (2022).
44. Lee, J., Lim, J., Byeon, K. & Kwak, J. T. Benchmarking pathology foundation models: Adaptation strategies and scenarios. *Comput. Biol. Med.* **190**, 110031 (2025).
45. Tampu, I. E. et al. Pediatric brain tumor classification using digital histopathology and deep learning: evaluation of SOTA methods on a multi-center Swedish cohort. Preprint at https://arxiv.org/abs/2409.01330 (2024).
46. Ilse, M., Tomczak, J. & Welling, M. Attention-based deep multiple instance learning. In *Proc. 35th International Conference on Machine Learning* 2127–2136 (PMLR, 2018).
47. Lu, M. Y. et al. Data-efficient and weakly supervised computational pathology on whole-slide images. *Nat. Biomed. Eng.* **5**, 555–570 (2021).
48. Shao, Z. et al. TransMIL: transformer based correlated multiple instance learning for whole slide image classification. In *Advances in Neural Information Processing Systems* **34**, 2136–2147 (2021).
49. Campanella, G. et al. Clinical-grade computational pathology using weakly supervised deep learning on whole slide images. *Nat. Med.* **25**, 1301–1309 (2019).
50. Umer, R. M. et al. A multicenter benchmark of multiple instance learning models for lymphoma subtyping from H&E-stained whole slide images. Preprint at https://arxiv.org/abs/2512.14640 (2025).
51. Ganz, J. et al. Is self-supervision enough? Benchmarking foundation models against end-to-end training for mitotic figure classification. In *Bildverarbeitung für die Medizin 2025* 63–68 (Springer Vieweg, 2025).
52. Kasireddy, H. R. et al. A comprehensive benchmark of histopathology foundation models for kidney digital pathology images. Preprint at https://arxiv.org/abs/2603.15967 (2026).
53. Hu, E. J. et al. LoRA: low-rank adaptation of large language models. In *Proc. International Conference on Learning Representations* (2022).
54. Jia, M. et al. Visual prompt tuning. In *Computer Vision – ECCV 2022* 709–727 (Springer, 2022).
55. Zhou, K., Yang, J., Loy, C. C. & Liu, Z. Learning to Prompt for Vision-Language Models. *Int. J. Comput. Vis.* **130**, 2337–2348 (2022).
56. Ramchandani, L. et al. Parameter-efficient fine-tuning (PEFT) of vision foundation models for atypical mitotic figure classification. Preprint at https://arxiv.org/abs/2509.16935 (2025).
57. Lin, Y. et al. Prompt-guided foundation model tuning for pathology image classification. Preprint at https://arxiv.org/abs/2403.12537 (2024).
58. Campanella, G. et al. Real-world deployment of a fine-tuned pathology foundation model for lung cancer biomarker detection. *Nat. Med.* **31**, 3002–3010 (2025).
59. Howard, F. M. et al. The impact of site-specific digital histology signatures on deep learning model accuracy and bias. *Nat. Commun.* **12**, 4423 (2021).
60. Tellez, D. et al. Quantifying the effects of data augmentation and stain color normalization in convolutional neural networks for computational pathology. *Med. Image Anal.* **58**, 101544 (2019).
61. Bandi, P. et al. From Detection of Individual Metastases to Classification of Lymph Node Status at the Patient Level: The CAMELYON17 Challenge. *IEEE Trans. Med. Imaging* **38**, 550–560 (2019).
62. de Jong, E. D., Marcus, E. & Teuwen, J. Current pathology foundation models are unrobust to medical center differences. Preprint at https://arxiv.org/abs/2501.18055 (2025).
63. Kömen, J. et al. Do histopathological foundation models eliminate batch effects? A comparative study. Preprint at https://arxiv.org/abs/2411.05489 (2024).
64. Matsui, I. et al. Domain-adaptive semi-supervised learning for efficient rare pathological lesion detection with minimal annotation. *npj Digit. Med.* **8**, 778 (2025).
65. Khan, U. et al. Staining normalization in histopathology: Method benchmarking using multicenter dataset. *Sci. Rep.* **16**, 11097 (2026).
66. Wang, J. et al. Self-supervised stain normalization empowers privacy-preserving and model generalization in digital pathology. *npj Digit. Med.* **9**, 22 (2026).
67. Huang, Y. et al. Knowledge-guided adaptation of pathology foundation models effectively improves cross-domain generalization and demographic fairness. *Nat. Commun.* **16**, 11485 (2025).
68. Lou, S. et al. Uncertainty-aware and causal test-time adaptive foundation model for robust colorectal cancer pathology diagnosis. *npj Digit. Med.* **8**, 784 (2025).
69. Zhu, X., Jiang, Z., Wu, K., Shi, J. & Zheng, Y. Adapting pathology foundation models for continual cross-center WSI retrieval. *Med. Image Anal.* **113**, 104213 (2026).
70. Bahumanya, R. G., Harshith, V. M. & Gowda, S. N. Explanation stability of test-time adaptation in computational pathology: a large-scale benchmark. Preprint at https://arxiv.org/abs/2608.07062 (2026).
71. Spyretos, C. et al. Multi-stain fusion of histopathology images using deep learning for pediatric brain tumor classification. Preprint at *bioRxiv* https://doi.org/10.64898/2026.04.10.717785 (2026).
72. Kleppe, A. et al. Designing deep learning studies in cancer diagnostics. *Nat. Rev. Cancer* **21**, 199–211 (2021).
73. Grisi, C., van der Laak, J. & Litjens, G. A distributional robustness margin for pathology foundation models. Preprint at https://arxiv.org/abs/2607.25497 (2026).
74. Collins, G. S. et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ* **385**, e078378 (2024).
75. Sounderajah, V. et al. The STARD-AI reporting guideline for diagnostic accuracy studies using artificial intelligence. *Nat. Med.* **31**, 3283–3289 (2025).
76. Vasey, B. et al. Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI. *Nat. Med.* **28**, 924–933 (2022).
77. Liu, X. et al. Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. *Nat. Med.* **26**, 1364–1374 (2020).
78. Gallifant, J. et al. The TRIPOD-LLM reporting guideline for studies using large language models. *Nat. Med.* **31**, 60–69 (2025).
79. Jin, D. et al. Hetairos is a histology-based artificial intelligence model for predicting central nervous system tumor methylation subtypes. *Nat. Cancer* **7**, 884–898 (2026).
80. Thiesen, A. et al. Multicenter Histology Image Integration and Multiscale Deep Learning for Machine Learning-Enabled Pediatric Sarcoma Classification. Preprint at *medRxiv* https://doi.org/10.1101/2025.06.10.25328700 (2025).
81. Li, Q., Wu, J., Liu, X., Li, D. & Xue, J. Uncertainty-driven hybrid-view adaptive learning for fully automated uterine leiomyosarcoma diagnosis. *Med. Image Anal.* **105**, 103692 (2025).
82. Cross, W. C. The diagnostic landscape of bone and soft tissue sarcoma: the pan-sarcoma era and AI-driven classification. *J. Pathol. Clin. Res.* **11**, e70054 (2025).
83. Bernhardt, S. et al. Deep learning-based histopathological subtyping of peripheral T-cell lymphoma (PTCL) on H&E-stained whole slide images. *Blood* **146**, 1784 (2025) (conference abstract).
84. Gondim, D., Cheng, L., Idrees, M. & Gondim, M. D. B. D. Zero-shot multiclass renal neoplasm classification leveraging foundational model embeddings. *Lab. Invest.* **105**, 103043 (2025) (abstract 810).
85. Lu, M. Y. et al. AI-based pathology predicts origins for cancers of unknown primary. *Nature* **594**, 106–110 (2021).
86. Cazzaniga, G. et al. Zebra bodies recognition by artificial intelligence (ZEBRA): a computational tool for Fabry nephropathy. *Sci. Rep.* **16**, 5072 (2026).
87. Allaume, P. et al. High performance deep-learning model for the diagnosis of auto-immune hepatitis based on histological whole slide images. *Virchows Arch.* https://doi.org/10.1007/s00428-026-04621-z (2026).
88. Rubin, D. T. et al. Deployment of an Artificial Intelligence Histology Tool to Aid Qualitative Assessment of Histopathology Using the Nancy Histopathology Index in Ulcerative Colitis. *Inflamm. Bowel Dis.* **31**, 1630–1636 (2025).
89. Das, A. et al. Deep Learning for Classification of Inflammatory Bowel Disease Activity in Whole Slide Images of Colonic Histopathology. *Am. J. Pathol.* **195**, 680–689 (2025).
90. Fang, S.-S. & Chen, S. Artificial intelligence in rare neurological diseases: a scoping review of the evidence landscape and framework for foundation model integration. *Egypt. J. Neurol. Psychiatry Neurosurg.* **62**, 147 (2026).
91. Detection of *Schistosoma* eggs using an AI-based deep learning model on urinary bladder histopathology images. *J. Coll. Physicians Surg. Pak.* **35**, 1385–1390 (2025).
92. Moons, K. G. M. et al. PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods. *BMJ* **388**, e082505 (2025).
93. Olsson, H. et al. Estimating diagnostic uncertainty in artificial intelligence assisted pathology using conformal prediction. *Nat. Commun.* **13**, 7761 (2022).
94. Lysenkova Wiklander, M., Zachariah, D., Krali, O. & Nordlund, J. Error reduction in leukemia machine learning classification with conformal prediction. *JCO Clin. Cancer Inform.* **9**, e2400324 (2025).
95. Zhang, X. et al. Implementing trust in non-small cell lung cancer diagnosis with a conformalized uncertainty-aware AI framework. *Nat. Biomed. Eng.* https://doi.org/10.1038/s41551-026-01694-8 (2026).
96. Kladny, K.-R., Schölkopf, B., Koch, L., Baumgartner, C. F. & Muehlebach, M. A critical perspective on finite sample conformal prediction theory in medical applications. *Artif. Intell. Med.* **180**, 103462 (2026).
97. Vaidya, A. et al. Demographic bias in misdiagnosis by computational pathology models. *Nat. Med.* **30**, 1174–1190 (2024).
98. Chen, R. J. et al. Algorithmic fairness in artificial intelligence for medicine and healthcare. *Nat. Biomed. Eng.* **7**, 719–742 (2023).
99. Lee, Y. et al. Benchmarking vision-language models for automated pathology diagnosis and report generation. Preprint at https://arxiv.org/abs/2609.00866 (2026).
100. Chen, M., Meng, Z. & Su, F. PathGLS: evaluating pathology vision-language models without ground truth through multi-dimensional consistency. Preprint at https://arxiv.org/abs/2603.16113 (2026).
101. Cruz Rivera, S. et al. Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension. *Nat. Med.* **26**, 1351–1363 (2020).
102. US Food and Drug Administration. De Novo classification request for Paige Prostate (DEN200080). https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN200080.pdf (2021).
103. Raciti, P. et al. Novel artificial intelligence system increases the detection of prostate cancer in whole slide images of core needle biopsies. *Mod. Pathol.* **33**, 2058–2066 (2020).
104. US Food and Drug Administration. Marketing submission recommendations for a predetermined change control plan for artificial intelligence-enabled device software functions. Final guidance (December 2024).
105. European Parliament and Council of the European Union. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). *Off. J. Eur. Union* L 2024/1689 (2024).
106. Lång, K. et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. *Lancet Oncol.* **24**, 936–944 (2023).
107. Hernström, V. et al. Screening performance and characteristics of breast cancer detected in the Mammography Screening with Artificial Intelligence trial (MASAI): a randomised, controlled, parallel-group, non-inferiority, single-blinded, screening accuracy study. *Lancet Digit. Health* **7**, e175–e183 (2025).
108. AI-assisted pathologist performance improvement: a multicenter, prospective, randomized controlled trial. *ClinicalTrials.gov* https://clinicaltrials.gov/study/NCT07291362 (2025).
109. Human-AI collaborative INSIGHT diagnostic workflow for breast cancer with extensive intraductal component. *ClinicalTrials.gov* https://clinicaltrials.gov/study/NCT07060599 (2025).
110. AI-based DeepGEM tool for predicting gene mutations in NSCLC patients: a randomized controlled study. *ClinicalTrials.gov* https://clinicaltrials.gov/study/NCT07110259 (2025).
111. Da, Q. et al. Computational pathology in the era of emerging foundation and agentic AI—international expert perspectives on clinical integration and translational readiness. Preprint at https://arxiv.org/abs/2603.05884 (2026).
112. Pati, S. et al. Federated learning enables big data for rare cancer boundary detection. *Nat. Commun.* **13**, 7346 (2022).
113. Schoenpflug, L. A., Nie, Y., Sheikhzadeh, F. & Koelzer, V. H. A review on federated learning in computational pathology. *Comput. Struct. Biotechnol. J.* **23**, 3938–3945 (2024).
114. Brull, A. et al. Training together, diagnosing better: federated learning for collagen VI-related dystrophies. Preprint at https://arxiv.org/abs/2512.16876 (2025).
115. Jaume, G. et al. HEST-1k: a dataset for spatial transcriptomics and histology image analysis. In *Advances in Neural Information Processing Systems* **37**, 53798–53833 (2024).
116. Schmauch, B. et al. A deep learning-based multiscale integration of spatial omics with tumor morphology. *Nat. Commun.* **16**, 11674 (2025).
117. Hemker, K. et al. Towards spatial transcriptomics-driven pathology foundation models. Preprint at https://arxiv.org/abs/2602.14177 (2026).
118. Zhang, P., Gao, C., Hua, K., Zhang, Z. & Li, S. Systematically decoding pathological morphologies and molecular profiles with unified multimodal embedding. *Nat. Methods* **23**, 903–908 (2026).
119. Alsentzer, E. et al. Few shot learning for phenotype-driven diagnosis of patients with rare genetic diseases. *npj Digit. Med.* **8**, 380 (2025).
120. Qi, G. et al. RareCollab: an LLM-powered framework for multimodal reasoning in Mendelian disease diagnosis. Preprint at https://arxiv.org/abs/2602.04058 (2026).
121. Tizhoosh, H. R. Rethinking foundation models in pathology. *Nat. Biomed. Eng.* **10**, 1513–1518 (2026).
122. Bai, J. et al. AI-assisted cervical cytology precancerous screening for high-risk population in resource-limited regions using a compact microscope. *Nat. Commun.* **16**, 7429 (2025).
123. Shaikovski, G. et al. PRISM: a multi-modal generative foundation model for slide-level histopathology. Preprint at https://arxiv.org/abs/2405.10254 (2024).

---

## Acknowledgements

[To be completed by the authors.]

## Author contributions

[To be completed using the CRediT taxonomy, for example: Conceptualization, A.B.; Literature search and screening, A.B., C.D.; Writing – original draft, A.B.; Writing – review and editing, all authors; Supervision, E.F.]

## Competing interests

[To be completed. All authors must declare financial and non-financial competing interests, including employment by, consultancy for, or equity in companies developing pathology AI or foundation models discussed in this Review.]

## Use of AI-assisted technologies

[To be completed and verified by the authors.] An earlier draft of this manuscript was generated with the assistance of an AI writing system. Large language model tools were also used to check references against Crossref and arXiv metadata and to edit the English text. The authors reviewed all content, verified every cited source and take full responsibility for the manuscript. AI tools are not listed as authors, in line with Nature Portfolio policy.

## Additional information

**Supplementary information** (search strategy and screening criteria; list of included studies; Supplementary Table 1, full model inventory with licences; Supplementary Table 2, domain-shift mitigation strategies; Supplementary Table 3, trustworthiness requirements) is available for this paper.

**Correspondence** should be addressed to [corresponding author].
