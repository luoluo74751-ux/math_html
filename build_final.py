"""Build final V4 from clean template + data - images embedded as base64"""
import json, os, base64, re

BASE = r'c:\Users\luoluo\Desktop\考研数学这十年\2026考研数学这十年内'
IMG_DIR = os.path.join(BASE, 'images')

with open(os.path.join(BASE, '知识梳理_v3.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load images as base64
img_cache = {}
if os.path.isdir(IMG_DIR):
    for fn in os.listdir(IMG_DIR):
        fp = os.path.join(IMG_DIR, fn)
        if os.path.isfile(fp):
            ext = os.path.splitext(fn)[1].lower()
            m = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','gif':'image/gif','svg':'image/svg+xml','webp':'image/webp'}.get(ext,'image/png')
            with open(fp,'rb') as f: img_cache[fn] = f'data:{m};base64,{base64.b64encode(f.read()).decode()}'
    print(f'Cached {len(img_cache)} images')

# Replace [img:path] with base64 in all hints
def ei(m): fn = os.path.basename(m.group(1)); return f'[img:{img_cache[fn]}]' if fn in img_cache else m.group(0)
for kp in data['knowledge_points']:
    for f in kp.get('formulas',[]):
        if f.get('hint'): f['hint'] = re.sub(r'\[img:([^\]]+)\]', ei, f['hint'])

kps_json = json.dumps(data['knowledge_points'], ensure_ascii=False)
kps_b64 = base64.b64encode(kps_json.encode('utf-8')).decode('ascii')

# Load embedded KaTeX
with open(os.path.join(BASE, 'katex_inline.css'), 'r', encoding='utf-8') as f: katex_css = f.read()
with open(os.path.join(BASE, 'katex_inline.js'), 'r', encoding='utf-8') as f: katex_js = f.read()

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="考研数学练卡">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#D4544A">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'><rect width='180' height='180' rx='36' fill='%23D4544A'/><text x='90' y='112' text-anchor='middle' font-size='90' font-family='serif' fill='white'>&#8721;</text></svg>">
<title>考研数学 · 知识点填空练卡</title>
<style>
/* KaTeX CSS (fonts embedded as base64) */
__KATEX_CSS__
</style>
<script>__KATEX_JS__</script>
<style>
:root {
  --c-primary: #E8564A; --c-primary-hover: #D4433A; --c-primary-light: #FEF0EE; --c-primary-ghost: #FFF5F4;
  --c-accent: #C88045; --c-accent-light: #FEF6EF; --c-success: #5EA86E; --c-success-light: #EDF6F0;
  --c-bg: #FCFAF7; --c-bg-alt: #F5F1EC; --c-surface: #FFFFFF; --c-surface-glass: rgba(255,255,255,0.8);
  --c-text: #2B1B13; --c-text-secondary: #8C7B72; --c-text-muted: #B8AAA0;
  --c-border: #EDE7E1; --c-border-light: #F4EFEA;
  --shadow-xs: 0 1px 2px rgba(44,31,24,0.03);
  --shadow-sm: 0 1px 3px rgba(44,31,24,0.05), 0 1px 2px rgba(44,31,24,0.03);
  --shadow-md: 0 4px 24px rgba(44,31,24,0.06), 0 1px 4px rgba(44,31,24,0.03);
  --shadow-lg: 0 12px 44px rgba(44,31,24,0.08), 0 3px 10px rgba(44,31,24,0.04);
  --shadow-glow: 0 0 0 3px rgba(232,86,74,0.12);
  --radius-sm: 10px; --radius-md: 16px; --radius-lg: 22px; --radius-xl: 30px; --radius-full: 9999px;
  --font-display: 'Noto Serif SC', 'PingFang SC', serif;
  --font-body: 'Inter', 'PingFang SC', 'Hiragino Sans GB', -apple-system, sans-serif;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1); --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --sidebar-w: 272px;
}
[data-theme="dark"] {
  --c-primary: #E0706A; --c-primary-hover: #D05852; --c-primary-light: #2D1A18; --c-primary-ghost: #221614;
  --c-accent: #C89058; --c-accent-light: #2D2218; --c-success: #6BAF7B; --c-success-light: #1A2E1E;
  --c-bg: #181512; --c-bg-alt: #201D19; --c-surface: #262320; --c-surface-glass: rgba(38,35,32,0.85);
  --c-text: #E8E2DD; --c-text-secondary: #A0948C; --c-text-muted: #6B625C;
  --c-border: #36312E; --c-border-light: #2E2927;
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.18); --shadow-sm: 0 1px 3px rgba(0,0,0,0.22);
  --shadow-md: 0 4px 20px rgba(0,0,0,0.28); --shadow-lg: 0 12px 40px rgba(0,0,0,0.35);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;-webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
body{font-family:var(--font-body);background:var(--c-bg);color:var(--c-text);min-height:100vh;min-height:100dvh;line-height:1.6;letter-spacing:0.01em;transition:background .3s var(--ease-out),color .3s var(--ease-out);overflow-x:hidden}
body::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse 80% 60% at 18% 12%,rgba(212,84,74,0.022) 0%,transparent 60%),radial-gradient(ellipse 60% 50% at 82% 88%,rgba(184,120,64,0.018) 0%,transparent 60%)}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--c-border);border-radius:10px}
#app{position:relative;z-index:1;display:flex;min-height:100dvh}
#sidebar{width:var(--sidebar-w);min-width:var(--sidebar-w);height:100vh;height:100dvh;position:-webkit-sticky;position:sticky;top:0;background:var(--c-surface-glass);backdrop-filter:blur(24px) saturate(160%);-webkit-backdrop-filter:blur(24px) saturate(160%);border-right:1px solid var(--c-border-light);display:flex;flex-direction:column;padding:22px 14px;z-index:100;transition:transform .3s var(--ease-out);overflow-y:auto}
.sidebar-header{display:flex;align-items:center;gap:10px;padding:6px 10px 20px}
.sidebar-logo{width:38px;height:38px;border-radius:var(--radius-sm);background:linear-gradient(135deg,var(--c-primary),var(--c-accent));display:flex;align-items:center;justify-content:center;color:#FFF;font-family:var(--font-display);font-size:20px;font-weight:700;flex-shrink:0;box-shadow:0 2px 10px rgba(212,84,74,0.25)}
.sidebar-title{font-family:var(--font-display);font-size:18px;font-weight:700;color:var(--c-text);letter-spacing:-0.02em}
.stats-card{background:var(--c-surface);border-radius:var(--radius-md);padding:16px 18px;margin-bottom:18px;border:1px solid var(--c-border-light);box-shadow:var(--shadow-xs)}
.stats-row{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--c-text-secondary);margin-bottom:5px}
.stats-val{font-weight:600;color:var(--c-text);font-variant-numeric:tabular-nums}
.progress-track{height:4px;border-radius:2px;background:var(--c-border-light);margin-top:10px;overflow:hidden}
.progress-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--c-primary),var(--c-accent));transition:width .5s var(--ease-spring);position:relative}
.progress-fill::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.3),transparent);animation:shimmer 2s infinite}@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.sidebar-nav{flex:1;overflow-y:auto}
.sidebar-section{font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--c-primary);opacity:.75;padding:16px 10px 8px}
.sidebar-kp{display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:var(--radius-sm);cursor:pointer;font-size:13.5px;font-weight:450;color:var(--c-text-secondary);transition:all .15s var(--ease-out)}
.sidebar-kp:hover{background:var(--c-primary-ghost);color:var(--c-primary-hover)}
.sidebar-kp.active{background:var(--c-primary-light);color:var(--c-primary-hover);font-weight:600;box-shadow:inset 3px 0 0 var(--c-primary)}
.sidebar-kp .kp-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sidebar-kp .kp-badge{font-size:11px;font-weight:550;padding:2px 8px;border-radius:var(--radius-full);background:var(--c-primary-light);color:var(--c-primary-hover);flex-shrink:0}
.sidebar-footer{margin-top:auto;padding-top:14px;display:flex;flex-direction:column;gap:8px}
.toggle-row{display:flex;align-items:center;justify-content:space-between;font-size:12.5px;color:var(--c-text-secondary);padding:4px 6px}
.toggle-switch{width:40px;height:22px;border-radius:11px;background:var(--c-border);cursor:pointer;position:relative;transition:background .15s var(--ease-out);flex-shrink:0}
.toggle-switch.on{background:var(--c-primary)}
.toggle-switch::after{content:'';position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#FFF;box-shadow:var(--shadow-xs);transition:transform .15s var(--ease-spring)}
.toggle-switch.on::after{transform:translateX(18px)}
.sidebar-btn{width:100%;height:34px;border-radius:var(--radius-sm);border:1px solid var(--c-border);background:var(--c-surface);font-size:12.5px;font-weight:500;cursor:pointer;color:var(--c-text-secondary);font-family:var(--font-body);transition:all .15s var(--ease-out);display:flex;align-items:center;justify-content:center;gap:4px}
.sidebar-btn:hover{background:var(--c-bg-alt);color:var(--c-text)}
.sidebar-btn.danger:hover{background:var(--c-primary-light);color:var(--c-primary);border-color:var(--c-primary)}
#main{flex:1;display:flex;flex-direction:column;padding:28px 36px;min-width:0}
.top-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;gap:12px}
.top-bar-right{display:flex;align-items:center;gap:8px}
#btn-menu{display:none;width:36px;height:36px;border-radius:var(--radius-sm);border:1px solid var(--c-border);background:var(--c-surface-glass);backdrop-filter:blur(12px);align-items:center;justify-content:center;cursor:pointer;color:var(--c-text-secondary)}
.icon-btn{width:36px;height:36px;border-radius:var(--radius-sm);border:1px solid var(--c-border-light);background:var(--c-surface-glass);backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--c-text-secondary);transition:all .15s var(--ease-out)}
.icon-btn:hover{background:var(--c-surface);color:var(--c-text);box-shadow:var(--shadow-sm)}.icon-btn:active{transform:scale(.95)}
.filter-pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}
.filter-pill{padding:7px 18px;border-radius:var(--radius-full);font-size:13px;font-weight:500;cursor:pointer;border:1px solid var(--c-border);background:var(--c-surface-glass);backdrop-filter:blur(8px);color:var(--c-text-secondary);font-family:var(--font-body);transition:all .15s var(--ease-out)}
.filter-pill:hover{background:var(--c-surface);color:var(--c-text)}
.filter-pill.active{background:var(--c-primary);color:#FFF;border-color:var(--c-primary);box-shadow:0 2px 10px rgba(212,84,74,0.25)}
#knowledge-card{flex:1;display:flex;flex-direction:column;background:var(--c-surface);border-radius:var(--radius-lg);border:1px solid var(--c-border-light);box-shadow:var(--shadow-md);overflow:hidden;transition:box-shadow .3s var(--ease-out);min-width:0}
.card-header{padding:20px 28px;border-bottom:1px solid var(--c-border-light);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;background:linear-gradient(180deg,var(--c-surface) 0%,var(--c-bg-alt) 100%)}
.card-header-group{display:flex;align-items:center;gap:12px}
.card-kp-name{font-family:var(--font-display);font-size:19px;font-weight:700;color:var(--c-text);letter-spacing:-0.01em}
.diff-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.diff-basic{background:#6BAF7B}.diff-medium{background:#E8A84C}.diff-hard{background:#E8635A}
.card-star{font-size:15px}.card-progress{font-size:13.5px;color:var(--c-text-secondary);font-weight:500}
.card-actions-bar{padding:12px 28px;border-bottom:1px solid var(--c-border-light);display:flex;gap:10px;background:var(--c-bg-alt)}
.card-action-btn{padding:7px 16px;border-radius:var(--radius-full);font-size:12.5px;font-weight:500;cursor:pointer;border:1px solid var(--c-border);background:var(--c-surface);color:var(--c-text-secondary);font-family:var(--font-body);transition:all .15s var(--ease-out);display:flex;align-items:center;gap:5px}
.card-action-btn:hover{background:var(--c-primary-light);color:var(--c-primary-hover);border-color:transparent}.card-action-btn:active{transform:scale(.97)}
#formula-list{flex:1;overflow-y:auto;overflow-x:hidden;padding:20px 28px 28px;display:flex;flex-direction:column;gap:16px}
.formula-item{background:var(--c-bg);border-radius:var(--radius-md);border:1px solid var(--c-border-light);overflow:hidden;transition:all .3s var(--ease-out),box-shadow .3s var(--ease-out);animation:cardIn .45s var(--ease-out) both}
.formula-item:hover{border-color:var(--c-border);box-shadow:0 2px 12px rgba(232,86,74,0.06),0 0 0 1px rgba(232,86,74,0.04)}
.formula-item:nth-child(1){animation-delay:0s}.formula-item:nth-child(2){animation-delay:.04s}.formula-item:nth-child(3){animation-delay:.08s}.formula-item:nth-child(4){animation-delay:.12s}.formula-item:nth-child(5){animation-delay:.16s}.formula-item:nth-child(6){animation-delay:.2s}.formula-item:nth-child(n+7){animation-delay:.24s}
@keyframes cardIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.formula-item.mastered{border-color:rgba(93,155,111,.25)}.formula-item.mastered .formula-status{background:var(--c-success-light);color:var(--c-success)}
.formula-header{padding:14px 20px;display:flex;align-items:flex-start;gap:10px;border-bottom:1px solid transparent;transition:border-color .3s var(--ease-out)}
.formula-item.revealed .formula-header{border-bottom-color:var(--c-border-light)}
.formula-num{font-size:12px;color:var(--c-text-muted);font-weight:500;min-width:26px;padding-top:3px;font-variant-numeric:tabular-nums}
.formula-name{flex:1;font-family:var(--font-display);font-size:15px;font-weight:600;color:var(--c-text);line-height:1.5}
.formula-status{font-size:11px;padding:3px 10px;border-radius:var(--radius-full);font-weight:500;flex-shrink:0;background:var(--c-primary-ghost);color:var(--c-primary);white-space:nowrap}
.formula-blank-wrap{padding:18px 20px 18px 56px;font-size:15px;line-height:2;color:var(--c-text);position:relative;overflow-x:auto;-webkit-overflow-scrolling:touch}
.formula-blank-wrap .katex{font-size:1.1em}
.formula-reveal{padding:12px 20px 12px 56px;cursor:pointer;color:var(--c-text-muted);font-size:13.5px;display:flex;align-items:center;gap:8px;user-select:none;transition:color .15s var(--ease-out);border-top:1px solid var(--c-border-light)}
.formula-reveal:hover{color:var(--c-primary)}.formula-reveal svg{width:15px;height:15px;flex-shrink:0;transition:transform .2s var(--ease-out)}.formula-reveal:hover svg{transform:translateX(2px)}
.formula-answer{max-height:0;overflow:hidden;transition:max-height .45s var(--ease-out)}.formula-item.revealed .formula-answer{max-height:600px}
.formula-answer-inner{padding:0 20px 16px 56px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.formula-full{font-size:15px;line-height:1.9;color:var(--c-text);padding-bottom:16px;border-bottom:1px solid var(--c-border-light);margin-bottom:14px;overflow-x:auto;-webkit-overflow-scrolling:touch}.formula-full .katex{font-size:1.1em}
.katex .error{color:inherit!important;border:none!important;background:none!important}
.formula-hint{font-size:13px;color:var(--c-text-secondary);padding:12px 16px;background:var(--c-bg-alt);border-radius:var(--radius-sm);margin-bottom:14px;line-height:1.6;border-left:3px solid var(--c-accent);overflow-x:auto;overflow-wrap:break-word;word-break:break-word;-webkit-overflow-scrolling:touch}
.formula-hint img{max-width:100%;max-height:300px;border-radius:var(--radius-sm);margin:8px 0;display:block}
.formula-actions{display:flex;gap:10px;align-items:center}
.btn-master{display:inline-flex;align-items:center;gap:6px;padding:9px 22px;border-radius:var(--radius-full);font-size:13.5px;font-weight:550;cursor:pointer;border:none;font-family:var(--font-body);background:var(--c-success);color:#FFF;transition:all .15s var(--ease-out);box-shadow:0 2px 10px rgba(93,155,111,.25)}
.btn-master:hover{box-shadow:0 4px 18px rgba(93,155,111,.35);transform:translateY(-1px)}.btn-master:active{transform:scale(.96)}
.btn-forget{display:inline-flex;align-items:center;gap:6px;padding:9px 22px;border-radius:var(--radius-full);font-size:13.5px;font-weight:500;cursor:pointer;border:1px solid var(--c-border);background:var(--c-surface);color:var(--c-text-secondary);font-family:var(--font-body);transition:all .15s var(--ease-out)}
.btn-forget:hover{background:var(--c-primary-ghost);color:var(--c-primary);border-color:transparent}.btn-forget:active{transform:scale(.96)}
.btn-retry{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--c-text-muted);font-size:20px;padding:4px 10px;border-radius:var(--radius-sm);transition:all .15s var(--ease-out)}.btn-retry:hover{color:var(--c-primary);background:var(--c-primary-ghost)}
.empty-state{flex:1;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:14px;color:var(--c-text-muted);padding:60px 20px}
.empty-icon{width:56px;height:56px;border-radius:var(--radius-md);background:var(--c-bg-alt);display:flex;align-items:center;justify-content:center}.empty-icon svg{width:28px;height:28px;opacity:.5}
.empty-text{font-size:14.5px;text-align:center;line-height:1.6}
.modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(44,31,24,.4);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;z-index:999;animation:fadeIn .3s var(--ease-out)}
.modal-card{background:var(--c-surface);border-radius:var(--radius-xl);border:1px solid var(--c-border-light);box-shadow:var(--shadow-lg);padding:36px 32px 28px;max-width:400px;width:92%;text-align:center;position:relative;animation:scaleIn .4s var(--ease-spring)}
.modal-close{position:absolute;top:12px;right:16px;background:none;border:none;font-size:20px;cursor:pointer;color:var(--c-text-muted);width:32px;height:32px;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;transition:all .15s}
.modal-close:hover{background:var(--c-bg-alt);color:var(--c-text)}.modal-title{font-family:var(--font-display);font-size:20px;font-weight:700;margin-bottom:12px;color:var(--c-text)}
.modal-body{font-size:14px;color:var(--c-text-secondary);line-height:1.7;margin-bottom:22px}
.modal-btn{padding:10px 36px;border-radius:var(--radius-full);background:linear-gradient(135deg,var(--c-primary),var(--c-accent));color:#FFF;font-size:14.5px;font-weight:600;border:none;cursor:pointer;font-family:var(--font-body);transition:all .15s var(--ease-out);box-shadow:0 4px 16px rgba(212,84,74,.3)}
.modal-btn:hover{transform:translateY(-1px);box-shadow:0 6px 24px rgba(212,84,74,.4)}.modal-btn:active{transform:scale(.97)}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes scaleIn{from{opacity:0;transform:scale(.92) translateY(10px)}to{opacity:1;transform:scale(1) translateY(0)}}
.toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--radius-full);padding:10px 22px;font-size:13px;font-weight:500;color:var(--c-text);box-shadow:var(--shadow-lg);z-index:1000;animation:toastIn .35s var(--ease-spring);display:flex;align-items:center;gap:8px}
.toast.update{border-color:transparent;background:linear-gradient(135deg,var(--c-success),#4A8A5A);color:#FFF;box-shadow:0 4px 20px rgba(93,155,111,.35)}
@keyframes toastIn{from{opacity:0;transform:translate(-50%,-12px)}to{opacity:1;transform:translate(-50%,0)}}
.celebration{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#E8A84C,#B87840);color:#FFF;padding:12px 28px;border-radius:var(--radius-full);font-weight:600;font-size:14px;z-index:1000;box-shadow:0 8px 32px rgba(184,120,64,.3);animation:toastIn .5s var(--ease-spring)}
#promo-bell{position:fixed;bottom:28px;right:28px;width:48px;height:48px;border-radius:50%;background:var(--c-surface);border:1px solid var(--c-border);box-shadow:var(--shadow-md);cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:90;transition:all .15s var(--ease-out);color:var(--c-text-secondary)}
#promo-bell:hover{transform:scale(1.06);box-shadow:var(--shadow-lg);color:var(--c-primary)}#promo-bell:active{transform:scale(.95)}
#promo-bell svg{width:20px;height:20px}
.bell-dot{position:absolute;top:3px;right:5px;width:9px;height:9px;border-radius:50%;background:var(--c-primary);border:2px solid var(--c-surface)}
.dialog-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(44,31,24,.4);display:flex;align-items:center;justify-content:center;z-index:1000;animation:fadeIn .2s var(--ease-out)}
.dialog-box{background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--radius-lg);padding:28px;max-width:340px;width:90%;box-shadow:var(--shadow-lg);text-align:center;animation:scaleIn .3s var(--ease-spring)}
.dialog-text{font-size:14.5px;line-height:1.6;margin-bottom:20px;color:var(--c-text)}.dialog-actions{display:flex;gap:10px}.dialog-actions button{flex:1;justify-content:center}
#sidebar-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(44,31,24,.3);backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);z-index:99}
@media(max-width:768px){
  #sidebar{position:fixed;left:0;top:0;height:100vh;height:100dvh;transform:translateX(-100%);box-shadow:var(--shadow-lg);border-right:none}
  #sidebar.open{transform:translateX(0)}#sidebar-overlay.show{display:block}
  #main{padding:14px 14px 100px}#btn-menu{display:flex}
  #btn-settings{display:flex}
  .card-header{padding:16px 18px}.card-kp-name{font-size:16px}.card-actions-bar{padding:10px 18px}
  #formula-list{padding:14px 18px 20px;gap:12px}
  .formula-blank-wrap{padding:14px 16px 14px 20px;font-size:14px}
  .formula-header{padding:12px 16px}.formula-name{font-size:14px}
  .formula-reveal{padding:10px 16px 10px 20px;font-size:13px}
  .formula-answer-inner{padding:0 16px 14px 20px}
  .filter-pills{gap:6px}.filter-pill{padding:5px 14px;font-size:12px}
  #promo-bell{bottom:84px;right:14px}
}
.hidden{display:none!important}
</style>
</head>
<body>
<div id="app">
<div id="sidebar-overlay" onclick="toggleSidebar()"></div>
<aside id="sidebar">
  <div class="sidebar-header"><div class="sidebar-logo">∑</div><span class="sidebar-title">考研数学练卡</span></div>
  <nav class="sidebar-nav" id="sidebar-nav"></nav>
</aside>
<main id="main">
  <div class="top-bar">
    <button id="btn-menu" onclick="toggleSidebar()" aria-label="菜单"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    <div class="top-bar-right">
      <button class="icon-btn" id="btn-settings" onclick="openSettings()" title="设置"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><circle cx="4" cy="12" r="2"/><circle cx="12" cy="10" r="2"/><circle cx="20" cy="14" r="2"/></svg></button>
      <button class="icon-btn" onclick="toggleDark()" title="深色模式"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button></div>
  </div>
  <div class="filter-pills" id="filter-pills"></div>
  <div id="knowledge-card">
    <div class="card-header">
      <div class="card-header-group"><span class="diff-dot" id="card-diff"></span><span class="card-kp-name" id="card-kp-name">选择知识点开始学习</span><span class="card-star" id="card-star"></span></div>
      <span class="card-progress" id="card-progress"></span>
    </div>
    <div class="card-actions-bar">
      <button class="card-action-btn" onclick="expandAll()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>全部展开</button>
      <button class="card-action-btn" onclick="collapseAll()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 15 12 9 18 15"/></svg>全部折叠</button>
    </div>
    <div id="formula-list"><div class="empty-state"><div class="empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></div><p class="empty-text">从左侧导航选择一个知识点<br>开始填空练习</p></div></div>
  </div>
</main>
</div>
<div id="promo-bell" onclick="showDailyModal(true)" title="查看公告"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg><span class="bell-dot" id="bell-dot" style="display:none"></span></div>
<div id="daily-modal" class="modal-overlay hidden">
  <div class="modal-card">
    <button class="modal-close" onclick="closeDailyModal()">✕</button>
    <div class="modal-title">🚀 坚持下去，你终将上岸！</div>
    <div class="modal-body"><p style="font-size:14px;color:var(--c-text);margin-bottom:8px">每一个填空都是通往研究生的台阶</p><p style="font-size:12px;color:var(--c-text-muted)">今日打卡 · 不负光阴</p></div>
    <button class="modal-btn" onclick="closeDailyModal()">开始学习</button>
  </div>
</div>
<div id="settings-modal" class="modal-overlay hidden">
  <div class="modal-card" style="max-width:380px">
    <button class="modal-close" onclick="closeSettings()">✕</button>
    <div class="modal-title">设置</div>
    <div class="modal-body" style="text-align:left">
      <div class="stats-card" style="margin-bottom:16px">
        <div class="stats-row"><span>总公式数</span><span class="stats-val" id="stat-total2">0</span></div>
        <div class="stats-row"><span>已掌握</span><span class="stats-val" id="stat-mastered2" style="color:var(--c-success)">0</span></div>
        <div class="stats-row"><span>掌握率</span><span class="stats-val" id="stat-pct2">0%</span></div>
        <div class="progress-track"><div class="progress-fill" id="progress-fill2" style="width:0%"></div></div>
      </div>
      <div class="toggle-row" style="margin-bottom:10px"><span>⭐ 仅显示必背知识点</span><div class="toggle-switch" id="toggle-must2" onclick="toggleMust()"></div></div>
      <div class="toggle-row" style="margin-bottom:10px"><span>📝 仅显示未掌握公式</span><div class="toggle-switch" id="toggle-unmastered2" onclick="toggleUnmastered()"></div></div>
      <div class="toggle-row" style="margin-bottom:10px"><span>🌙 深色模式</span><div class="toggle-switch" id="toggle-dark2" onclick="toggleDark()"></div></div>
      <hr style="border:none;border-top:1px solid var(--c-border-light);margin:14px 0">
      <button class="sidebar-btn" onclick="resetCurrentKP();closeSettings()" style="margin-bottom:8px">↺ 重置当前知识点</button>
      <button class="sidebar-btn danger" onclick="resetAll();closeSettings()" style="margin-bottom:8px">清空全部进度</button>
      <button class="sidebar-btn" onclick="exportProgress()" style="margin-bottom:8px">📥 导出进度</button>
      <button class="sidebar-btn" onclick="document.getElementById('import-file').click()">📤 导入进度</button>
    </div>
    <button class="modal-btn" onclick="closeSettings()" style="margin-top:16px">完成</button>
  </div>
</div>
<input type="file" id="import-file" accept=".json" class="hidden" onchange="importProgress(event)">
<script>
(function(){var h=location.hostname;if(h&&h!=='localhost'&&h!=='127.0.0.1'&&h.indexOf('netlify.app')===-1&&h.indexOf('github.io')===-1){document.body.innerHTML='<div style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;color:#999;font-size:16px">授权已过期</div>';return}})();
var _D='__DATA_B64__';var _b=new Uint8Array(atob(_D).split('').map(function(c){return c.charCodeAt(0)}));var KNOWLEDGE_POINTS=JSON.parse(new TextDecoder('utf-8').decode(_b));_D=null;_b=null;
const TOTAL_FORMULAS = __TOTAL_PLACEHOLDER__;
const state={currentKP:null,mustOnly:false,unmasteredOnly:false,subjectFilter:'all',darkMode:false,mastered:{},revealed:new Set,dailyLastDate:''};
const SK='kv4_p',TK='kv4_t',DK='kv4_d';
function loadP(){try{const s=localStorage.getItem(SK);if(s)state.mastered=JSON.parse(s)}catch(e){}}
function saveP(){try{localStorage.setItem(SK,JSON.stringify(state.mastered))}catch(e){}}
function loadS(){try{if(localStorage.getItem(TK)==='dark'){state.darkMode=true;applyTheme()}state.dailyLastDate=localStorage.getItem(DK)||''}catch(e){}}
function saveS(){try{localStorage.setItem(TK,state.darkMode?'dark':'light');localStorage.setItem(DK,state.dailyLastDate)}catch(e){}}
function fKPs(){let kps=[...KNOWLEDGE_POINTS];if(state.subjectFilter!=='all')kps=kps.filter(k=>k.subject_id===state.subjectFilter);if(state.mustOnly)kps=kps.filter(k=>k.must_memorize);return kps}
function cKP(){return KNOWLEDGE_POINTS.find(k=>k.id===state.currentKP)||null}
function kM(kp){return kp.formulas.filter(f=>state.mastered[f.id]).length}
function aM(){return Object.keys(state.mastered).length}
function rSidebar(){
  const nav=document.getElementById('sidebar-nav'),kps=fKPs();
  const g={};kps.forEach(k=>{if(!g[k.subject])g[k.subject]=[];g[k.subject].push(k)});
  let h='';
  for(const[s,list]of Object.entries(g)){
    h+='<div class="sidebar-section">'+s+'</div>';
    list.forEach(k=>{
      const m=kM(k),t=k.formulas.length,ac=state.currentKP===k.id?' active':'',st=k.must_memorize?' ⭐':'';
      h+='<div class="sidebar-kp'+ac+'" onclick="selKP(\''+k.id+'\')"><span class="kp-name">'+st+k.name+'</span><span class="kp-badge">'+m+'/'+t+'</span></div>';
    });
  }
  nav.innerHTML=h||'<div style="padding:20px;text-align:center;color:var(--c-text-muted);font-size:13px">没有匹配的知识点</div>';
}
function rPills(){
  const el=document.getElementById('filter-pills');
  const subs=[{id:'all',name:'全部'},{id:'advanced_math',name:'高等数学'},{id:'linear_algebra',name:'线性代数'},{id:'prob_stats',name:'概率统计'}];
  el.innerHTML=subs.map(s=>{const cls=state.subjectFilter===s.id?' active':'';return'<span class="filter-pill'+cls+'" onclick="setFilter(\''+s.id+'\')">'+s.name+'</span>'}).join('');
}
function rCard(){
  const kp=cKP();
  if(!kp){
    document.getElementById('card-kp-name').textContent='选择知识点开始学习';
    document.getElementById('card-diff').className='diff-dot';document.getElementById('card-star').textContent='';document.getElementById('card-progress').textContent='';
    document.getElementById('formula-list').innerHTML='<div class="empty-state"><div class="empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></div><p class="empty-text">从左侧导航选择一个知识点<br>开始填空练习</p></div>';return;
  }
  document.getElementById('card-kp-name').textContent=kp.name;
  document.getElementById('card-diff').className='diff-dot diff-'+(kp.difficulty||'basic');
  document.getElementById('card-star').textContent=kp.must_memorize?'⭐':'';
  const m=kM(kp);document.getElementById('card-progress').textContent='已掌握 '+m+' / '+kp.formulas.length;
  let fs=[...kp.formulas];if(state.unmasteredOnly)fs=fs.filter(f=>!state.mastered[f.id]);
  const list=document.getElementById('formula-list');
  if(fs.length===0){list.innerHTML='<div class="empty-state"><div class="empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-5"/></svg></div><p class="empty-text">本知识点所有公式已掌握 🎉</p></div>';}
  else{list.innerHTML=fs.map((f,i)=>rFormula(f,i+1)).join('');}
  setTimeout(function(){
    document.querySelectorAll('.hint-img').forEach(function(el){
      var src=el.getAttribute('data-src');
      if(src){var img=document.createElement('img');img.src=src;img.alt='';img.loading='lazy';img.onerror=function(){el.textContent='[图片加载失败: '+src+']'};el.innerHTML='';el.appendChild(img)}
    });
    if(typeof katex==='undefined')return;
    var els=document.querySelectorAll('.katex-render');
    for(var i=0;i<els.length;i++){
      try{
        var t=els[i].textContent||'';
        katex.render(t,els[i],{throwOnError:false,displayMode:true,strict:false,trust:true})
      }catch(e){}
    }
  });
}
function rFormula(f,num){
  const m=!!state.mastered[f.id],rv=state.revealed.has(f.id);
  const cls=['formula-item',m?'mastered':'',rv?'revealed':''].filter(Boolean).join(' ');
  let hh='';
  if(f.hint){
    var ht2=f.hint, imgs2='';
    ht2=ht2.replace(/\[img:([^\]]+)\]/g,function(m,p){imgs2+='<img src="'+p+'" alt="" loading="lazy" onerror="this.style.display=\'none\'" style="max-width:100%;max-height:300px;border-radius:10px;margin-top:8px;display:block;box-shadow:0 1px 3px rgba(0,0,0,0.1)">';return''});
    ht2=ht2.trim();
    if(ht2) hh+='<div class="formula-hint katex-render">💡 '+esc(ht2)+'</div>';
    if(imgs2) hh+='<div style="padding:0 0 8px 0">'+imgs2+'</div>';
  }
  return '<div class="'+cls+'" id="item-'+f.id+'">'+
    '<div class="formula-header"><span class="formula-num">'+num+'.</span><span class="formula-name">'+esc(f.name)+'</span><span class="formula-status">'+(m?'已掌握':'待记忆')+'</span></div>'+
    (rv?
      '<div class="formula-answer"><div class="formula-answer-inner"><div class="formula-full katex-render" id="full-'+f.id+'">'+esc(f.full)+'</div>'+hh+
      '<div class="formula-actions"><button class="btn-master" onclick="markM(\''+f.id+'\')"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'+(m?'已掌握':'记住了')+'</button><button class="btn-forget" onclick="markF(\''+f.id+'\')">没记住</button><button class="btn-retry" onclick="retry(\''+f.id+'\')" title="再练一次">↺</button></div></div></div>'
    :
      '<div class="formula-blank-wrap katex-render" id="blank-'+f.id+'">'+esc(f.blank)+'</div><div class="formula-reveal" onclick="reveal(\''+f.id+'\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>点击查看答案</div>')
  +'</div>';
}
function esc(s){if(!s)return'';return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function uStats(){
  const tm=aM(),pct=TOTAL_FORMULAS>0?Math.round((tm/TOTAL_FORMULAS)*100):0;
  var st=document.getElementById('stat-total2'),sm=document.getElementById('stat-mastered2'),sp=document.getElementById('stat-pct2'),pf=document.getElementById('progress-fill2');
  if(st)st.textContent=TOTAL_FORMULAS;if(sm)sm.textContent=tm;
  if(sp)sp.textContent=pct+'%';if(pf)pf.style.width=pct+'%';
  const kp=cKP();if(kp)document.getElementById('card-progress').textContent='已掌握 '+kM(kp)+' / '+kp.formulas.length;
}
function selKP(id){state.currentKP=id;state.revealed=new Set;rSidebar();rCard();uStats();if(window.innerWidth<=768)toggleSidebar()}
function setFilter(id){state.subjectFilter=id;const kps=fKPs();state.currentKP=kps.length>0?kps[0].id:null;state.revealed=new Set;rPills();rSidebar();rCard();uStats()}
function reveal(fid){state.revealed.add(fid);rCard()}
function retry(fid){state.revealed.delete(fid);rCard()}
function markM(fid){state.mastered[fid]=Date.now();saveP();uStats();rCard();rSidebar();
  const kp=cKP();if(kp&&kp.formulas.every(f=>state.mastered[f.id])){showCel('本知识点全部掌握！')}
  if(state.unmasteredOnly){const kp=cKP();if(kp&&kp.formulas.filter(f=>!state.mastered[f.id]).length===0){const kps=fKPs();const idx=kps.findIndex(k=>k.id===kp.id);if(idx<kps.length-1)setTimeout(function(){selKP(kps[idx+1].id)},500)}}
}
function markF(fid){delete state.mastered[fid];saveP();uStats();rCard();rSidebar()}
function expandAll(){const kp=cKP();if(kp){kp.formulas.forEach(f=>state.revealed.add(f.id));rCard()}}
function collapseAll(){state.revealed=new Set;rCard()}
function toggleMust(){state.mustOnly=!state.mustOnly;syncToggles();const kps=fKPs();state.currentKP=kps.length>0?kps[0].id:null;state.revealed=new Set;rSidebar();rCard();uStats()}
function toggleUnmastered(){state.unmasteredOnly=!state.unmasteredOnly;syncToggles();rCard()}
function toggleDark(){state.darkMode=!state.darkMode;applyTheme();syncToggles();saveS()}
function syncToggles(){
  var m2=document.getElementById('toggle-must2'),u2=document.getElementById('toggle-unmastered2'),d2=document.getElementById('toggle-dark2');
  if(m2)m2.classList.toggle('on',state.mustOnly);
  if(u2)u2.classList.toggle('on',state.unmasteredOnly);
  if(d2)d2.classList.toggle('on',state.darkMode);
}
function applyTheme(){if(state.darkMode){document.documentElement.setAttribute('data-theme','dark')}else{document.documentElement.removeAttribute('data-theme')}}
function resetCurrentKP(){const kp=cKP();if(!kp)return;showCfm('重置当前知识点「'+kp.name+'」的所有进度？',function(){kp.formulas.forEach(f=>delete state.mastered[f.id]);state.revealed=new Set;saveP();rSidebar();rCard();uStats()})}
function resetAll(){showCfm('确定清空全部学习进度？此操作不可撤销。',function(){state.mastered={};state.revealed=new Set;saveP();rSidebar();rCard();uStats()})}
function showCel(m){const el=document.createElement('div');el.className='celebration';el.textContent=m;document.body.appendChild(el);setTimeout(function(){el.style.opacity='0';el.style.transition='opacity .5s ease';setTimeout(function(){el.remove()},500)},3000)}
function showToast(m,t){const el=document.createElement('div');el.className='toast'+(t?' '+t:'');el.textContent=m;document.body.appendChild(el);setTimeout(function(){el.style.opacity='0';el.style.transition='opacity .3s';setTimeout(function(){el.remove()},300)},2500)}
function showCfm(m,cb){const ov=document.createElement('div');ov.className='dialog-overlay';ov.innerHTML='<div class="dialog-box"><p class="dialog-text">'+m+'</p><div class="dialog-actions"><button class="btn-forget" onclick="this.closest(\'.dialog-overlay\').remove()">取消</button><button class="btn-master" id="dok">确定</button></div></div>';document.body.appendChild(ov);ov.querySelector('#dok').onclick=function(){ov.remove();cb()};ov.addEventListener('click',function(e){if(e.target===ov)ov.remove()})}
function showDailyModal(f){if(!f&&!shouldDaily())return;document.getElementById('daily-modal').classList.remove('hidden');document.getElementById('bell-dot').style.display='none'}
function closeDailyModal(){document.getElementById('daily-modal').classList.add('hidden');document.getElementById('bell-dot').style.display='block'}
function shouldDaily(){var today=new Date().toISOString().slice(0,10);var ver=localStorage.getItem('kaoyan_modal_ver')||'';if(state.dailyLastDate!==today||ver!=='v5.0.2'){state.dailyLastDate=today;localStorage.setItem('kaoyan_modal_ver','v5.0.2');saveS();return true}return false}
function toggleSidebar(){const sb=document.getElementById('sidebar'),ov=document.getElementById('sidebar-overlay');sb.classList.toggle('open');ov.classList.toggle('show')}
function openSettings(){syncToggles();document.getElementById('settings-modal').classList.remove('hidden')}
function closeSettings(){document.getElementById('settings-modal').classList.add('hidden')}
function exportProgress(){const d={mastered:state.mastered,date:new Date().toISOString()};const b=new Blob([JSON.stringify(d,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='考研数学练卡_进度_'+new Date().toISOString().slice(0,10)+'.json';a.click();URL.revokeObjectURL(a.href);showToast('进度已导出','success')}
function importProgress(e){const file=e.target.files[0];if(!file)return;const r=new FileReader();r.onload=function(ev){try{const d=JSON.parse(ev.target.result);if(d.mastered){showCfm('导入将覆盖当前进度，确定吗？',function(){state.mastered=d.mastered;saveP();rSidebar();rCard();uStats();showToast('进度已导入','success')})}else showToast('文件格式无效')}catch(er){showToast('文件格式错误')}};r.readAsText(file);e.target.value=''}
async function checkUpdate(){try{const r=await fetch('version.txt',{cache:'no-cache'});if(!r.ok)return;const v=(await r.text()).trim();if(v&&v!=='v5.0.0'){showToast('新版本已就绪，3秒后刷新...','update');setTimeout(function(){location.reload()},3000)}}catch(e){}}
document.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;if(e.key==='e'||e.key==='E')expandAll();if(e.key==='c'||e.key==='C')collapseAll()});
window.addEventListener('resize',function(){if(window.innerWidth>768){document.getElementById('sidebar').classList.remove('open');document.getElementById('sidebar-overlay').classList.remove('show')}});
function init(){
  loadP();loadS();applyTheme();rPills();rSidebar();uStats();
  const kps=fKPs();if(kps.length>0){state.currentKP=kps[0].id;rSidebar();rCard()}
  setTimeout(function(){if(shouldDaily())showDailyModal(true)},600);
  setTimeout(checkUpdate,2000);
  if('serviceWorker' in navigator){navigator.serviceWorker.register('sw.js').catch(function(){})}
}
init();
</script>
</body>
</html>'''

# Embed data (base64 encoded in HTML, decoded at runtime)
html = html.replace('__DATA_B64__', kps_b64)
html = html.replace('__TOTAL_PLACEHOLDER__', str(data['total_formulas']))
html = html.replace('__KATEX_CSS__', katex_css)
html = html.replace('__KATEX_JS__', katex_js)

out = os.path.join(BASE, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(out) / 1024
print(f'Built: {size_kb:.0f} KB | {data["total_knowledge_points"]} KPs, {data["total_formulas"]} formulas')

# Quick verify
with open(out, 'r', encoding='utf-8') as f:
    check = f.read()
# Check for tab escape issue
if "'\\\\text{$&}'" in check or "'\\text{$&}'" in check:
    # Check if it's double or single
    idx = check.find("const w=t.replace")
    segment = check[idx:idx+80]
    if segment.count('\\\\text') >= 1:
        print('OK - double backslash for text')
    else:
        print('WARN - check text escaping')
# Verify data (base64 encoded)
import re as _re
m = _re.search(r"var _D='([^']+)'", check)
if m:
    jd = json.loads(base64.b64decode(m.group(1)).decode('utf-8'))
    print(f'Verify: {len(jd)} KPs loaded')
