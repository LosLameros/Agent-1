// Načte z úvodní stránky portu.cz aktuální objem zainvestovaných peněz („76 miliard Kč zainvestováno“).
// Použití: node nastroje/portu-aum.js   -> vypíše jen číslo v miliardách Kč, např. 76
// Stránka se vykresluje JavaScriptem, proto se načítá v Chromiu přes Playwright.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  try {
    const p = await b.newPage();
    await p.goto('https://www.portu.cz/', { waitUntil: 'networkidle', timeout: 60000 });
    const t = await p.innerText('body');
    const m = t.match(/(\d+(?:[.,]\d+)?)\s*miliard(?:y|a)?\s*Kč\s*\n?\s*zainvestováno/i)
      || t.match(/zainvestováno\s*\n?\s*(\d+(?:[.,]\d+)?)\s*miliard/i);
    if (!m) { console.error('CHYBA: na portu.cz nenalezen údaj „… miliard Kč zainvestováno“'); process.exit(1); }
    console.log(m[1]);
  } finally { await b.close(); }
})();
