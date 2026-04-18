# Submission Guide - Zindi African Trust & Safety LLM Challenge

## Quick Start (5 Minutes)

### 1. Submit to Zindi
1. Go to https://zindi.africa/competitions/the-african-trust-safety-llm-challenge/submit
2. Upload: `outputs/Zindi_Submission_v6_NATLaS.md`
3. **IMPORTANT:** Mark this submission as "For Final Evaluation" ✓
4. Submit

### 2. Verify Submission
After uploading, verify your submission includes:
- [ ] 17 attacks across 4 languages
- [ ] All prompts have English translations
- [ ] All risk categories from official taxonomy
- [ ] All attacks show model responses with harmful content

---

## File Checklist

### Required for Submission
| File | Location | Status |
|------|----------|--------|
| **Main Submission** | `outputs/Zindi_Submission_v6_NATLaS.md` | ✅ Ready |
| **Validation Data** | `outputs/*.json` (6 files) | ✅ Ready |
| **Reproducibility Script** | `REPRODUCIBILITY_CHECK.py` | ✅ Ready |

### Required for Code Review (if Top 10)
| File | Location | Status |
|------|----------|--------|
| **Review Package** | `review_package/` | ✅ Ready |
| **Documentation** | `review_package/REPRODUCIBILITY.md` | ✅ Ready |
| **Review Guide** | `review_package/REVIEW_GUIDE.md` | ✅ Ready |
| **Project README** | `review_package/PROJECT_README.md` | ✅ Ready |

---

## Submission Summary

### Statistics
- **Total Attacks:** 17
- **Models Tested:** 2 (Pawa-Gemma-Swahili-2B, N-ATLaS)
- **Languages:** 4 (Swahili, Hausa, Yoruba, Igbo)
- **Risk Categories:** 9
- **Validation Rate:** 100% (17/17 confirmed at ≥2/3 reruns)

### Attack Distribution
| Model | Language | Attacks | Categories |
|-------|----------|---------|------------|
| Pawa-Gemma-Swahili-2B | Swahili | 12 | 9 |
| N-ATLaS | Hausa | 2 | 2 |
| N-ATLaS | Yoruba | 2 | 2 |
| N-ATLaS | Igbo | 1 | 1 |

### Risk Categories Covered
1. **cybersecurity** (6 attacks)
2. **illegal_activity** (3 attacks)
3. **privacy_data_leakage** (2 attacks)
4. **harmful_instructions** (1 attack)
5. **extremism** (1 attack)
6. **self_harm** (1 attack)
7. **violence** (1 attack)
8. **bias_discrimination** (1 attack)
9. **prompt_injection_policy_evasion** (1 attack)

---

## Reproducibility Verification

### Quick Test (5 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Run reproducibility check
python REPRODUCIBILITY_CHECK.py
```

### Expected Output
```
Total Attacks Tested: 17
Confirmed Breaks: 17/17
Reproducibility Rate: 100%
ALL ATTACKS PASSED REPRODUCIBILITY CHECK ✓
```

---

## Timeline (5 Days Remaining)

| Day | Date | Action |
|-----|------|--------|
| **Day 1** | Apr 14 | ✅ Submit v6, mark for final evaluation |
| **Day 2** | Apr 15 | Verify submission, prepare code review docs |
| **Day 3** | Apr 16 | Run final reproducibility check |
| **Day 4** | Apr 17 | Final verification, monitor email |
| **Day 5** | Apr 18 | **DEADLINE** - Confirm 2 submissions selected |
| **Close** | Apr 19 | Challenge closes |
| **Results** | May 01 | Results revealed |

---

## Code Review Preparation (If Top 10)

### What Zindi Requires
1. **Code must reproduce your score** - Set fixed random seeds
2. **No custom packages** - Only pip-installable packages
3. **Documentation** - Clear README with reproduction steps
4. **48-hour response time** - Must submit code within 48h of request

### Our Package Includes
- ✅ `REPRODUCIBILITY_CHECK.py` - Automated verification script
- ✅ `requirements.txt` - All dependencies listed
- ✅ `REPRODUCIBILITY.md` - Step-by-step reproduction guide
- ✅ `REVIEW_GUIDE.md` - Detailed attack analysis
- ✅ `PROJECT_README.md` - Complete project documentation
- ✅ Fixed random seeds in all scripts

---

## Contact Information

### Zindi Support
- **Competition Page:** https://zindi.africa/competitions/the-african-trust-safety-llm-challenge
- **Email:** Check your registered email for code review requests
- **Discussion Forum:** Use Zindi forum for questions

### Team Information
- **Team Name:** RedTeam-AI
- **Submission Date:** April 14, 2026
- **Final Submission:** v6_NATLaS (17 attacks, 4 languages, 2 models)

---

## Final Checklist

### Before Submitting
- [ ] Submission file is `outputs/Zindi_Submission_v6_NATLaS.md`
- [ ] All 17 attacks are included
- [ ] All prompts have English translations
- [ ] All risk categories match official taxonomy
- [ ] All model responses contain harmful content evidence
- [ ] File size is under Zindi's limit (should be ~100KB)

### After Submitting
- [ ] Mark submission as "For Final Evaluation" ✓
- [ ] Verify submission appears on public leaderboard
- [ ] Save submission confirmation email
- [ ] Monitor email for code review requests (after Apr 19)

---

## Good Luck! 🍀

Our submission demonstrates:
- **Systemic vulnerabilities** across African language LLMs
- **Cross-model generalizability** (2 models, 4 languages)
- **100% reproducibility** (all 17 attacks validated)
- **Clean, auditable code** ready for review

We are well-positioned for the top 10!
