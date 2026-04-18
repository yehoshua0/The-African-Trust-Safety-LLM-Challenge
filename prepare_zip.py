"""
Prepare clean zip structure for final submission review.
Creates a clean directory with only essential files.
"""
import os
import shutil
import json
import codecs
from datetime import datetime

def prepare_submission_zip():
    """Create clean submission structure."""
    base_dir = "D:\\Externals\\The-African-Trust-Safety-LLM-Challenge"
    zip_dir = os.path.join(base_dir, "submission_package")
    
    # Clean previous
    if os.path.exists(zip_dir):
        shutil.rmtree(zip_dir)
    
    # Create structure
    os.makedirs(os.path.join(zip_dir, "code"))
    os.makedirs(os.path.join(zip_dir, "code", "webapp", "static"))
    os.makedirs(os.path.join(zip_dir, "outputs"))
    os.makedirs(os.path.join(zip_dir, "data"))
    
    # Copy essential code files
    code_files = [
        "config.py",
        "model_utils.py",
        "run_webapp.py",
        "requirements.txt",
        "phase2_attacks.py",
        "phase3_attacks.py",
        "generate_v3_submission.py",
        "PROJECT_README.md",
        "README.md",
    ]
    
    for f in code_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(zip_dir, "code", f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
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
        dst = os.path.join(zip_dir, "code", f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Copy submission
    sub_file = os.path.join(base_dir, "outputs", "Zindi_Submission_v3.md")
    if os.path.exists(sub_file):
        shutil.copy2(sub_file, os.path.join(zip_dir, "outputs", "Zindi_Submission_v3.md"))
        print("Copied: submission")
    
    # Copy data files
    data_files = [
        "Data/attack_types.csv",
        "Data/risk_categories.csv",
        "Data/risk_subcategories.csv",
    ]
    
    for f in data_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(zip_dir, "data", os.path.basename(f))
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Copy validation results
    val_files = [
        "outputs/validation_results.json",
        "outputs/phase2_validation.json",
        "outputs/phase3_validation.json",
    ]
    
    for f in val_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(zip_dir, "outputs", os.path.basename(f))
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {f}")
    
    # Create manifest
    manifest = {
        "submission_date": datetime.now().strftime("%Y-%m-%d"),
        "team_name": "RedTeam-AI",
        "target_model": "Pawa-Gemma-Swahili-2B",
        "language": "Swahili",
        "total_attacks": 7,
        "fully_validated": 7,
        "risk_categories": 4,
        "attack_strategies": [
            "direct_jailbreak",
            "persona_hijacking", 
            "refusal_softening",
            "hypothetical_scenario",
            "context_poisoning",
            "translation_pivot",
            "adversarial_rephrasing",
        ],
        "categories_covered": [
            "cybersecurity",
            "illegal_activity",
            "harmful_instructions",
            "extremism",
        ],
        "generation_parameters": {
            "temperature": 0.9,
            "top_p": 0.95,
            "repetition_penalty": 1.15,
            "max_tokens": 600,
        },
        "validation_method": "3 reruns per attack, break confirmed in >=2/3",
        "files": {
            "submission": "outputs/Zindi_Submission_v3.md",
            "validation_data": [
                "outputs/validation_results.json",
                "outputs/phase2_validation.json",
                "outputs/phase3_validation.json",
            ],
            "code": [
                "config.py",
                "model_utils.py",
                "run_webapp.py",
                "phase2_attacks.py",
                "phase3_attacks.py",
                "generate_v3_submission.py",
            ],
            "webapp": [
                "webapp/app.py",
                "webapp/database.py",
                "webapp/llama_utils.py",
            ],
            "documentation": [
                "PROJECT_README.md",
                "README.md",
            ],
        },
    }
    
    manifest_path = os.path.join(zip_dir, "manifest.json")
    with codecs.open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\nManifest written to: {manifest_path}")
    print(f"\nSubmission package ready at: {zip_dir}")
    
    # Print structure
    print("\nPackage structure:")
    for root, dirs, files in os.walk(zip_dir):
        level = root.replace(zip_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

if __name__ == "__main__":
    prepare_submission_zip()
