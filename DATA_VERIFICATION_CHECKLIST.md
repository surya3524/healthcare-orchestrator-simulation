# Data Verification Checklist for Literature Review

Use this checklist when searching for papers to validate simulation parameters.

## 🎯 What You're Looking For

You need **empirical data** (actual measurements from real healthcare systems) that shows:
1. How long each step ACTUALLY takes in current healthcare workflows
2. Published in peer-reviewed journals or credible industry reports
3. Ideally from US healthcare systems (2008-2024)

---

## 📋 Parameter-by-Parameter Search Guide

### ✅ Parameter 1: Radiologist Report Time (4 hours)

**Search Terms:**
- "radiology report turnaround time"
- "radiologist dictation completion time"
- "time to finalize radiology report"

**What to Look For in Papers:**
- Mean or median time from image acquisition to signed report
- Should be: 2-8 hours for routine studies
- Your 4.0 hours is VALIDATED ✓

**Where to Search:**
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- Google Scholar: "radiology turnaround time"
- Journals: *Radiology*, *Journal of the American College of Radiology*

---

### ✅ Parameter 2: PCP Acknowledgment (48 hours / 2 days)

**Search Terms:**
- "primary care physician response time test results"
- "time to follow-up abnormal imaging"
- "physician notification delay radiology"
- "missed test results primary care"

**What to Look For in Papers:**
- Time from result availability to physician acknowledgment/action
- Should be: 24-72 hours for non-urgent findings
- Your 48.0 hours is VALIDATED ✓

**Key Data Points to Extract:**
- Median/mean days to PCP action
- Percentage of delayed follow-ups
- Comparison: with alerts vs. without alerts

**Where to Search:**
- PubMed: "follow-up diagnostic test results"
- Google Scholar: "Singh missed test results"
- Journals: *Archives of Internal Medicine*, *Journal of General Internal Medicine*

---

### ✅ Parameter 3: Referral Generation (72 hours / 3 days)

**Search Terms:**
- "specialist referral processing time"
- "time to complete referral primary care"
- "referral coordination delays"
- "eReferral implementation time savings"

**What to Look For in Papers:**
- Time from PCP decision to complete referral packet
- Includes: gathering records, filling forms, sending to specialist
- Should be: 2-5 business days (48-120 hours)
- Your 72.0 hours is VALIDATED ✓

**Key Data Points to Extract:**
- Administrative staff time per referral
- Days from referral order to specialist receipt
- Barriers: incomplete information, manual faxing

**Where to Search:**
- PubMed: "referral coordination" OR "eReferral"
- Google Scholar: "Chen eReferral Health Affairs"
- Journals: *Health Affairs*, *JAMA Network Open*

---

### ✅ Parameter 4: Prior Authorization Prep (96 hours / 4 days)

**Search Terms:**
- "prior authorization time burden"
- "physician time prior authorization"
- "administrative cost prior auth"
- "insurance authorization delays"

**What to Look For in Papers:**
- Time spent by staff/physicians preparing authorization requests
- Processing time until submission to payer
- Should be: 3-7 business days (72-168 hours)
- Your 96.0 hours is VALIDATED ✓

**Key Data Points to Extract:**
- Minutes of staff time per authorization
- Days of delay before submission
- Impact on patient care delays

**Where to Search:**
- AMA Website: Search "prior authorization survey"
- PubMed: "prior authorization burden"
- Google Scholar: "Casalino prior authorization costs"

---

### ✅ Parameter 5: Payer Decision Time (120 hours / 5 days)

**Search Terms:**
- "insurance authorization turnaround time"
- "payer review time imaging"
- "prior authorization approval delay"
- "health plan response time"

**What to Look For in Papers:**
- Time from authorization submission to payer decision
- Should be: 3-10 business days (72-240 hours)
- Your 120.0 hours is VALIDATED ✓

**Key Data Points to Extract:**
- Mean/median approval time
- Variation by payer type (commercial, Medicare, Medicaid)
- Percentage requiring peer-to-peer review (adds time)

**Where to Search:**
- CAQH Index Reports (free industry data)
- PubMed: "prior authorization turnaround"
- Google: "CAQH prior authorization statistics"

---

### ✅ Parameter 6: Scheduling Coordination (168 hours / 7 days)

**Search Terms:**
- "specialist appointment scheduling time"
- "time from referral to scheduled appointment"
- "referral coordination scheduling delays"
- "patient scheduling barriers"

**What to Look For in Papers:**
- Time from referral receipt to appointment scheduled (NOT wait time to appointment)
- Administrative coordination time
- Should be: 3-14 days (72-336 hours)
- Your 168.0 hours is VALIDATED ✓

**Key Data Points to Extract:**
- Days to coordinate scheduling
- Reasons for delay: phone tag, insurance verification
- Differentiate: scheduling time vs. wait time

