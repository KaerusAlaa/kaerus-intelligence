# Kaerus Intelligence

**Status: in development.** The method is defined and work on the tools has
just started. No results or notes have been published yet. This page will be
updated as things progress.

An open-source tool and public notes following how AI is changing drug
regulation in oncology: marketing authorisations, clinical trials, and the
guidance that regulators such as the EMA and the FDA publish on AI/ML.

## The question

When AI contributes to the evidence behind an oncology medicine, what do
regulators accept, discuss or reject, and why? The European Medicines Agency
(EMA) and its CHMP are the main reference. The US FDA is used as a
counterpoint.

## Scope

- Oncology medicines assessed by the EMA, mainly since 2024, with 2020 to
  2023 used for comparison.
- Any use of AI that produces or supports evidence in the dossier: trial
  design, patient selection, endpoints, real-world data, pharmacovigilance,
  manufacturing. Companion diagnostics are included when they condition the
  prescription.
- Out of scope: AI as a stand-alone medical device.

## Method

1. **Screening.** Every oncology EPAR in the period is searched for
   AI-related terms. Each result is logged, negatives included.
2. **Case files.** Each positive dossier is described with a common grid:
   context of use, purpose of the AI, position of the regulator, arguments of
   the applicant and objections of the regulator, quoted with page numbers.
   Where possible, the corresponding FDA review is checked.
3. **Notes.** Findings are summarised in a quarterly note.

Every statement is traceable to a public document and page. Only published
documents are used. The field is moving quickly, so each note reflects what
was public at its date.

## What is public

- the collection and screening scripts
- the method and the headings of the analysis grid
- the screening log, in aggregate form
- quarterly notes, with selected examples

The full set of case files is not published for now.

## Sources

- Primary: EMA European public assessment reports (EPARs), FDA approval
  documents (Drugs@FDA), EMA and FDA publications on AI.
- Secondary: ClinicalTrials.gov, PubMed.

## Roadmap

1. Learning the tools on a first data source (ClinicalTrials.gov API)
2. List of oncology EPARs since 2024
3. Automated screening of EPAR text, with a screening log
4. Case files and FDA counterpart
5. First note and full documentation
6. Comparison with 2020 to 2023

## About

Personal project by Alaa, a PharmD student working towards regulatory
affairs. I am learning Python while building it, so the code stays simple,
and I say clearly what works and what does not.

This is an independent, educational project. It is not affiliated with the
EMA or the FDA and is not regulatory advice.

Licence: to be chosen at the first release.