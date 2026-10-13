# Presubmission enquiry — *Nature Medicine* (Review)

**To:** The Editors, *Nature Medicine*
**From:** [Corresponding author name, title, institution, e-mail, ORCID]
**Date:** [Date]
**Proposed article type:** Review

---

## Proposed title

Pathology foundation models for rare disease diagnosis: data-efficient adaptation, cross-site robustness and the evidence gap

## Summary of the proposal (about 200 words)

Pathology foundation models pretrained on up to millions of whole-slide images are increasingly presented as a solution for diseases with few labelled cases, and rare diseases are the most frequently cited example. Yet no review has asked what the evidence actually shows for rare diseases: which adaptation strategies work when only a handful of cases per class are available, how much performance is lost when models move between hospitals, and how far disease-specific applications have progressed toward clinical use.

We propose a Review that answers these three questions. We introduce an explicit five-level evidence-maturity scale (L0 inferred feasibility to L4 demonstrated clinical utility or authorization) and apply it to rare tumours, non-neoplastic rare diseases and rare infections. The Review shows that the first prospective evaluations have now been reported, for central nervous system tumours and autoimmune hepatitis, but that no study has yet demonstrated benefit to patients. It also shows that current models encode the medical centre of origin strongly enough that it can be predicted from their embeddings. We close with a minimum reporting checklist and eight priority questions for researchers, regulators and funders.

## Why *Nature Medicine*

- The topic sits at the intersection of two areas the journal publishes extensively: pathology foundation models (several landmark models, including UNI, CONCH, Virchow and TITAN, were published in *Nature Medicine*) and rare diseases.
- The Review is written for clinicians, pathologists and policymakers as well as for computational scientists, and its central contribution, a disease-by-disease grading of evidence maturity, is directly relevant to clinical and regulatory decisions.
- It complements rather than duplicates existing technical reviews of computational pathology, which do not focus on rare diseases or grade disease-specific evidence.

## Proposed structure

1. Introduction: the rare disease diagnostic problem and the role of histopathology
2. Building blocks of pathology foundation models, including the evidence on scale versus data diversity
3. Data-efficient adaptation for rare diseases (zero-shot, retrieval, linear probing, MIL, parameter-efficient and prompt tuning, full fine-tuning)
4. Cross-site robustness: sources of domain shift, quantified losses and mitigation
5. Applications in rare diseases, graded by evidence maturity
6. From discrimination to clinical evidence: calibration, bias, generative risks, reporting standards, regulation and prospective studies
7. Outlook: federated collaboration, molecular supervision, knowledge graphs, rare diseases as a stress test, global access

**Display items:** 5 figures, 2 tables and 3 boxes (definitions and evidence levels; minimum reporting checklist; priority open questions).
**Length:** about 4,900 words of main text, about 120 references.

## Representative references

1. Vorontsov, E. et al. A foundation model for clinical-grade computational pathology and rare cancers detection. *Nat. Med.* **30**, 2924–2935 (2024).
2. He, D. et al. Boosting pathology foundation models via few-shot prompt-tuning for rare cancer subtyping. *Nat. Commun.* **17**, 5058 (2026).
3. Kömen, J. et al. Towards robust foundation models for digital pathology. *Nat. Commun.* **17**, 5218 (2026).
4. Jin, D. et al. Hetairos is a histology-based artificial intelligence model for predicting central nervous system tumor methylation subtypes. *Nat. Cancer* **7**, 884–898 (2026).
5. Campanella, G. et al. Real-world deployment of a fine-tuned pathology foundation model for lung cancer biomarker detection. *Nat. Med.* **31**, 3002–3010 (2025).
6. Neidlinger, P. et al. Benchmarking foundation models as feature extractors for weakly supervised computational pathology. *Nat. Biomed. Eng.* **10**, 1113–1123 (2026).

## Authors

[List the authors with one-sentence descriptions of their expertise relevant to the proposal, for example computational pathology, paediatric and rare tumour pathology, rare disease registries, and AI regulation.]

## Competing interests

[Declare any relevant competing interests.]
