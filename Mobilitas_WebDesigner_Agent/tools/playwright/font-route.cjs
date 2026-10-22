// Montserrat in locale nei test visivi: risponde nel browser al posto di Google Fonts.
//   - fonts.googleapis.com/css2?family=Montserrat...  -> montserrat-local.css
//   - fonts.gstatic.com/s/montserrat/local/<file>     -> file woff2 del pacchetto @fontsource-variable/montserrat (OFL-1.1)
// Nessuna richiesta lascia il browser; ogni altro indirizzo Google resta bloccato dalla guardia di rete.
// Con WEBDESIGNER_LOCAL_FONTS=off non fa nulla (controllo con i font di ripiego).
const fs = require('fs');
const path = require('path');

const cssFile = path.join(__dirname, 'montserrat-local.css');
const filesDir = path.join(__dirname, 'node_modules/@fontsource-variable/montserrat/files');
const cors = { 'access-control-allow-origin': '*', 'x-webdesigner-font': 'local' };

exports.default = async ({ page }) => {
  if (process.env.WEBDESIGNER_LOCAL_FONTS === 'off') return;
  await page.route(
    url => url.hostname === 'fonts.googleapis.com' && url.pathname === '/css2' && /(^|&)family=Montserrat(:|&|$)/.test(url.search.slice(1)),
    route => route.fulfill({ status: 200, contentType: 'text/css; charset=utf-8', headers: cors, body: fs.readFileSync(cssFile, 'utf8') }));
  await page.route(
    url => url.hostname === 'fonts.gstatic.com' && url.pathname.startsWith('/s/montserrat/local/'),
    route => {
      const name = path.basename(new URL(route.request().url()).pathname);
      const file = path.join(filesDir, name);
      if (!/^montserrat-[a-z-]+-wght-normal\.woff2$/.test(name) || !fs.existsSync(file)) return route.abort('blockedbyclient');
      return route.fulfill({ status: 200, contentType: 'font/woff2', headers: cors, body: fs.readFileSync(file) });
    });
};
