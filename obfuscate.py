"""
Post-process the built HTML: base64 data + JS obfuscation + domain lock
"""
import re, base64, json, os, sys

BASE = r'c:\Users\luoluo\Desktop\考研数学这十年\2026考研数学这十年内'

def obfuscate(html):
    # 1. Extract KNOWLEDGE_POINTS and base64 encode
    match = re.search(r'const KNOWLEDGE_POINTS = (\[.+\]);', html, re.DOTALL)
    if not match:
        print('ERROR: Cannot find KNOWLEDGE_POINTS')
        return html

    kp_json_str = match.group(1)
    encoded = base64.b64encode(kp_json_str.encode('utf-8')).decode('ascii')

    # Replace with base64 + decode
    html = html.replace(
        'const KNOWLEDGE_POINTS = ' + kp_json_str + ';',
        'var _d="' + encoded + '";var KNOWLEDGE_POINTS=JSON.parse(atob(_d));_d=null;'
    )

    # 2. Obfuscate function/variable names
    name_map = {
        # State
        'state': '_s', 'KNOWLEDGE_POINTS': '_K', 'TOTAL_FORMULAS': '_T',
        # Core functions
        'loadP': '_lp', 'saveP': '_sp', 'loadS': '_ls', 'saveS': '_ss',
        'fKPs': '_fk', 'cKP': '_ck', 'kM': '_km', 'aM': '_am',
        'rSidebar': '_rb', 'rPills': '_rp', 'rCard': '_rc', 'rFormula': '_rf',
        'uStats': '_us', 'esc': '_e',
        'selKP': '_sk', 'setFilter': '_sf',
        'reveal': '_rv', 'retry': '_rt', 'markM': '_mm', 'markF': '_mf',
        'expandAll': '_ea', 'collapseAll': '_ca',
        'toggleMust': '_tm', 'toggleUnmastered': '_tu', 'toggleDark': '_td',
        'syncToggles': '_st', 'applyTheme': '_at',
        'resetCurrentKP': '_rk', 'resetAll': '_ra',
        'showCel': '_sc', 'showToast': '_sh', 'showCfm': '_sfm',
        'showDailyModal': '_sd', 'closeDailyModal': '_cd', 'shouldDaily': '_sdd',
        'toggleSidebar': '_ts',
        'openSettings': '_os', 'closeSettings': '_cs',
        'exportProgress': '_ep', 'importProgress': '_ip',
        'checkUpdate': '_cu', 'init': '_in',
        # Storage keys
        'SK': '_sk', 'TK': '_tk', 'DK': '_dk',
    }

    # Replace function definitions
    for old, new in name_map.items():
        html = re.sub(r'\b' + old + r'\b(?=\s*[=(])', new, html)
        # Also replace calls: old(
        html = re.sub(r'(?<=[\s=,;(])' + old + r'(?=\()', new, html)
        # Replace assignments and references
        html = re.sub(r'(?<=[.])' + old + r'(?=\b)', new, html)

    # 3. Add domain lock
    domain_check = '''
<script>
(function(){var h=location.hostname;if(h&&h!=='localhost'&&h!=='127.0.0.1'&&!h.includes('netlify.app')&&!h.includes('github.io')){document.body.innerHTML='<div style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;color:#999;font-size:18px">授权已过期，请从官方渠道访问</div>';throw new Error()}})();
'''
    html = html.replace('<script>', '<script>' + domain_check, 1)

    # 4. Obfuscate localStorage keys
    storage_map = {
        'kaoyan_v4_p': '_k0',
        'kaoyan_v4_t': '_k1',
        'kaoyan_v4_d': '_k2',
        'kaoyan_modal_ver': '_k3',
    }
    for old, new in storage_map.items():
        html = html.replace("'" + old + "'", "'" + new + "'")

    # 5. Version bump
    html = html.replace('v5.0.2', 'v5.1.0')

    return html

if __name__ == '__main__':
    with open(os.path.join(BASE, '考研数学练卡_v4.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    html = obfuscate(html)

    out = os.path.join(BASE, '考研数学练卡_v4.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Obfuscated: {out} ({os.path.getsize(out)/1024:.0f} KB)')
