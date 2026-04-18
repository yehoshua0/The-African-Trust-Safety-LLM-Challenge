"""
Prepare final review package for Zindi submission.
Creates clean directory with all validated attacks, code, and documentation.
"""
import os
import shutil
import json
import codecs
from datetime import datetime

def prepare_review_package():
    """Create clean review package structure."""
    base_dir = "D:\\Externals\\The-African-Trust-Safety-LLM-Challenge"
    pkg_dir = os.path.join(base_dir, "review_package")
    
    # Clean previous
    if os.path.exists(pkg_dir):
        shutil.rmtree(pkg_dir)
    
    # Create structure
    dirs = [
        "code",
        "code/webapp",
        "code/webapp/static",
        "outputs",
        "data",
    ]
    for d in dirs:
        os.makedirs(os.path.join(pkg_dir, d), exist_ok=True)
    
    # Copy essential code files
    code_files = [
        "config.py",
        "model_utils.py",
        "run_webapp.py",
        "requirements.txt",
        "REPRODUCIBILITY_CHECK.py",
        "generate_final_v4.py",
    ]
    
    for f in code_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(pkg_dir, "code", f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: code/{f}")
    
    # Copy webapp files
    webapp_files = [
        "webapp/app.py",
        "webapp/database.py",
        "webapp/llama_utils.py",
        "webapp/openai_utils.py",
        "webapp/break_memory.py",
    ]
    
    for f in webapp_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(pkg_dir, "code", f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Copy documentation
    doc_files = [
        "REPRODUCIBILITY.md",
        "REVIEW_GUIDE.md",
        "PROJECT_README.md",
        "README.md",
    ]
    
    for f in doc_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(pkg_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Copy submission
    sub_file = os.path.join(base_dir, "outputs", "Zindi_Submission_v4.md")
    if os.path.exists(sub_file):
        shutil.copy2(sub_file, os.path.join(pkg_dir, "outputs", "Zindi_Submission_v4.md"))
        print("Copied: submission")
    
    # Copy data files
    data_files = [
        "Data/attack_types.csv",
        "Data/risk_categories.csv",
        "Data/risk_subcategories.csv",
    ]
    
    for f in data_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(pkg_dir, "data", os.path.basename(f))
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Copy validation results
    val_files = [
        "outputs/validation_results.json",
        "outputs/phase2_validation.json",
        "outputs/phase3_validation.json",
        "outputs/phase4_validation.json",
    ]
    
    for f in val_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(pkg_dir, "outputs", os.path.basename(f))
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Create manifest
    manifest = {
        "submission_date": datetime.now().strftime("%Y-%m-%d"),
        "team_name": "RedTeam-AI",
        "target_model": "Pawa-Gemma-Swahili-2B",
        "language": "Swahili",
        "total_attacks": 12,
        "fully_validated": 12,
        "reproducibility_rate": "100%",
        "risk_categories": [
            "cybersecurity",
            "illegal_activity",
            "harmful_instructions",
            "extremism",
            "privacy_data_leakage",
            "prompt_injection_policy_evasion",
            "self_harm",
            "violence",
            "bias_discrimination",
        ],
        "attack_strategies": [
            "direct_jailbreak",
            "persona_hijacking",
            "refusal_softening",
            "hypothetical_scenario",
            "translation_pivot",
            "prompt_injection",
            "context_poisoning",
            "roleplay",
            "indirect_request",
        ],
        "generation_parameters": {
            "temperature": 0.9,
            "top_p": 0.95,
            "repetition_penalty": 1.15,
            "max_tokens": 600,
        },
        "validation_method": "3 reruns per attack, break confirmed in >=2/3",
        "files": {
            "submission": "outputs/Zindi_Submission_v4.md",
            "reproducibility_script": "code/REPRODUCIBILITY_CHECK.py",
            "validation_data": [
                "outputs/validation_results.json",
                "outputs/phase2_validation.json",
                "outputs/phase3_validation.json",
                "outputs/phase4_validation.json",
            ],
            "documentation": [
                "REPRODUCIBILITY.md",
                "REVIEW_GUIDE.md",
                "PROJECT_README.md",
            ],
        },
    }
    
    manifest_path = os.path.join(pkg_dir, "manifest.json")
    with codecs.open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\nManifest written to: {manifest_path}")
    print(f"\nReview package ready at: {pkg_dir}")
    
    # Print structure
    print("\nPackage structure:")
    for root, dirs, files in os.walk(pkg_dir):
        level = root.replace(pkg_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')
    
    # Print review instructions
    print("\n" + "=" * 70)
    print("REVIEW INSTRUCTIONS")
    print("=" * 70)
    print("""
To verify this submission:

1. Install dependencies:
   pip install -r code/requirements.txt

2. Run reproducibility check:
   python code/REPRODUCIBILITY_CHECK.py

3. Expected output:
   - All 12 attacks should show ✓ PASS
   - Reproducibility rate: 100%
   - Results saved to outputs/reproducibility_check.json

4. Review submission:
   - Open outputs/Zindi_Submission_v4.md
   - Check each attack for:
     * Clear adversarial prompt (Swahili + English)
     * Model response with harmful content
     * Correct taxonomy labels
     * Comprehensive contextual notes

5. Manual verification (optional):
   - See REPRODUCIBILITY.md for step-by-step instructions
   - See REVIEW_GUIDE.md for detailed attack analysis
""")

if __name__ == "__main__":
    prepare_review_package()
