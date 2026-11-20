// Doksanland render service.
// Small HTTP wrapper around the house template so n8n (or anything else) can turn
// a visual spec into a finished PNG without knowing about Playwright.
//
//   POST /render   body: a visuals.json object (id, format, kind, bg, title, ...)
//                  returns: image/png
//   POST /render/batch  body: {"visuals":[ ... ]}  returns: {"files":[{id,url}]}
//   GET  /health
//
// Images are also written to /data so other containers and the publisher can read them.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATE = process.env.TEMPLATE || path.join(ROOT, 'templates', 'card.html');
const OUT = process.env.OUT_DIR || '/data';
const PORT = Number(process.env.PORT || 4000);

fs.mkdirSync(OUT, { recursive: true });

let browser;
const getBrowser = async () => {
  if (!browser || !browser.isConnected()) browser = await chromium.launch({ args: ['--no-sandbox'], ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  return browser;
};

const SIZES = { post: { width: 1080, height: 1350 }, story: { width: 1080, height: 1920 } };

async function render(card) {
  if (!card || !card.id) throw new Error('visual needs an id');
  const size = SIZES[card.format === 'story' ? 'story' : 'post'];
  const page = await (await getBrowser()).newPage({ viewport: size, deviceScaleFactor: 1 });
  try {
    await page.addInitScript((c) => { window.CARD = c; }, card);
    await page.goto('file://' + TEMPLATE, { waitUntil: 'load' });
    await page.waitForSelector('body[data-ready="1"]', { timeout: 20000 });
    const file = path.join(OUT, `${card.id}.png`);
    await page.locator('.card').screenshot({ path: file });
    return file;
  } finally {
    await page.close();
  }
}

const body = (req) => new Promise((resolve, reject) => {
  let s = '';
  req.on('data', (c) => { s += c; if (s.length > 5e6) req.destroy(); });
  req.on('end', () => { try { resolve(s ? JSON.parse(s) : {}); } catch (e) { reject(e); } });
  req.on('error', reject);
});

http.createServer(async (req, res) => {
  const send = (code, obj) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(obj)); };
  try {
    if (req.method === 'GET' && req.url === '/health') return send(200, { ok: true });

    if (req.method === 'GET' && req.url.startsWith('/file/')) {
      const f = path.join(OUT, path.basename(decodeURIComponent(req.url.slice(6))));
      if (!fs.existsSync(f)) return send(404, { error: 'not found' });
      res.writeHead(200, { 'content-type': 'image/png' });
      return fs.createReadStream(f).pipe(res);
    }

    if (req.method === 'POST' && req.url === '/render') {
      const file = await render(await body(req));
      res.writeHead(200, { 'content-type': 'image/png' });
      return fs.createReadStream(file).pipe(res);
    }

    if (req.method === 'POST' && req.url === '/render/batch') {
      const { visuals = [] } = await body(req);
      const files = [];
      for (const v of visuals) files.push({ id: v.id, file: await render(v), url: `/file/${v.id}.png` });
      return send(200, { files });
    }

    send(404, { error: 'POST /render, POST /render/batch, GET /file/<name>, GET /health' });
  } catch (e) {
    send(500, { error: String(e && e.message || e) });
  }
}).listen(PORT, () => console.log(`doksanland render service on :${PORT}`));
