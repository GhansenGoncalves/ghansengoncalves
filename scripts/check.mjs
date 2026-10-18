import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, sep } from 'node:path';

const root = process.argv[2] ? resolve(process.argv[2]) : resolve(dirname(fileURLToPath(import.meta.url)), '..');
const readme = readFileSync(resolve(root, 'README.md'), 'utf8');
const localLinks = [...readme.matchAll(/\]\(([^)]+)\)/g)]
  .map((match) => match[1])
  .filter((link) => !/^(?:https?:|mailto:|#)/.test(link));
for (const link of localLinks) {
  const target = resolve(root, link);
  assert(target.startsWith(root + sep));
  assert(existsSync(target), `Arquivo vinculado não encontrado: ${link}`);
}
assert.equal((readme.match(/<details>/g) ?? []).length, (readme.match(/<\/details>/g) ?? []).length);
assert(readme.includes('terminal é ilustrativo'));
assert(readme.includes('Capturas reais da aplicação local'));
assert(readme.indexOf('### Projeto em destaque: Liga Enge') < readme.indexOf('### Automação com Cypress: PNUD'));

const svg = readFileSync(resolve(root, 'assets/apresentacao.svg'), 'utf8');
assert(svg.includes('viewBox="0 0 1000 230"'));
assert(!/<script\b|\bonload\s*=|<foreignObject\b/i.test(svg));
assert(svg.includes('<title') && svg.includes('<desc'));

function checkMedia(name, width, height, expectedDuration) {
  const gif = readFileSync(resolve(root, `assets/${name}.gif`));
  assert.equal(gif.toString('ascii', 0, 6), 'GIF89a');
  assert.equal(gif.readUInt16LE(6), width);
  assert.equal(gif.readUInt16LE(8), height);
  let offset = 13 + ((gif[10] & 0x80) ? 3 * 2 ** ((gif[10] & 7) + 1) : 0);
  let frames = 0;
  let duration = 0;
  function subBlocks() {
    while (true) {
      assert(offset < gif.length, 'GIF truncado');
      const size = gif[offset++];
      if (size === 0) break;
      offset += size;
      assert(offset <= gif.length, 'Bloco GIF inválido');
    }
  }
  let trailer = false;
  while (offset < gif.length) {
    const marker = gif[offset++];
    if (marker === 0x3b) { trailer = true; break; }
    if (marker === 0x21) {
      const label = gif[offset++];
      if (label === 0xf9) duration += gif.readUInt16LE(offset + 2) * 10;
      subBlocks();
    } else if (marker === 0x2c) {
      const packed = gif[offset + 8];
      offset += 9;
      if (packed & 0x80) offset += 3 * 2 ** ((packed & 7) + 1);
      offset++;
      subBlocks();
      frames++;
    } else {
      throw new Error(`Bloco GIF inesperado: ${marker}`);
    }
  }
  assert(trailer && frames > 10, 'A animação precisa conter quadros completos');
  assert.equal(duration, expectedDuration, 'Duração inesperada na animação');
  assert(gif.length < 2_000_000, 'O GIF deve permanecer leve para o perfil');
  const png = readFileSync(resolve(root, `assets/${name}.png`));
  assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
  assert.equal(png.readUInt32BE(16), width);
  assert.equal(png.readUInt32BE(20), height);
  console.log(`${name}: ${frames} quadros, ${duration / 1000}s, ${gif.length} bytes.`);
}

checkMedia('pnud-fluxo-cypress', 1200, 790, 18000);
const liga = JSON.parse(readFileSync(resolve(root, 'assets/liga-enge-demo.json'), 'utf8'));
assert.equal(liga.branch, 'develop');
assert.match(liga.commit_aplicacao, /^[a-f0-9]{40}$/);
assert.equal(liga.cenas.length, 5);
assert.equal(liga.duracao_ms, 20000);
checkMedia('liga-enge-demo', liga.largura, liga.altura, liga.duracao_ms);

for (const name of ['README.md', 'assets/apresentacao.svg', 'assets/liga-enge-demo.json', 'scripts/gerar-animacao.py', 'scripts/montar-demo-liga.py']) {
  const source = readFileSync(resolve(root, name), 'utf8');
  assert(!/alm\.engesoftware|homolog\.agricultura|\b(?:ghp_|github_pat_)/i.test(source),
    `Referência interna ou credencial em ${name}`);
}
console.log(`README e ${localLinks.length} vínculos locais conferidos.`);
