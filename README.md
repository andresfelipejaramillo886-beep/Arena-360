<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>ARENA360 — Deportes, Tecnología & Actualidad</title>
<meta name="description" content="ARENA360 - Tu portal de noticias sobre deportes, tecnología y actualidad mundial"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;0,700;1,400&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
:root {
  --red: #E63946;
  --yellow: #FFD23F;
  --bg: #0D0D0D;
  --bg2: #141414;
  --bg3: #1c1c1c;
  --card: #181818;
  --border: #2a2a2a;
  --text: #F0F0F0;
  --text2: #A0A0A0;
  --text3: #666;
  --white: #FFFFFF;
  --radius: 6px;
  --shadow: 0 4px 24px rgba(0,0,0,0.5);
}
[data-theme="light"] {
  --bg: #F4F4F4;
  --bg2: #FFFFFF;
  --bg3: #EBEBEB;
  --card: #FFFFFF;
  --border: #DEDEDE;
  --text: #111111;
  --text2: #555555;
  --text3: #999;
  --shadow: 0 4px 24px rgba(0,0,0,0.1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;font-size:16px}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;line-height:1.6;transition:background .3s,color .3s;overflow-x:hidden}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--red);border-radius:3px}

/* ── COOKIE BANNER ── */
#cookie-banner{position:fixed;bottom:0;left:0;right:0;background:#111;border-top:2px solid var(--red);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;z-index:9999;flex-wrap:wrap}
#cookie-banner p{font-size:.85rem;color:#ccc;flex:1;min-width:200px}
#cookie-banner a{color:var(--yellow);text-decoration:underline}
#cookie-banner button{background:var(--red);color:#fff;border:none;padding:9px 22px;border-radius:var(--radius);cursor:pointer;font-weight:600;font-size:.85rem;white-space:nowrap}
#cookie-banner.hidden{display:none}

