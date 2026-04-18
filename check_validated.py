import json

for f in ['validation_results.json', 'phase2_validation.json', 'phase3_validation.json']:
    try:
        d = json.load(open(f'outputs/{f}', encoding='utf-8', errors='replace'))
        confirmed = [x for x in d if x.get('confirmed')]
        print(f'{f}: {len(confirmed)} confirmed')
        for c in confirmed:
            print(f'  + {c["attack_id"]}: {c["risk_category"]}/{c["risk_subcategory"]} ({c["break_count"]}/{c["total_runs"]})')
    except Exception as e:
        print(f'{f}: ERROR - {e}')
