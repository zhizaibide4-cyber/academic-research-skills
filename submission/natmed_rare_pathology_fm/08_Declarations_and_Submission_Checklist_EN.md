# Declarations and submission checklist

## Part A. Declarations to insert into the manuscript

### Author contributions (CRediT)

[Example, to be replaced:] A.B. conceived the Review. A.B. and C.D. performed the literature search and screening. A.B. wrote the original draft. C.D., E.F. and G.H. contributed domain expertise in rare tumour pathology, rare disease registries and AI regulation, respectively. All authors reviewed and edited the manuscript and approved the final version. E.F. supervised the work.

### Competing interests

[Choose one and complete:]
- "The authors declare no competing interests."
- "[Author] is an employee of / consultant for / holds equity in [company], which develops [product]. [Author] has received research funding from [company]. The remaining authors declare no competing interests."

Disclose any relationship with developers of models discussed in the Review (for example Paige, Microsoft/Providence, Owkin, Aignostics, Bioptimus, HistAI or academic groups whose models are evaluated).

### Funding

[Funder name, grant number and recipient for each grant.] If the funders had no role, state: "The funders had no role in the design, literature selection, interpretation or writing of this Review."

### Use of AI-assisted technologies

[Verify and adapt:] "An earlier draft of this manuscript was produced with the assistance of an AI writing system. Large language model tools were also used to check references against Crossref, arXiv and ClinicalTrials.gov metadata and to edit the English text. The authors reviewed and verified all content and references and take full responsibility for the manuscript. No AI tool is listed as an author."

### Data availability

"No new data were generated or analysed in this Review. The literature search strategy is provided in Supplementary Information."

### Peer review information

[Completed by the journal.]

---

## Part B. Pre-submission checklist

### Policy and eligibility

- [ ] All authors are human, meet authorship criteria and approved the submission; no AI tool is listed as an author.
- [ ] AI use is disclosed in the manuscript.
- [ ] A presubmission enquiry has been sent (`05_Presubmission_Enquiry_EN.md`) and an editor has invited a full submission.
- [ ] Current *Nature Medicine* Review guidelines (length, display items, reference limit) have been checked on the journal website on the submission date.

### Manuscript

- [ ] Title is concise and contains no unexplained abbreviations.
- [ ] Abstract is about 150 words and contains no references (currently 147 words).
- [ ] Main text is within the current limit (currently about 4,900 words, excluding boxes, legends, tables and references).
- [ ] Every abbreviation is defined at first use.
- [ ] British spelling is used throughout.
- [ ] Section headings are short and informative.

### References

- [ ] References are numbered in order of first citation and formatted in Nature style.
- [ ] Every reference has been checked against its DOI, arXiv or registry record (see `03_参考文献核查表_Reference_Audit_ZH.md`).
- [ ] Preprints and conference abstracts are labelled; their necessity has been reconsidered.
- [ ] No news articles, press releases or blogs are cited for factual claims.
- [ ] Figure legends and tables cite only references that also appear in the main text.

### Display items

- [ ] Figures 1–5 have been redrawn following `04_修改说明与逐条回应_Revision_Response_ZH.md` (Part III), in particular the L3 entries in Fig. 4 and the S3 annotation in Fig. 5.
- [ ] Figures are supplied as vector files or as TIFF files at ≥300 dpi, with text ≥5 pt and colour-blind-safe palettes.
- [ ] Any third-party image has a reuse licence.
- [ ] Tables 1 and 2 are editable (not images).
- [ ] Supplementary Tables 1–3 are complete.

### Files to upload

| File | Source in this package |
|---|---|
| Cover letter | `06_Cover_Letter_EN.md` |
| Manuscript (main text, boxes, legends, tables, references) | `02_Manuscript_NatMed_Review_EN.md`, converted to Word |
| Figures 1–5 (separate files) | To be redrawn by the authors |
| Supplementary Information | `07_Supplementary_Information_EN.md`, converted to PDF |
| Competing interests and author information | Part A of this file |

### Conversion

To convert Markdown to Word with Pandoc:

```bash
pandoc 02_Manuscript_NatMed_Review_EN.md -o Manuscript.docx
pandoc 07_Supplementary_Information_EN.md -o Supplementary_Information.docx
```
