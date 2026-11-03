// Vypíše text stránky portu.cz (nebo magazin.portu.cz) tak, jak ji vidí návštěvník.
// Web Portu se vykresluje JavaScriptem, proto se načítá v Chromiu přes Playwright.
// Rozbalí i sbalené odpovědi (FAQ, akordeony), aby byl v textu celý obsah.
// Použití: node nastroje/portu-stranka.js https://www.portu.cz/o-nas/kolik-to-stoji
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

(async () => {
  const url = process.argv[2];
  if (!url || !/^https:\/\/(www\.|magazin\.)?portu\.cz\//.test(url)) {
    console.error('Použití: node nastroje/portu-stranka.js https://www.portu.cz/...');
    process.exit(2);
  }
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  try {
    const p = await b.newPage();
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(() => document.querySelectorAll('details').forEach((d) => { d.open = true; }));
    let t;
    try { t = await p.innerText('main'); } catch (e) { t = await p.innerText('body'); }
    console.log(`ZDROJ: ${url}\nNAČTENO: ${new Date().toISOString().slice(0, 10)}\n`);
    // vyhodit opakovanou patičku (kontakty, „Účet založíte za 10 minut“, počty klientů)
    t = t.replace(/Zeptejte se\nOnline chat[\s\S]*?Začít investovat\n?/g, '');
    console.log(t.replace(/\n{3,}/g, '\n\n'));

    // Akordeony (FAQ) se otevírají po jednom: každou otázku rozklikni a vypiš její odpověď.
    const triggers = await p.$$('main .accordion__trigger');
    if (triggers.length) console.log('\n===== OTÁZKY A ODPOVĚDI (rozbalené akordeony) =====');
    for (const tr of triggers) {
      const q = (await tr.innerText().catch(() => '')).trim();
      let a = '';
      for (let pokus = 0; pokus < 3 && !a; pokus++) {
        try {
          await tr.scrollIntoViewIfNeeded({ timeout: 2000 });
          if ((await tr.getAttribute('aria-expanded')) !== 'true') await tr.click({ timeout: 3000, force: pokus > 0 });
          await p.waitForTimeout(400 + 400 * pokus);
          const id = await tr.getAttribute('aria-controls');
          if (id) a = await p.$eval(`[id="${id}"]`, (el) => el.innerText.trim()).catch(() => '');
        } catch (e) { /* zkusit znovu */ }
      }
      console.log(`\nOTÁZKA: ${q}\nODPOVĚĎ: ${a || '(odpověď se nepodařilo načíst – otevři stránku a ověř ručně)'}`);
    }
  } finally {
    await b.close();
  }
})();