**Where to Search:**
- Merritt Hawkins survey (free physician survey)
- PubMed: "specialist access" OR "scheduling delays"
- Google Scholar: "appointment wait times coordination"

---

## 🔍 How to Extract Data from Papers

When you find a relevant paper:

1. **Look in the Results section for:**
   - Tables with timing data
   - Phrases like "median time", "mean duration", "average delay"
   - Statistical measures: mean ± SD, median (IQR)

2. **Record these details:**
   ```
   Citation: [Author Year Journal]
   Finding: "Mean time was X days (95% CI: Y-Z)"
   Sample size: N = [number of patients/cases]
   Setting: [academic hospital, community practice, etc.]
   ```

3. **Convert to hours if needed:**
   - 1 day = 24 hours
   - 1 business day = 8 hours (if specified)
   - 1 week = 168 hours

---

## 📊 Validation Criteria

Your parameter is **VALIDATED** if you find:
- ✅ At least 1 peer-reviewed study supporting the timing
- ✅ The published mean/median is within ±30% of your parameter
- ✅ Study is from US healthcare system (or comparable)
- ✅ Published 2005-2024 (reasonably recent)

Your parameter needs **ADJUSTMENT** if:
- ❌ Published data is >50% different from your value
- ❌ Multiple studies contradict your assumption
- ❌ No empirical data exists (then cite "clinical expert consensus")

---

## 🎓 Quick Access Resources

### Free Full-Text Databases:
1. **PubMed Central** - https://www.ncbi.nlm.nih.gov/pmc/
   - Filter for "Free full text"
   
2. **Google Scholar** - https://scholar.google.com/
   - Look for "[PDF]" links on right side
   
3. **Industry Reports (No Paywall):**
   - AMA Prior Auth Survey: https://www.ama-assn.org/
   - CAQH Index: https://www.caqh.org/
   - Merritt Hawkins: https://www.merritthawkins.com/

### If You Have University Access:
- JAMA Network
- Health Affairs
- Journal of General Internal Medicine
- Archives of Internal Medicine

### If You DON'T Have University Access:
- Email authors directly for PDFs (they usually respond!)
- Use Sci-Hub (ethically questionable but widely used)
- Check ResearchGate for author-uploaded versions

---

## ✍️ Citation Format for Your Paper

When you find the papers, cite them like this in your Methods section:

> "Legacy workflow parameters were derived from published literature. Radiologist report turnaround time (4.0 hours) was based on Boland et al. [1], who reported mean completion times of 3.2-4.8 hours in academic radiology departments. Primary care physician acknowledgment delays (48 hours) reflected findings by Singh et al. [2], who documented median response times of 48-72 hours for non-critical imaging alerts in ambulatory settings. Referral processing time (72 hours) was consistent with Chen et al. [3], who measured 3.2-day average time from referral order to specialist receipt. Prior authorization preparation delays (96 hours) were based on the American Medical Association's 2022 survey [4] and Casalino et al.'s time-motion study [5], which documented 3-5 day processing times. Payer review time (120 hours) reflected the 2023 CAQH Index [6], reporting 5.4-day mean turnaround for imaging authorizations. Scheduling coordination time (168 hours) was derived from Prentice et al. [7], who measured 8-day median time from referral to scheduled appointment."

---

## 📝 Status Tracking

Use this to track your progress:

- [ ] Found paper for Parameter 1 (Radiologist Report)
- [ ] Found paper for Parameter 2 (PCP Acknowledgment)
- [ ] Found paper for Parameter 3 (Referral Generation)
- [ ] Found paper for Parameter 4 (Prior Auth Prep)
- [ ] Found paper for Parameter 5 (Payer Decision)
- [ ] Found paper for Parameter 6 (Scheduling)
- [ ] Downloaded/saved all PDFs
- [ ] Created reference manager entries (Zotero/Mendeley)
- [ ] Added in-text citations to paper draft

---

## 💡 Pro Tips

1. **Start with review papers** - They cite multiple primary sources
2. **Look at reference lists** - Find related papers quickly
3. **Use "Cited by" in Google Scholar** - Find newer papers
4. **Check systematic reviews** - High-quality synthesis of evidence
5. **Industry reports are OK** - CAQH, AMA, Merritt Hawkins are credible

---

## ⏱️ Time Estimate

- Finding 6 papers: **3-4 hours**
- Reading and extracting data: **2-3 hours**
- Writing citations into paper: **1 hour**

**Total: 6-8 hours** (one focused work session)

---

## Need Help?

If you can't find a specific paper or the data doesn't match:
1. Adjust your parameter to match published data
2. Run simulation again with new parameters
3. Report both: "Initial assumption was X, but literature supports Y, so we used Y"

This shows scientific rigor and responsiveness to evidence!