/* ── TOP BAR ── */
.topbar{background:var(--red);padding:6px 0;overflow:hidden}
.topbar-inner{display:flex;align-items:center;gap:0;white-space:nowrap;animation:ticker 40s linear infinite}
.topbar span{color:#fff;font-size:.78rem;font-weight:600;letter-spacing:.04em;padding:0 32px;border-right:1px solid rgba(255,255,255,.3)}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

/* ── HEADER ── */
header{background:var(--bg2);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:1000}
.header-inner{max-width:1280px;margin:0 auto;padding:0 24px;display:flex;align-items:center;gap:20px;height:64px}
.logo{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:var(--white);letter-spacing:.05em;text-decoration:none;flex-shrink:0;display:flex;align-items:center;gap:2px}
.logo span{color:var(--red)}
.logo sup{font-size:.7rem;color:var(--yellow);vertical-align:super;font-family:'DM Sans',sans-serif;font-weight:700;margin-left:2px}
nav{display:flex;align-items:center;gap:2px;flex:1;justify-content:center}
nav a{color:var(--text2);text-decoration:none;font-size:.88rem;font-weight:500;padding:8px 14px;border-radius:var(--radius);transition:all .2s;position:relative}
nav a:hover,nav a.active{color:var(--text);background:var(--bg3)}
nav a.active::after{content:'';position:absolute;bottom:4px;left:50%;transform:translateX(-50%);width:16px;height:2px;background:var(--red);border-radius:2px}
.header-actions{display:flex;align-items:center;gap:10px;flex-shrink:0}
.search-box{display:flex;align-items:center;background:var(--bg3);border:1px solid var(--border);border-radius:24px;padding:6px 14px;gap:8px;transition:border-color .2s}
.search-box:focus-within{border-color:var(--red)}
.search-box input{background:none;border:none;outline:none;color:var(--text);font-size:.85rem;width:160px}
.search-box input::placeholder{color:var(--text3)}
.search-box svg{color:var(--text3);flex-shrink:0}
.btn-theme{background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:8px 10px;border-radius:var(--radius);cursor:pointer;font-size:.9rem;line-height:1;transition:all .2s}
.btn-theme:hover{border-color:var(--yellow);color:var(--yellow)}
.hamburger{display:none;background:none;border:none;color:var(--text);cursor:pointer;padding:6px}

/* ── MOBILE NAV ── */
.mobile-nav{display:none;position:fixed;top:64px;left:0;right:0;background:var(--bg2);border-bottom:2px solid var(--red);z-index:999;padding:16px 24px;flex-direction:column;gap:4px}
.mobile-nav.open{display:flex}
.mobile-nav a{color:var(--text);text-decoration:none;padding:10px 12px;border-radius:var(--radius);font-weight:500;transition:background .2s}
.mobile-nav a:hover{background:var(--bg3)}

/* ── MAIN LAYOUT ── */
main{max-width:1280px;margin:0 auto;padding:32px 24px}
.page{display:none}
.page.active{display:block}

/* ── HERO ── */
.hero{display:grid;grid-template-columns:1fr 380px;gap:24px;margin-bottom:48px}
.hero-main{position:relative;border-radius:10px;overflow:hidden;cursor:pointer;aspect-ratio:16/9}
.hero-main img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.hero-main:hover img{transform:scale(1.03)}
.hero-main .overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.92) 0%,rgba(0,0,0,.3) 50%,transparent 100%)}
.hero-main .hero-content{position:absolute;bottom:0;left:0;right:0;padding:28px}
.hero-main .category-tag{display:inline-block;background:var(--red);color:#fff;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 10px;border-radius:3px;margin-bottom:12px}
.hero-main h1{font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:#fff;line-height:1.1;letter-spacing:.02em;margin-bottom:10px}
.hero-main .hero-meta{display:flex;align-items:center;gap:12px;color:rgba(255,255,255,.65);font-size:.8rem}
.hero-main .hero-meta span{display:flex;align-items:center;gap:4px}
.hero-side{display:flex;flex-direction:column;gap:14px}
.side-card{display:grid;grid-template-columns:100px 1fr;gap:12px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:12px;cursor:pointer;transition:border-color .2s,transform .2s}
.side-card:hover{border-color:var(--red);transform:translateX(3px)}
.side-card img{width:100px;height:70px;object-fit:cover;border-radius:4px}
.side-card .cat{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--red);margin-bottom:4px}
.side-card h3{font-family:'Source Serif 4',serif;font-size:.9rem;color:var(--text);line-height:1.3}
.side-card .meta{font-size:.75rem;color:var(--text3);margin-top:4px}

/* ── SECTION TITLE ── */
.section-title{display:flex;align-items:center;gap:14px;margin-bottom:24px}
.section-title h2{font-family:'Bebas Neue',sans-serif;font-size:1.7rem;letter-spacing:.05em;color:var(--text)}
.section-title .line{flex:1;height:2px;background:linear-gradient(to right,var(--red),transparent)}
.section-title .view-all{font-size:.8rem;color:var(--red);text-decoration:none;font-weight:600;white-space:nowrap}
.section-title .view-all:hover{text-decoration:underline}

/* ── NEWS GRID ── */
.news-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-bottom:48px}
.news-card{background:var(--card);border:1px solid var(--border);border-radius:8px;overflow:hidden;cursor:pointer;transition:border-color .25s,transform .25s,box-shadow .25s}
.news-card:hover{border-color:var(--red);transform:translateY(-4px);box-shadow:var(--shadow)}
.news-card img{width:100%;aspect-ratio:16/9;object-fit:cover;transition:transform .3s}
.news-card:hover img{transform:scale(1.04)}
.news-card-body{padding:16px}
.news-card-body .cat{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;display:inline-block;padding:3px 8px;border-radius:3px}
.cat-deportes{color:#fff;background:#E63946}
.cat-tecnologia{color:#fff;background:#3A86FF}
.cat-actualidad{color:#fff;background:#06D6A0}
.cat-opinion{color:#fff;background:#FF9F1C}
.news-card-body h3{font-family:'Source Serif 4',serif;font-size:1rem;font-weight:600;line-height:1.4;color:var(--text);margin-bottom:8px}
.news-card-body p{font-size:.83rem;color:var(--text2);line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.news-card-footer{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-top:1px solid var(--border)}
.news-card-footer .author{display:flex;align-items:center;gap:7px;font-size:.78rem;color:var(--text2)}
.author-avatar{width:24px;height:24px;border-radius:50%;background:var(--red);display:flex;align-items:center;justify-content:center;font-size:.6rem;font-weight:700;color:#fff;flex-shrink:0}
.news-card-footer .date{font-size:.75rem;color:var(--text3)}

/* ── LAYOUT CON SIDEBAR ── */
.content-sidebar{display:grid;grid-template-columns:1fr 320px;gap:32px}
.sidebar-widget{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:20px;margin-bottom:22px}
.sidebar-widget h4{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:.05em;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--red);display:flex;align-items:center;gap:8px}
.trending-item{display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);cursor:pointer}
.trending-item:last-child{border-bottom:none}
.trending-num{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--red);line-height:1;min-width:28px;opacity:.7}
.trending-item h5{font-size:.85rem;font-weight:500;color:var(--text);line-height:1.4;transition:color .2s}
.trending-item:hover h5{color:var(--red)}
.trending-item .tmeta{font-size:.72rem;color:var(--text3);margin-top:3px}

/* NEWSLETTER */
.newsletter-widget{background:linear-gradient(135deg,var(--red),#c1121f);border:none;text-align:center}
.newsletter-widget h4{color:#fff;border-bottom-color:rgba(255,255,255,.3);font-size:1.2rem}
.newsletter-widget p{font-size:.82rem;color:rgba(255,255,255,.85);margin-bottom:14px;line-height:1.5}
.newsletter-form{display:flex;flex-direction:column;gap:8px}
.newsletter-form input{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;padding:10px 14px;border-radius:var(--radius);font-size:.85rem;outline:none}
.newsletter-form input::placeholder{color:rgba(255,255,255,.6)}
.newsletter-form input:focus{border-color:#fff}
.newsletter-form button{background:#fff;color:var(--red);font-weight:700;border:none;padding:10px;border-radius:var(--radius);cursor:pointer;font-size:.88rem;transition:opacity .2s}
.newsletter-form button:hover{opacity:.9}

/* AD SPACE */
.ad-space{background:var(--bg3);border:2px dashed var(--border);border-radius:var(--radius);display:flex;align-items:center;justify-content:center;font-size:.75rem;color:var(--text3);text-transform:uppercase;letter-spacing:.08em;font-weight:600;min-height:100px;margin-bottom:22px}
.ad-banner{min-height:90px;border-radius:var(--radius);margin-bottom:32px}

/* ── CATEGORÍA FILTROS ── */
.cat-filters{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:28px}
.cat-btn{background:var(--bg3);border:1px solid var(--border);color:var(--text2);padding:7px 18px;border-radius:24px;cursor:pointer;font-size:.83rem;font-weight:500;transition:all .2s}
.cat-btn:hover,.cat-btn.active{background:var(--red);border-color:var(--red);color:#fff}

/* ── ARTICLE VIEW ── */
#page-article{animation:fadeIn .3s ease}
.article-header{max-width:780px;margin:0 auto 32px}
.article-header .breadcrumb{font-size:.78rem;color:var(--text3);margin-bottom:16px}
.article-header .breadcrumb a{color:var(--red);text-decoration:none}
.article-header .breadcrumb a:hover{text-decoration:underline}
.article-header h1{font-family:'Bebas Neue',sans-serif;font-size:clamp(2rem,5vw,3.2rem);letter-spacing:.03em;line-height:1.05;color:var(--text);margin-bottom:16px}
.article-header .article-meta{display:flex;align-items:center;gap:16px;flex-wrap:wrap;font-size:.82rem;color:var(--text2);padding-bottom:16px;border-bottom:1px solid var(--border)}
.article-hero-img{width:100%;max-width:900px;margin:0 auto 32px;display:block;border-radius:8px;aspect-ratio:16/9;object-fit:cover}
.article-body{max-width:720px;margin:0 auto;font-family:'Source Serif 4',serif;font-size:1.05rem;line-height:1.85;color:var(--text)}
.article-body p{margin-bottom:1.4em}
.article-body h2{font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:.04em;margin:2em 0 .6em;color:var(--text)}
.article-body blockquote{border-left:4px solid var(--red);padding:16px 20px;margin:2em 0;background:var(--bg3);border-radius:0 var(--radius) var(--radius) 0;font-style:italic;color:var(--text2)}
.share-bar{max-width:720px;margin:32px auto;display:flex;align-items:center;gap:12px;padding:16px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.share-bar span{font-size:.83rem;color:var(--text2);font-weight:600;margin-right:4px}
.share-btn{display:flex;align-items:center;gap:6px;padding:8px 16px;border-radius:var(--radius);border:none;cursor:pointer;font-size:.8rem;font-weight:600;transition:opacity .2s}
.share-btn:hover{opacity:.85}
.share-btn.fb{background:#1877F2;color:#fff}
.share-btn.tw{background:#000;color:#fff}
.share-btn.wa{background:#25D366;color:#fff}
.back-btn{display:inline-flex;align-items:center;gap:8px;color:var(--red);text-decoration:none;font-size:.85rem;font-weight:600;margin-bottom:24px;cursor:pointer;background:none;border:none;padding:0}
.back-btn:hover{text-decoration:underline}

/* ── CONTACTO / ABOUT ── */
.static-page{max-width:760px;margin:0 auto}
.static-page h1{font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:.05em;margin-bottom:8px}
.static-page .subtitle{color:var(--text2);margin-bottom:32px;font-size:1rem}
.static-page h2{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;letter-spacing:.04em;margin:32px 0 12px;color:var(--red)}
.static-page p{font-family:'Source Serif 4',serif;font-size:1rem;line-height:1.8;color:var(--text2);margin-bottom:16px}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:24px}
.contact-info-item{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:20px;display:flex;align-items:flex-start;gap:14px}
.contact-info-item .icon{font-size:1.4rem;flex-shrink:0}
.contact-info-item strong{display:block;font-size:.85rem;color:var(--text);margin-bottom:4px}
.contact-info-item span{font-size:.83rem;color:var(--text2)}
.form-group{margin-bottom:18px}
.form-group label{display:block;font-size:.83rem;font-weight:600;margin-bottom:6px;color:var(--text)}
.form-group input,.form-group textarea,.form-group select{width:100%;background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:11px 14px;border-radius:var(--radius);font-size:.9rem;outline:none;transition:border-color .2s;font-family:'DM Sans',sans-serif}
.form-group input:focus,.form-group textarea:focus,.form-group select:focus{border-color:var(--red)}
.form-group textarea{height:120px;resize:vertical}
.btn-primary{background:var(--red);color:#fff;border:none;padding:12px 28px;border-radius:var(--radius);font-weight:700;font-size:.9rem;cursor:pointer;transition:opacity .2s,transform .15s}
.btn-primary:hover{opacity:.88;transform:translateY(-1px)}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}

/* PANEL ADMIN */
#admin-panel{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:9000;display:flex;align-items:center;justify-content:center;padding:16px;opacity:0;pointer-events:none;transition:opacity .3s}
#admin-panel.open{opacity:1;pointer-events:all}
.admin-box{background:var(--bg2);border:1px solid var(--border);border-radius:12px;width:100%;max-width:640px;max-height:90vh;overflow-y:auto}
.admin-header{display:flex;align-items:center;justify-content:space-between;padding:20px 24px;border-bottom:1px solid var(--border)}
.admin-header h3{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;letter-spacing:.05em}
.admin-header button{background:none;border:none;color:var(--text2);cursor:pointer;font-size:1.3rem;line-height:1}
.admin-body{padding:24px}
.admin-body .form-group label{font-size:.82rem}
.admin-articles-list{margin-top:24px;border-top:1px solid var(--border);padding-top:16px}
.admin-articles-list h4{font-size:.85rem;font-weight:700;margin-bottom:12px;color:var(--text2);text-transform:uppercase;letter-spacing:.06em}
.admin-article-item{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border);gap:10px}
.admin-article-item span{font-size:.83rem;color:var(--text);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.admin-article-item .del-btn{background:none;border:1px solid #c1121f;color:#E63946;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:.75rem;flex-shrink:0}
.admin-article-item .del-btn:hover{background:#E63946;color:#fff}
.btn-admin-open{position:fixed;bottom:24px;right:24px;background:var(--red);color:#fff;border:none;border-radius:50px;padding:12px 20px;font-weight:700;font-size:.85rem;cursor:pointer;z-index:2000;box-shadow:0 4px 20px rgba(230,57,70,.5);display:flex;align-items:center;gap:8px;transition:transform .2s}
.btn-admin-open:hover{transform:scale(1.05)}

/* ── PRIVACY PAGE ── */
.privacy-content{max-width:760px;margin:0 auto;font-family:'Source Serif 4',serif;font-size:.98rem;line-height:1.8;color:var(--text2)}
.privacy-content h1{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:var(--text);margin-bottom:8px}
.privacy-content h2{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:var(--text);margin:28px 0 10px;letter-spacing:.04em}
.privacy-content p{margin-bottom:14px}
.privacy-content ul{padding-left:20px;margin-bottom:14px}
.privacy-content ul li{margin-bottom:6px}

/* ── FOOTER ── */
footer{background:var(--bg2);border-top:1px solid var(--border);margin-top:60px}
.footer-main{max-width:1280px;margin:0 auto;padding:48px 24px 32px;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px}
.footer-brand .logo{font-size:1.8rem;display:inline-flex}
.footer-brand p{font-size:.85rem;color:var(--text2);margin-top:12px;line-height:1.6;max-width:260px}
.footer-social{display:flex;gap:10px;margin-top:16px}
.social-btn{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.85rem;font-weight:700;color:#fff;text-decoration:none;transition:transform .2s}
.social-btn:hover{transform:scale(1.1)}
.social-btn.fb{background:#1877F2}
.social-btn.tw{background:#000}
.social-btn.ig{background:linear-gradient(45deg,#fd1d1d,#e1306c,#833ab4)}
.social-btn.yt{background:#FF0000}
.footer-col h5{font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:.08em;color:var(--text);margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid var(--red)}
.footer-col ul{list-style:none}
.footer-col ul li{margin-bottom:8px}
.footer-col ul li a{color:var(--text2);text-decoration:none;font-size:.85rem;transition:color .2s}
.footer-col ul li a:hover{color:var(--red)}
.footer-bottom{border-top:1px solid var(--border);padding:16px 24px;max-width:1280px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.footer-bottom p{font-size:.78rem;color:var(--text3)}
.footer-bottom a{color:var(--text3);text-decoration:none;font-size:.78rem}
.footer-bottom a:hover{color:var(--red)}

/* ── SEARCH RESULTS ── */
.search-results{background:var(--bg2);border:1px solid var(--border);position:absolute;top:calc(100% + 6px);right:0;width:340px;border-radius:8px;box-shadow:var(--shadow);z-index:2000;max-height:360px;overflow-y:auto;display:none}
.search-results.show{display:block}
.search-result-item{padding:12px 16px;border-bottom:1px solid var(--border);cursor:pointer;transition:background .15s}
.search-result-item:last-child{border-bottom:none}
.search-resul
