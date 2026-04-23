#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取所有 JSON 数据，生成完整的政协委员通 app.html
图片使用真实本地路径（file:// 绝对路径），街道名单全量显示
"""
import json, os, sys

BASE = r'C:\Users\HWH\Desktop\the lab report of web\classwork\政协委员通'
DATA = os.path.join(BASE, 'data_web')
OUT  = r'C:\Users\HWH\WorkBuddy\20260423093457\app.html'

def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)

members_data  = load('members_by_district.json')
studios_data  = load('studios.json')
platform_data = load('platform_studios.json')
plan_data     = load('duty_plan_2026.json')
act_photos    = load('activity_photos.json')
stu_photos    = load('studio_photos.json')

# 把图片路径转成 file:// 绝对路径
PHOTO_BASE_JIEBEI = BASE + r'\data\3. 界别基本情况\活动照片'
PHOTO_BASE_STUDIO = BASE + r'\data\5. 委员履职平台'

def jiebei_img_url(photo):
    p = os.path.join(PHOTO_BASE_JIEBEI, photo['jiebei'], photo['filename'])
    return 'file:///' + p.replace('\\', '/')

def studio_img_url(photo):
    p = os.path.join(PHOTO_BASE_STUDIO, photo['filename'])
    return 'file:///' + p.replace('\\', '/')

# 更新照片 URL
for ph in act_photos['photos']:
    ph['url'] = jiebei_img_url(ph)
for ph in stu_photos['photos']:
    ph['url'] = studio_img_url(ph)

# 序列化为 JS 内联数据（compact）
def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

members_js  = js(members_data)
studios_js  = js(studios_data)
platform_js = js(platform_data)
plan_js     = js(plan_data)
actphotos_js= js(act_photos)
stuphotos_js= js(stu_photos)

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>政协委员通 · 杭州市上城区政协</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
:root{
  --red:#c0252d;--red-dark:#8f0d14;--red-deep:#6b0000;
  --red-light:#f8e9ea;--red-pale:#fdf3f3;
  --white:#fff;--bg:#f5f6f8;--surface:#fff;
  --border:#e2e5ec;--border2:#d0d4dd;
  --text1:#1a1e2e;--text2:#4a5068;--text3:#8892a4;--textinv:#fff;
  --gold:#b8860b;--gold-bg:#fff8e8;
  --blue:#1a56a8;--blue-bg:#eaf1fb;
  --green:#217a45;--green-bg:#e8f5ee;
  --sh-sm:0 1px 3px rgba(0,0,0,.08);
  --sh-md:0 4px 12px rgba(0,0,0,.10);
  --sh-lg:0 8px 28px rgba(0,0,0,.13);
  --r-sm:4px;--r-md:8px;--r-lg:12px;--r-xl:16px;
  --ease-out:cubic-bezier(.22,.68,0,1.2);
  --ease-std:cubic-bezier(.4,0,.2,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
body{font-family:'Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text1);font-size:14px;line-height:1.6;min-height:100vh}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer;border:none;background:none}
input,select{font-family:inherit}
ul{list-style:none}
img{display:block;max-width:100%;object-fit:cover}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}

/* ── gov banner ── */
.gov-banner{background:var(--red-deep);color:rgba(255,255,255,.75);font-size:12px;padding:5px 24px;display:flex;align-items:center;justify-content:space-between}
.gov-banner a{color:rgba(255,255,255,.7);transition:color .15s}.gov-banner a:hover{color:#fff}

/* ── header ── */
.header{background:var(--red);color:#fff;box-shadow:0 2px 12px rgba(144,13,20,.35);position:sticky;top:0;z-index:200}
.header-inner{max-width:1340px;margin:0 auto;padding:0 24px;display:flex;align-items:center;gap:24px;height:64px}
.logo{display:flex;align-items:center;gap:12px;flex-shrink:0}
.logo-emblem{width:44px;height:44px;background:rgba(255,255,255,.15);border:2px solid rgba(255,255,255,.4);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700}
.logo-title{font-size:19px;font-weight:700;font-family:'Noto Serif SC',serif;letter-spacing:.04em;line-height:1.2}
.logo-sub{font-size:11px;opacity:.72;letter-spacing:.05em}
.topnav{flex:1;display:flex;align-items:center;gap:2px;overflow-x:auto}
.topnav::-webkit-scrollbar{height:0}
.nav-item{display:flex;align-items:center;gap:6px;padding:6px 14px;border-radius:var(--r-sm);font-size:13.5px;font-weight:500;color:rgba(255,255,255,.85);white-space:nowrap;transition:background .15s,color .15s,transform .15s;position:relative;cursor:pointer}
.nav-item::after{content:'';position:absolute;bottom:-2px;left:50%;width:0;height:2px;background:#fff;border-radius:1px;transition:width .22s var(--ease-std),left .22s var(--ease-std)}
.nav-item:hover{background:rgba(255,255,255,.14);color:#fff}
.nav-item:hover::after{width:60%;left:20%}
.nav-item.active{background:rgba(255,255,255,.2);color:#fff;font-weight:600}
.nav-item.active::after{width:70%;left:15%}
.nav-item:active{transform:scale(.97)}
.nav-icon{font-size:15px;line-height:1}
.hdr-actions{display:flex;align-items:center;gap:8px;flex-shrink:0}
.hdr-btn{padding:6px 14px;border-radius:var(--r-md);font-size:12.5px;font-weight:500;color:rgba(255,255,255,.9);background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);transition:background .15s,transform .15s}
.hdr-btn:hover{background:rgba(255,255,255,.22);transform:translateY(-1px)}

/* ── main ── */
.main{flex:1;max-width:1340px;margin:0 auto;width:100%;padding:24px}

/* ── page anim ── */
.page-enter{animation:pageIn .35s var(--ease-out) both}
@keyframes pageIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

/* ── hero ── */
.hero{background:linear-gradient(135deg,var(--red-dark) 0%,var(--red) 55%,#e83a3a 100%);color:#fff;border-radius:var(--r-xl);padding:32px 40px;margin-bottom:32px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat}
.hero::after{content:'';position:absolute;right:-60px;top:-60px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.06)}
.hero-eyebrow{font-size:12px;opacity:.75;letter-spacing:.1em;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.hero-dot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.6)}
.hero-title{font-size:26px;font-weight:700;font-family:'Noto Serif SC',serif;margin-bottom:8px;position:relative;z-index:1}
.hero-sub{font-size:13px;opacity:.8;position:relative;z-index:1;line-height:1.8}

/* ── stat cards ── */
.stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:32px}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:20px;display:flex;flex-direction:column;gap:8px;transition:box-shadow .22s,transform .22s,border-color .22s;cursor:default}
.stat-card:hover{box-shadow:var(--sh-md);transform:translateY(-2px);border-color:var(--red-light)}
.stat-num{font-size:28px;font-weight:700;color:var(--red);font-family:'Noto Serif SC',serif;line-height:1}
.stat-label{font-size:13px;color:var(--text2)}
.stat-icon{font-size:28px;margin-bottom:4px}

/* ── section ── */
.sec{margin-bottom:32px}
.sec-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.sec-title{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:700;color:var(--text1)}
.sec-bar{width:4px;height:18px;background:var(--red);border-radius:2px;flex-shrink:0}
.link-more{font-size:12px;color:var(--red);display:flex;align-items:center;gap:4px;cursor:pointer;font-weight:500;transition:opacity .15s,gap .15s}
.link-more:hover{opacity:.75;gap:7px}

/* ── card grid ── */
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.card-grid-3{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}

/* ── generic card ── */
.card{background:var(--surface);border:2px solid var(--border);border-radius:var(--r-lg);padding:20px;transition:box-shadow .22s,transform .22s,border-color .22s;cursor:pointer;position:relative}
.card:hover{box-shadow:var(--sh-md);transform:translateY(-2px);border-color:var(--red-light)}
.card.selected{border-color:var(--red);background:var(--red-pale);box-shadow:0 0 0 3px rgba(192,37,45,.12)}
.card-check{position:absolute;top:10px;right:10px;width:22px;height:22px;border-radius:50%;background:var(--red);display:flex;align-items:center;justify-content:center;animation:popIn .25s var(--ease-out) both}
@keyframes popIn{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
.card-name{font-size:15px;font-weight:600;color:var(--text1);margin-bottom:6px}
.card-info{font-size:13px;color:var(--text2);line-height:1.7}
.card-meta{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.tag{display:inline-flex;align-items:center;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:500}
.tag-red{background:var(--red-light);color:var(--red)}
.tag-blue{background:var(--blue-bg);color:var(--blue)}
.tag-gold{background:var(--gold-bg);color:var(--gold)}
.tag-green{background:var(--green-bg);color:var(--green)}
.tag-gray{background:#f0f1f4;color:var(--text2)}

/* ── search bar ── */
.search-bar{display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.search-input{flex:1;min-width:220px;padding:9px 14px 9px 38px;border:1.5px solid var(--border2);border-radius:var(--r-md);font-size:14px;background:var(--surface);transition:border-color .15s,box-shadow .15s;outline:none;color:var(--text1)}
.search-input:focus{border-color:var(--red);box-shadow:0 0 0 3px rgba(192,37,45,.1)}
.search-wrap{position:relative;flex:1}
.search-icon{position:absolute;left:11px;top:50%;transform:translateY(-50%);font-size:15px;color:var(--text3);pointer-events:none}
.filter-btns{display:flex;flex-wrap:wrap;gap:8px}
.filter-btn{padding:7px 14px;border-radius:var(--r-md);font-size:13px;font-weight:500;border:1.5px solid var(--border2);color:var(--text2);background:var(--surface);transition:all .15s;cursor:pointer}
.filter-btn:hover{border-color:var(--red);color:var(--red);background:var(--red-pale)}
.filter-btn.active{border-color:var(--red);color:var(--red);background:var(--red-light);font-weight:600}

/* ── tab bar ── */
.tab-bar{display:flex;gap:4px;border-bottom:2px solid var(--border);margin-bottom:24px;overflow-x:auto}
.tab-bar::-webkit-scrollbar{height:0}
.tab{padding:10px 18px;font-size:14px;font-weight:500;color:var(--text2);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;transition:color .15s,border-color .15s;white-space:nowrap}
.tab:hover{color:var(--red)}
.tab.active{color:var(--red);border-bottom-color:var(--red);font-weight:600}

/* ── table ── */
.tbl-wrap{overflow-x:auto;border-radius:var(--r-lg);border:1px solid var(--border);background:var(--surface)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
thead{background:linear-gradient(135deg,var(--red-dark),var(--red));color:#fff}
th{padding:11px 16px;text-align:left;font-weight:600;font-size:13px;letter-spacing:.02em}
td{padding:10px 16px;border-bottom:1px solid var(--border);color:var(--text1)}
tr:last-child td{border-bottom:none}
tr.row-hover:hover td{background:var(--red-pale)}
tr.row-selected td{background:var(--red-pale) !important}
tr.row-selected td:first-child{border-left:3px solid var(--red)}

/* ── district group card ── */
.district-card{background:var(--surface);border:2px solid var(--border);border-radius:var(--r-lg);overflow:hidden;transition:box-shadow .22s,border-color .22s;cursor:pointer}
.district-card:hover{box-shadow:var(--sh-md);border-color:var(--red-light)}
.district-card.selected{border-color:var(--red);box-shadow:0 0 0 3px rgba(192,37,45,.12)}
.district-hd{padding:16px 20px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,var(--red-pale) 0%,#fff 100%)}
.district-name{font-size:15px;font-weight:700;color:var(--text1)}
.district-count{font-size:12px;font-weight:600;padding:3px 10px;background:var(--red);color:#fff;border-radius:20px}
.district-body{padding:0 16px 16px}
.member-table{width:100%;border-collapse:collapse;font-size:13px;margin-top:12px}
.member-table th{padding:7px 12px;text-align:left;background:var(--bg);color:var(--text2);font-weight:600;border-bottom:1px solid var(--border);font-size:12px}
.member-table td{padding:7px 12px;border-bottom:1px solid var(--border);color:var(--text1)}
.member-table tr:last-child td{border-bottom:none}
.member-table tr:hover td{background:var(--red-pale)}
.member-table tr.selected-row td{background:var(--red-pale);border-left:3px solid var(--red)}

/* ── photo grid ── */
.photo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.photo-item{border-radius:var(--r-md);overflow:hidden;aspect-ratio:4/3;background:var(--bg);position:relative;cursor:pointer;transition:transform .22s,box-shadow .22s}
.photo-item:hover{transform:scale(1.04);box-shadow:var(--sh-lg);z-index:2}
.photo-item img{width:100%;height:100%;object-fit:cover;transition:transform .3s}
.photo-item:hover img{transform:scale(1.06)}
.photo-item .photo-label{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.55));padding:6px 8px 5px;color:#fff;font-size:11px;text-align:center}
/* img fallback */
.img-fallback{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--red-pale),var(--red-light));color:var(--red);font-size:11px;gap:4px;padding:8px;text-align:center}

/* ── star badge ── */
.star-badge{display:inline-flex;align-items:center;gap:3px;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600}
.star-5{background:#fff3cd;color:#b8860b;border:1px solid #e6c200}
.star-4{background:#e8f5ee;color:#217a45;border:1px solid #90c7a5}
.star-3{background:#eaf1fb;color:#1a56a8;border:1px solid #99bae6}

/* ── progress bar ── */
.prog-row{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.prog-label{min-width:80px;font-size:13px;color:var(--text2)}
.prog-bar{flex:1;height:8px;background:var(--bg);border-radius:4px;overflow:hidden}
.prog-fill{height:100%;border-radius:4px;background:var(--red);transition:width .6s var(--ease-out)}
.prog-val{min-width:36px;font-size:13px;font-weight:600;color:var(--text1);text-align:right}

/* ── timeline ── */
.timeline{display:flex;flex-direction:column;gap:0}
.tl-item{display:flex;gap:16px;padding:12px 0;border-bottom:1px dashed var(--border)}
.tl-item:last-child{border-bottom:none}
.tl-dot{width:10px;height:10px;border-radius:50%;background:var(--red);flex-shrink:0;margin-top:5px}
.tl-time{min-width:70px;font-size:12px;color:var(--text3);padding-top:2px}
.tl-name{font-size:14px;font-weight:500;color:var(--text1)}
.tl-meta{font-size:12px;color:var(--text2);margin-top:2px}

/* ── loading skeleton ── */
.skel{background:linear-gradient(90deg,#f0f1f4 25%,#e4e6eb 50%,#f0f1f4 75%);background-size:200% 100%;animation:skel 1.4s ease infinite;border-radius:var(--r-sm)}
@keyframes skel{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* ── responsive ── */
@media(max-width:768px){
  .main{padding:16px}
  .hero{padding:24px 20px}
  .hero-title{font-size:20px}
  .stat-row{grid-template-columns:repeat(2,1fr)}
  .card-grid{grid-template-columns:1fr}
  .header-inner{gap:12px;padding:0 16px}
  .logo-sub{display:none}
}
@media(max-width:480px){
  .stat-row{grid-template-columns:1fr 1fr}
  .topnav{gap:0}
  .nav-item{padding:5px 10px;font-size:12.5px}
}
</style>
</head>
<body>
<div id="root"></div>

<!-- ═══════════════════════════════════════════════════════════
     INLINE DATA (all JSON embedded, no CORS / file:// issues)
     ═══════════════════════════════════════════════════════════ -->
<script>
window.__MEMBERS__  = """ + members_js + r""";
window.__STUDIOS__  = """ + studios_js + r""";
window.__PLATFORM__ = """ + platform_js + r""";
window.__PLAN__     = """ + plan_js + r""";
window.__ACT_PHOTOS__= """ + actphotos_js + r""";
window.__STU_PHOTOS__= """ + stuphotos_js + r""";
</script>

<script type="text/babel">
const {useState, useMemo, useCallback, useRef, useEffect} = React;

/* ── nav config ── */
const NAV = [
  {id:'home',     icon:'🏛',  label:'首页'},
  {id:'members',  icon:'👤',  label:'委员之家'},
  {id:'district', icon:'🗺',  label:'街道小组'},
  {id:'jiebei',   icon:'⭐',  label:'界别风采'},
  {id:'consult',  icon:'🤝',  label:'协商民主'},
  {id:'platform', icon:'📋',  label:'履职平台'},
  {id:'studios',  icon:'🏢',  label:'委员工作室'},
  {id:'plan',     icon:'📅',  label:'履职计划'},
];

/* ── Image component with fallback ── */
function Img({src, alt='', label='', className=''}){
  const [err, setErr] = useState(false);
  return err ? (
    <div className={`img-fallback ${className}`}>
      <span style={{fontSize:28}}>🖼</span>
      <span>{label || alt || '图片'}</span>
    </div>
  ) : (
    <img src={src} alt={alt} className={className}
      onError={()=>setErr(true)} loading="lazy"/>
  );
}

/* ── Photo grid ── */
function PhotoGrid({photos, maxShow=20}){
  const [show, setShow] = useState(maxShow);
  const items = photos.slice(0, show);
  return (
    <div>
      <div className="photo-grid">
        {items.map((p,i)=>(
          <div className="photo-item" key={i}>
            <Img src={p.url} alt={p.filename} label={p.jiebei||p.filename} />
            {(p.jiebei||p.filename) &&
              <div className="photo-label">{p.jiebei||p.filename}</div>}
          </div>
        ))}
      </div>
      {photos.length > show &&
        <button className="filter-btn" style={{marginTop:16}}
          onClick={()=>setShow(s=>s+20)}>
          加载更多 ({photos.length - show} 张剩余)
        </button>}
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: HOME
   ══════════════════════════════════ */
function PageHome(){
  const plat = window.__PLATFORM__;
  const mem  = window.__MEMBERS__;
  const stu  = window.__STUDIOS__;
  const plan = window.__PLAN__;
  const totalMembers = mem.groups.reduce((s,g)=>s+g.members.length,0);
  const totalActs    = plan.plan.reduce((s,g)=>s+g.activities.length,0);
  const st = plat.statistics;

  // Latest activities from plan
  const recentActs = plan.plan.slice(0,6).flatMap(g=>
    g.activities.slice(0,2).map(a=>({...a, jiebei:g.jiebei}))
  ).slice(0,8);

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>政协杭州市上城区委员会</div>
        <div className="hero-title">政协委员通 · 履职服务平台</div>
        <div className="hero-sub">
          汇聚全区 {totalMembers} 名政协委员 · {stu.total} 个工作室 · {totalActs} 项年度履职计划<br/>
          {plat.district}政协 · {new Date().getFullYear()} 年度数据版本
        </div>
      </div>

      <div className="stat-row">
        <div className="stat-card"><div className="stat-icon">👥</div><div className="stat-num">{totalMembers}</div><div className="stat-label">在册政协委员</div></div>
        <div className="stat-card"><div className="stat-icon">🗺</div><div className="stat-num">{mem.groups.length}</div><div className="stat-label">街道委员小组</div></div>
        <div className="stat-card"><div className="stat-icon">🏢</div><div className="stat-num">{stu.total}</div><div className="stat-label">委员工作室</div></div>
        <div className="stat-card"><div className="stat-icon">⭐</div><div className="stat-num">{st.star_ratings_2025.five_star}</div><div className="stat-label">五星工作室</div></div>
        <div className="stat-card"><div className="stat-icon">🌟</div><div className="stat-num">{st.star_ratings_2025.four_star}</div><div className="stat-label">四星工作室</div></div>
        <div className="stat-card"><div className="stat-icon">📅</div><div className="stat-num">{totalActs}</div><div className="stat-label">年度履职计划</div></div>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:24}}>
        <div className="sec">
          <div className="sec-hd"><div className="sec-title"><div className="sec-bar"/>工作室星级分布</div></div>
          <div style={{background:'var(--surface)',borderRadius:'var(--r-lg)',padding:20,border:'1px solid var(--border)'}}>
            {[
              {label:'五星工作室',val:st.star_ratings_2025.five_star,max:stu.total,emoji:'⭐⭐⭐⭐⭐'},
              {label:'四星工作室',val:st.star_ratings_2025.four_star,max:stu.total,emoji:'⭐⭐⭐⭐'},
              {label:'三星工作室',val:st.star_ratings_2025.three_star,max:stu.total,emoji:'⭐⭐⭐'},
            ].map(r=>(
              <div className="prog-row" key={r.label}>
                <div className="prog-label">{r.label}</div>
                <div className="prog-bar"><div className="prog-fill" style={{width:`${r.val/r.max*100}%`}}/></div>
                <div className="prog-val">{r.val}</div>
              </div>
            ))}
            <p style={{fontSize:12,color:'var(--text3)',marginTop:12}}>数据来源：2025年度星级评定结果</p>
          </div>
        </div>

        <div className="sec">
          <div className="sec-hd"><div className="sec-title"><div className="sec-bar"/>近期履职动态</div></div>
          <div className="timeline">
            {recentActs.map((a,i)=>(
              <div className="tl-item" key={i}>
                <div className="tl-dot"/>
                <div>
                  <div className="tl-name">{a.name}</div>
                  <div className="tl-meta">{a.jiebei} · {a.type} · {a.plannedTime}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="sec" style={{marginTop:24}}>
        <div className="sec-hd"><div className="sec-title"><div className="sec-bar"/>平台简介</div></div>
        <div style={{background:'var(--surface)',borderRadius:'var(--r-lg)',padding:20,border:'1px solid var(--border)',lineHeight:1.9,color:'var(--text1)',fontSize:14}}>
          {plat.overview}
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: MEMBERS
   ══════════════════════════════════ */
function PageMembers(){
  const {groups} = window.__MEMBERS__;
  const [search, setSearch] = useState('');
  const [group,  setGroup]  = useState('all');
  const [selRow, setSelRow] = useState(null);

  const allMembers = useMemo(()=>
    groups.flatMap(g=>g.members.map(m=>({...m, groupName:g.groupName}))),
  []);

  const filtered = useMemo(()=>{
    let arr = group === 'all' ? allMembers : allMembers.filter(m=>m.groupName===group);
    if(search.trim()){
      const q = search.trim();
      arr = arr.filter(m=>
        m.name.includes(q) || m.position.includes(q) || m.party.includes(q)
      );
    }
    return arr;
  },[search,group,allMembers]);

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>委员名录</div>
        <div className="hero-title">委员之家</div>
        <div className="hero-sub">全区 {allMembers.length} 名政协委员 · 共 {groups.length} 个街道分组</div>
      </div>
      <div className="search-bar">
        <div className="search-wrap">
          <span className="search-icon">🔍</span>
          <input className="search-input" placeholder="搜索委员姓名、单位、党派…"
            value={search} onChange={e=>setSearch(e.target.value)}/>
        </div>
        <div className="filter-btns">
          <button className={`filter-btn${group==='all'?' active':''}`} onClick={()=>setGroup('all')}>全部</button>
          {groups.map(g=>(
            <button key={g.groupName}
              className={`filter-btn${group===g.groupName?' active':''}`}
              onClick={()=>setGroup(g.groupName)}>
              {g.groupName}
            </button>
          ))}
        </div>
      </div>
      <div style={{marginBottom:12,fontSize:13,color:'var(--text3)'}}>共 {filtered.length} 人</div>
      <div className="tbl-wrap">
        <table>
          <thead><tr><th>序号</th><th>姓名</th><th>党派</th><th>性别</th><th>所属小组</th><th>工作单位及职务</th></tr></thead>
          <tbody>
            {filtered.map((m,i)=>(
              <tr key={i} className={`row-hover${selRow===i?' row-selected':''}`}
                onClick={()=>setSelRow(i===selRow?null:i)} style={{cursor:'pointer'}}>
                <td><span className="tag tag-gray">{m.id||i+1}</span></td>
                <td><strong>{m.name}</strong></td>
                <td><span className="tag tag-blue">{m.party}</span></td>
                <td>{m.gender}</td>
                <td><span className="tag tag-red">{m.groupName}</span></td>
                <td style={{maxWidth:280}}>{m.position}</td>
              </tr>
            ))}
            {filtered.length===0 && <tr><td colSpan={6} style={{textAlign:'center',padding:32,color:'var(--text3)'}}>未找到匹配的委员</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: DISTRICT  —— 街道小组（全量展开）
   ══════════════════════════════════ */
function PageDistrict(){
  const {groups, title} = window.__MEMBERS__;
  const [selGroup, setSelGroup] = useState(null);
  const [selMem,   setSelMem]   = useState(null);
  const [search,   setSearch]   = useState('');

  // 全局搜索委员
  const searchResult = useMemo(()=>{
    if(!search.trim()) return null;
    const q = search.trim();
    return groups.flatMap(g=>
      g.members
        .filter(m=>m.name.includes(q)||m.position.includes(q)||m.party.includes(q))
        .map(m=>({...m, groupName:g.groupName}))
    );
  },[search]);

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>委员分布</div>
        <div className="hero-title">街道委员小组</div>
        <div className="hero-sub">{title}</div>
      </div>

      {/* 全局搜索 */}
      <div className="search-bar" style={{marginBottom:24}}>
        <div className="search-wrap">
          <span className="search-icon">🔍</span>
          <input className="search-input" placeholder="跨小组搜索委员姓名、单位…"
            value={search} onChange={e=>{setSearch(e.target.value);setSelGroup(null)}}/>
        </div>
        {search && <button className="filter-btn active" onClick={()=>setSearch('')}>清除搜索</button>}
      </div>

      {/* 搜索结果 */}
      {searchResult && (
        <div className="sec">
          <div className="sec-hd">
            <div className="sec-title"><div className="sec-bar"/>搜索结果（{searchResult.length} 人）</div>
          </div>
          <div className="tbl-wrap">
            <table>
              <thead><tr><th>姓名</th><th>党派</th><th>性别</th><th>所属小组</th><th>工作单位及职务</th></tr></thead>
              <tbody>
                {searchResult.map((m,i)=>(
                  <tr key={i} className="row-hover">
                    <td><strong>{m.name}</strong></td>
                    <td><span className="tag tag-blue">{m.party}</span></td>
                    <td>{m.gender}</td>
                    <td><span className="tag tag-red">{m.groupName}</span></td>
                    <td>{m.position}</td>
                  </tr>
                ))}
                {searchResult.length===0 &&
                  <tr><td colSpan={5} style={{textAlign:'center',padding:24,color:'var(--text3)'}}>未找到匹配委员</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 分组卡片列表（全量展示所有委员） */}
      {!search && (
        <div style={{display:'flex',flexDirection:'column',gap:20}}>
          {groups.map(g=>{
            const isOpen = selGroup === g.groupName;
            return (
              <div key={g.groupName}
                className={`district-card${isOpen?' selected':''}`}
                onClick={()=>{ setSelGroup(isOpen ? null : g.groupName); setSelMem(null); }}>
                <div className="district-hd">
                  <div className="district-name">
                    {isOpen ? '▼' : '▶'} {g.groupName}
                  </div>
                  <div style={{display:'flex',alignItems:'center',gap:8}}>
                    <span className="district-count">{g.members.length} 人</span>
                    {isOpen && <span className="tag tag-red">已展开</span>}
                  </div>
                </div>

                {/* 展开后显示全量委员表格 */}
                {isOpen && (
                  <div className="district-body" onClick={e=>e.stopPropagation()}>
                    <table className="member-table">
                      <thead>
                        <tr>
                          <th>序号</th>
                          <th>姓名</th>
                          <th>党派</th>
                          <th>性别</th>
                          <th>工作单位及职务</th>
                        </tr>
                      </thead>
                      <tbody>
                        {g.members.map((m,i)=>(
                          <tr key={i}
                            className={selMem===`${g.groupName}-${i}` ? 'selected-row' : ''}
                            onClick={()=>setSelMem(
                              selMem===`${g.groupName}-${i}` ? null : `${g.groupName}-${i}`
                            )}
                            style={{cursor:'pointer'}}>
                            <td><span className="tag tag-gray">{m.id||i+1}</span></td>
                            <td><strong>{m.name}</strong></td>
                            <td><span className="tag tag-blue">{m.party}</span></td>
                            <td>{m.gender}</td>
                            <td>{m.position}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    <p style={{fontSize:12,color:'var(--text3)',marginTop:8,textAlign:'right'}}>
                      共 {g.members.length} 位委员 · 点击行高亮选中
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: JIEBEI 界别风采
   ══════════════════════════════════ */
function PageJiebei(){
  const {plan} = window.__PLAN__;
  const photos  = window.__ACT_PHOTOS__.photos;
  const [tab, setTab]       = useState('overview');
  const [selJB, setSelJB]   = useState(null);

  // group photos by jiebei
  const photosByJB = useMemo(()=>{
    const m={};
    photos.forEach(p=>{ if(!m[p.jiebei]) m[p.jiebei]=[]; m[p.jiebei].push(p); });
    return m;
  },[]);

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>界别</div>
        <div className="hero-title">界别风采</div>
        <div className="hero-sub">共 {plan.length} 个界别 · 年度履职动态 · 活动精彩瞬间</div>
      </div>
      <div className="tab-bar">
        {[{id:'overview',label:'界别总览'},{id:'photos',label:'活动照片'},{id:'plan',label:'履职计划'}].map(t=>(
          <div key={t.id} className={`tab${tab===t.id?' active':''}`}
            onClick={()=>{setTab(t.id);setSelJB(null)}}>{t.label}</div>
        ))}
      </div>

      {tab==='overview' && (
        <div className="card-grid">
          {plan.map((g,i)=>(
            <div key={i} className={`card${selJB===i?' selected':''}`}
              onClick={()=>setSelJB(i===selJB?null:i)}>
              {selJB===i && <div className="card-check"><span style={{color:'#fff',fontSize:12}}>✓</span></div>}
              <div className="card-name">{g.jiebei}</div>
              <div className="card-info">年度活动：{g.activities.length} 项</div>
              {selJB===i && (
                <div style={{marginTop:12}}>
                  {g.activities.map((a,j)=>(
                    <div key={j} style={{padding:'6px 0',borderBottom:'1px dashed var(--border)',fontSize:13}}>
                      <div style={{fontWeight:500}}>{a.name}</div>
                      <div style={{color:'var(--text3)',fontSize:12}}>{a.type} · {a.plannedTime}</div>
                    </div>
                  ))}
                </div>
              )}
              <div className="card-meta">
                {g.activities.slice(0,2).map((a,j)=>(
                  <span key={j} className="tag tag-gray">{a.type}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {tab==='photos' && (
        <div>
          {Object.entries(photosByJB).map(([jb, phs])=>(
            <div className="sec" key={jb}>
              <div className="sec-hd">
                <div className="sec-title"><div className="sec-bar"/>{jb}（{phs.length}张）</div>
              </div>
              <PhotoGrid photos={phs} maxShow={8}/>
            </div>
          ))}
          {Object.keys(photosByJB).length===0 &&
            <p style={{color:'var(--text3)',padding:32,textAlign:'center'}}>暂无活动照片</p>}
        </div>
      )}

      {tab==='plan' && (
        <div className="tbl-wrap">
          <table>
            <thead><tr><th>界别</th><th>活动名称</th><th>活动类型</th><th>拟召开时间</th></tr></thead>
            <tbody>
              {plan.flatMap((g,gi)=>g.activities.map((a,ai)=>(
                <tr key={`${gi}-${ai}`} className="row-hover">
                  <td><span className="tag tag-red">{g.jiebei}</span></td>
                  <td>{a.name}</td>
                  <td><span className="tag tag-blue">{a.type}</span></td>
                  <td>{a.plannedTime}</td>
                </tr>
              )))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: CONSULT 协商民主
   ══════════════════════════════════ */
function PageConsult(){
  const plat = window.__PLATFORM__;
  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>实践中心</div>
        <div className="hero-title">协商民主实践</div>
        <div className="hero-sub">市政协新时代协商民主实践 · {plat.district}分中心</div>
      </div>
      <div className="card-grid" style={{marginBottom:32}}>
        {[
          {icon:'🏛',title:'分中心建设',desc:`${plat.district}分中心依托委员工作室，推进协商民主向基层延伸，覆盖全区各街道委员小组。`},
          {icon:'📣',title:'界别协商',desc:'定期组织各界别委员开展界别协商活动，围绕重点民生议题深入调研，形成高质量提案建议。'},
          {icon:'🤝',title:'民生议事堂',desc:'在各街道设立民生议事堂，搭建委员与居民直接沟通渠道，推动协商成果转化落地。'},
          {icon:'📊',title:'数字协商',desc:'推进协商民主数字化转型，实现协商流程线上化、数据化，提升协商效率与透明度。'},
        ].map((c,i)=>(
          <div className="card" key={i} style={{cursor:'default'}}>
            <div style={{fontSize:32,marginBottom:12}}>{c.icon}</div>
            <div className="card-name">{c.title}</div>
            <div className="card-info">{c.desc}</div>
          </div>
        ))}
      </div>
      <div className="sec">
        <div className="sec-hd"><div className="sec-title"><div className="sec-bar"/>平台概述</div></div>
        <div style={{background:'var(--surface)',borderRadius:'var(--r-lg)',padding:24,border:'1px solid var(--border)',fontSize:14,lineHeight:2,color:'var(--text1)'}}>
          {plat.overview}
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: PLATFORM 履职平台
   ══════════════════════════════════ */
function PagePlatform(){
  const plat    = window.__PLATFORM__;
  const studios = plat.studios || [];
  const photos  = window.__STU_PHOTOS__.photos;
  const st      = plat.statistics;

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>委员工作室</div>
        <div className="hero-title">委员履职平台</div>
        <div className="hero-sub">{st.total_studios} 个委员工作室 · {st.coverage}</div>
      </div>

      <div className="stat-row" style={{marginBottom:32}}>
        <div className="stat-card"><div className="stat-icon">⭐</div><div className="stat-num">{st.star_ratings_2025.five_star}</div><div className="stat-label">五星工作室</div></div>
        <div className="stat-card"><div className="stat-icon">🌟</div><div className="stat-num">{st.star_ratings_2025.four_star}</div><div className="stat-label">四星工作室</div></div>
        <div className="stat-card"><div className="stat-icon">✨</div><div className="stat-num">{st.star_ratings_2025.three_star}</div><div className="stat-label">三星工作室</div></div>
        <div className="stat-card"><div className="stat-icon">🏢</div><div className="stat-num">{st.total_studios}</div><div className="stat-label">工作室总计</div></div>
      </div>

      <div className="sec">
        <div className="sec-hd"><div className="sec-title"><div className="sec-bar"/>工作室活动照片</div></div>
        {photos.length > 0 ? <PhotoGrid photos={photos} maxShow={12}/> :
          <p style={{color:'var(--text3)',textAlign:'center',padding:32}}>暂无工作室活动照片</p>}
      </div>

      {studios.length > 0 && (
        <div className="sec">
          <div className="sec-hd"><div className="sec-title"><div className="sec-bar"/>工作室列表</div></div>
          <div className="card-grid-3">
            {studios.map((s,i)=>(
              <div className="card" key={i} style={{cursor:'default'}}>
                <div className="card-name">{s.name}</div>
                <div className="card-info">领衔：{s.leader}</div>
                <div className="card-info" style={{marginTop:4}}>📍 {s.address}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: STUDIOS 委员工作室
   ══════════════════════════════════ */
function PageStudios(){
  const {studios, total, title} = window.__STUDIOS__;
  const [search, setSearch] = useState('');
  const [sel, setSel]       = useState(null);

  const filtered = useMemo(()=>{
    if(!search.trim()) return studios;
    const q = search.trim();
    return studios.filter(s=>
      s.name.includes(q)||s.leader.includes(q)||s.address.includes(q)
    );
  },[search, studios]);

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>工作室</div>
        <div className="hero-title">委员工作室</div>
        <div className="hero-sub">{title} · 共 {total} 个</div>
      </div>

      <div className="search-bar">
        <div className="search-wrap">
          <span className="search-icon">🔍</span>
          <input className="search-input" placeholder="搜索工作室名称、领衔委员、地址…"
            value={search} onChange={e=>setSearch(e.target.value)}/>
        </div>
        {search && <button className="filter-btn active" onClick={()=>setSearch('')}>清除</button>}
        <span style={{fontSize:13,color:'var(--text3)'}}>共 {filtered.length} 个</span>
      </div>

      <div className="card-grid">
        {filtered.map((s,i)=>(
          <div key={i} className={`card${sel===i?' selected':''}`}
            onClick={()=>setSel(i===sel?null:i)}>
            {sel===i && <div className="card-check"><span style={{color:'#fff',fontSize:12}}>✓</span></div>}
            <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:8}}>
              <span className="tag tag-red" style={{fontWeight:700}}>#{s.id}</span>
            </div>
            <div className="card-name">{s.name}</div>
            <div className="card-info">👤 领衔委员：{s.leader}</div>
            <div className="card-info">📍 {s.address}</div>
          </div>
        ))}
        {filtered.length===0 &&
          <div style={{gridColumn:'1/-1',textAlign:'center',padding:48,color:'var(--text3)'}}>未找到匹配的工作室</div>}
      </div>
    </div>
  );
}

/* ══════════════════════════════════
   PAGE: PLAN 履职计划
   ══════════════════════════════════ */
function PagePlan(){
  const {plan, title} = window.__PLAN__;
  const [tab, setTab]   = useState('all');
  const [selJB, setSelJB] = useState('all');

  const jiebeis = useMemo(()=>plan.map(g=>g.jiebei),[]);
  const allActs = useMemo(()=>
    plan.flatMap(g=>g.activities.map(a=>({...a, jiebei:g.jiebei}))),
  []);

  const shown = useMemo(()=>{
    if(selJB==='all') return allActs;
    return allActs.filter(a=>a.jiebei===selJB);
  },[selJB, allActs]);

  const typeColors = {
    '专题协商':'tag-red', '界别协商':'tag-blue', '民主监督':'tag-green',
    '调研视察':'tag-gold', '反映社情民意':'tag-gray',
  };
  function typeTag(type){ return typeColors[type]||'tag-gray'; }

  return (
    <div className="page-enter">
      <div className="hero">
        <div className="hero-eyebrow"><div className="hero-dot"/>年度计划</div>
        <div className="hero-title">2026年度履职计划</div>
        <div className="hero-sub">{title} · 共 {allActs.length} 项活动</div>
      </div>

      <div className="tab-bar">
        <div className={`tab${tab==='all'?' active':''}`} onClick={()=>setTab('all')}>全部活动</div>
        <div className={`tab${tab==='jiebei'?' active':''}`} onClick={()=>setTab('jiebei')}>按界别筛选</div>
      </div>

      {tab==='jiebei' && (
        <div className="filter-btns" style={{marginBottom:20,flexWrap:'wrap'}}>
          <button className={`filter-btn${selJB==='all'?' active':''}`} onClick={()=>setSelJB('all')}>全部</button>
          {jiebeis.map(jb=>(
            <button key={jb} className={`filter-btn${selJB===jb?' active':''}`}
              onClick={()=>setSelJB(jb)}>{jb}</button>
          ))}
        </div>
      )}

      <div style={{marginBottom:12,fontSize:13,color:'var(--text3)'}}>
        显示 {shown.length} 项活动
        {selJB!=='all' && <> · 界别：<strong style={{color:'var(--red)'}}>{selJB}</strong></>}
      </div>
      <div className="tbl-wrap">
        <table>
          <thead><tr><th>#</th><th>界别</th><th>活动名称</th><th>活动类型</th><th>拟召开时间</th></tr></thead>
          <tbody>
            {shown.map((a,i)=>(
              <tr key={i} className="row-hover">
                <td><span className="tag tag-gray">{i+1}</span></td>
                <td><span className="tag tag-red">{a.jiebei}</span></td>
                <td style={{fontWeight:500}}>{a.name}</td>
                <td><span className={`tag ${typeTag(a.type)}`}>{a.type}</span></td>
                <td>{a.plannedTime}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ══════════════════════════════════
   APP ROOT
   ══════════════════════════════════ */
function App(){
  const [page, setPage] = useState('home');
  const [loading, setLoading] = useState(true);

  // Simulate parallel data init
  useEffect(()=>{
    Promise.all([
      new Promise(r=>setTimeout(r,60)),
      new Promise(r=>setTimeout(r,80)),
      new Promise(r=>setTimeout(r,100)),
    ]).then(()=>setLoading(false));
  },[]);

  const pages = {
    home:     <PageHome/>,
    members:  <PageMembers/>,
    district: <PageDistrict/>,
    jiebei:   <PageJiebei/>,
    consult:  <PageConsult/>,
    platform: <PagePlatform/>,
    studios:  <PageStudios/>,
    plan:     <PagePlan/>,
  };

  return (
    <div style={{display:'flex',flexDirection:'column',minHeight:'100vh'}}>
      {/* Gov Banner */}
      <div className="gov-banner">
        <div style={{display:'flex',gap:20}}>
          <span>杭州市上城区人民政府</span>
          <span>·</span>
          <span>政协杭州市上城区委员会</span>
        </div>
        <div style={{display:'flex',gap:16}}>
          <span>信息公开</span>
          <span>|</span>
          <span>网上办事</span>
          <span>|</span>
          <span>政民互动</span>
        </div>
      </div>

      {/* Header + Nav */}
      <div className="header">
        <div className="header-inner">
          <div className="logo">
            <div className="logo-emblem">政</div>
            <div>
              <div className="logo-title">政协委员通</div>
              <div className="logo-sub">杭州市上城区政协</div>
            </div>
          </div>
          <nav className="topnav">
            {NAV.map(n=>(
              <button key={n.id}
                className={`nav-item${page===n.id?' active':''}`}
                onClick={()=>setPage(n.id)}>
                <span className="nav-icon">{n.icon}</span>{n.label}
              </button>
            ))}
          </nav>
          <div className="hdr-actions">
            <button className="hdr-btn">🔔 通知</button>
            <button className="hdr-btn">👤 登录</button>
          </div>
        </div>
      </div>

      {/* Main */}
      <main className="main">
        {loading ? (
          <div style={{display:'flex',flexDirection:'column',gap:16}}>
            {[240,180,120,160].map((h,i)=>(
              <div key={i} className="skel" style={{height:h,borderRadius:12}}/>
            ))}
          </div>
        ) : (
          <div key={page}>
            {pages[page] || <PageHome/>}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{background:'var(--red-deep)',color:'rgba(255,255,255,.7)',padding:'20px 24px',textAlign:'center',fontSize:12,marginTop:'auto'}}>
        <div>政协杭州市上城区委员会 · 政协委员通履职服务平台</div>
        <div style={{marginTop:6,opacity:.6}}>数据来源：上城区政协 2026 年度工作数据 · 本平台供内部学习与展示</div>
      </footer>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"app.html written: {len(HTML)} chars")
print(f"Members groups: {len(members_data['groups'])}")
print(f"Studios: {studios_data['total']}")
print(f"Plan jiebeis: {len(plan_data['plan'])}")
print(f"Activity photos: {act_photos['count']}")
print(f"Studio photos: {stu_photos['count']}")
