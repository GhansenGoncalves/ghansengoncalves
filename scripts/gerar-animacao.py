"""Gera uma animação ilustrativa do script PTE com visual de editor e terminal.

Não executa Cypress. O comando de terminal e a sequência são uma representação.
O trecho de código foi adaptado do script privado; os valores são fictícios.
Requer Python e Pillow: python scripts/gerar-animacao.py
"""

from functools import lru_cache
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1200, 790
NAVY, BLUE, INK = '#123650', '#007acc', '#243746'
MUTED, LINE, PAPER = '#617585', '#dce3e8', '#f6f9fb'
FONT_DIR = Path('C:/Windows/Fonts')


@lru_cache(maxsize=32)
def font(size, bold=False, mono=False):
    windows = 'consola.ttf' if mono else ('segoeuib.ttf' if bold else 'segoeui.ttf')
    linux = 'DejaVuSansMono.ttf' if mono else ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    for path in [FONT_DIR / windows, Path('/usr/share/fonts/truetype/dejavu') / linux]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise FileNotFoundError('Instale Segoe UI ou DejaVu Sans.')


# Apenas este pequeno trecho adaptado é público. Nenhuma URL ou credencial é usada.
CODE = [
    "// PNUD: trecho adaptado do cadastro PTE",
    "// Valores de exemplo; sem execução nesta animação",
    "",
    "cy.contains('span.content', 'Requerimentos')",
    "  .click();",
    "",
    "cy.contains('h2',",
    "  'Cadastrar Solicitação de Registro de ' +",
    "  'Produto Técnico Equivalente'",
    ").should('be.visible');",
    "",
    "cy.get('#marcaComercial')",
    "  .should('be.visible')",
    "  .type('Produto exemplo');",
    "",
    "cy.get('#nomeQuimico')",
    "  .should('be.visible')",
    "  .type('Composto exemplo');",
]

# Código existente, valores substituídos e quebras de linha para legibilidade.
STAGES = [
    ('Preparar o comando', None, 'O comando abaixo é ilustrativo e não será executado.'),
    ('Abrir Requerimentos', (3, 4), 'Navegação representada: Requerimentos.'),
    ('Conferir o formulário PTE', (6, 9), 'Verificação representada: título do formulário.'),
    ('Preencher marca comercial', (11, 13), 'Preenchimento representado: Produto exemplo.'),
    ('Preencher nome químico', (15, 17), 'Preenchimento representado: Composto exemplo.'),
    ('Revisar as verificações', (15, 16), 'Fim da prévia visual. Nenhum resultado de teste é emitido.'),
]
TOKEN = re.compile(r"('[^']*'|\b(?:cy|contains|click|should|get|type)\b)")


def make_frame(stage, tick):
    im = Image.new('RGB', (WIDTH, HEIGHT), PAPER)
    d = ImageDraw.Draw(im)

    def text(x, y, content, size=18, fill=INK, bold=False, mono=False):
        d.text((x, y), content, fill=fill, font=font(size, bold, mono))

    # Identidade do portfólio fora do editor.
    text(24, 13, 'PNUD / Automação com Cypress', 25, NAVY, True)
    text(900, 18, 'Demonstração animada', 19, MUTED)

    # Janela inspirada no Visual Studio Code, tema claro e controles Windows.
    d.rounded_rectangle((16, 59, 1184, 724), radius=8, fill='white', outline=LINE)
    d.rounded_rectangle((17, 60, 1183, 99), radius=8, fill='#edf1f5')
    d.rectangle((17, 83, 1183, 99), fill='#edf1f5')
    d.polygon([(33, 77), (46, 68), (46, 90), (33, 81), (26, 86), (26, 73)], fill=BLUE)
    text(62, 69, 'Arquivo   Editar   Seleção   Exibir   Executar   Terminal', 15)
    text(620, 69, 'PNUD — Visual Studio Code', 15, MUTED)
    text(1064, 67, '—    □    ×', 19, MUTED)

    # Barra de atividades e explorador, sem caminhos internos.
    d.rectangle((17, 100, 64, 698), fill='#e8eef3')
    d.rectangle((17, 111, 20, 145), fill=BLUE)
    d.rectangle((30, 117, 48, 138), outline=NAVY, width=2)
    d.line((35, 112, 54, 112, 54, 133), fill=NAVY, width=2)
    d.ellipse((31, 174, 47, 190), outline=MUTED, width=2)
    d.line((45, 188, 53, 198), fill=MUTED, width=2)
    d.ellipse((31, 226, 38, 233), outline=MUTED, width=2)
    d.ellipse((44, 250, 51, 257), outline=MUTED, width=2)
    d.line((35, 232, 35, 249, 46, 249), fill=MUTED, width=2)
    d.polygon([(34, 290), (34, 311), (49, 300)], outline=MUTED, width=2)
    d.rectangle((65, 100, 267, 698), fill='#f3f5f7')
    text(82, 111, 'Explorador', 16, MUTED)
    for x, y in [(82, 160), (97, 197), (115, 229)]:
        d.polygon([(x, y), (x + 10, y), (x + 5, y + 6)], fill=MUTED)
    text(101, 150, 'PNUD · exemplo', 17, NAVY, True)
    text(116, 187, 'cypress', 17)
    text(134, 219, 'e2e', 17)
    d.rectangle((65, 250, 266, 282), fill='#dce9f2')
    text(133, 256, 'JS', 15, '#956800', True)
    text(164, 255, 'fluxo_pte…', 16)
    text(96, 304, 'cypress.config.js', 16, MUTED)
    text(96, 337, 'package.json', 16, MUTED)

    # Editor: trecho real adaptado, destaque percorrendo a sequência.
    d.rectangle((268, 100, 1183, 139), fill='#f3f5f7')
    d.rectangle((268, 100, 674, 139), fill='white')
    d.rectangle((268, 100, 674, 102), fill=BLUE)
    text(286, 110, 'JS', 15, '#956800', True)
    text(321, 109, 'fluxo_cadastro_pte_homol.cy.js', 17)
    text(645, 107, '×', 20, MUTED)
    text(291, 149, 'cypress  ›  e2e  ›  Trecho adaptado para o portfólio', 15, MUTED)
    d.line((267, 100, 267, 698), fill=LINE)
    highlight = STAGES[stage][1]
    for idx, line in enumerate(CODE):
        y = 177 + idx * 23
        if highlight and highlight[0] <= idx <= highlight[1]:
            d.rectangle((269, y - 1, 1182, y + 22), fill='#e9f2fa')
            d.rectangle((269, y - 1, 272, y + 22), fill=BLUE)
        text(292, y, str(idx + 1).rjust(2), 18, '#8b969f', mono=True)
        if line.startswith('//'):
            text(338, y, line, 18, '#487d3d', mono=True)
        else:
            x = 338
            for part in TOKEN.split(line):
                color = '#a31515' if part.startswith("'") else '#001080' if part == 'cy' else '#795e26' if part in ['contains', 'click', 'should', 'get', 'type'] else '#243746'
                text(x, y, part, 18, color, mono=True)
                x += font(18, mono=True).getlength(part)

    # Terminal: digitação e etapas identificadas como prévia, sem resultados fictícios.
    d.rectangle((268, 605, 1183, 698), fill='#fafbfc')
    d.line((268, 605, 1183, 605), fill=LINE)
    text(288, 614, 'Problèmes     Sortie     Console de débogage', 13, MUTED)
    text(638, 613, 'Terminal', 14, INK, True)
    d.line((638, 634, 697, 634), fill=BLUE, width=2)
    text(958, 614, 'Prévia ilustrativa', 14, BLUE)
    prompt = 'PS C:\\portfolio\\pnud> '
    command = 'npx cypress run'
    count = min(len(command), int(tick / 2)) if stage == 0 else len(command)
    text(289, 645, prompt + command[:count], 17, NAVY, mono=True)
    if stage == 0 and tick % 10 < 5:
        px = 289 + font(17, mono=True).getlength(prompt + command[:count])
        d.rectangle((px + 1, 646, px + 3, 665), fill=BLUE)
    if stage > 0:
        text(289, 674, STAGES[stage][2], 15, MUTED, mono=True)

    d.rectangle((17, 699, 1183, 723), fill=BLUE)
    text(32, 701, 'Demonstração', 14, 'white')
    text(756, 701, 'UTF-8     JavaScript     Cypress', 14, 'white')
    text(24, 743, 'Script adaptado • dados fictícios • terminal ilustrativo • sem execução real', 20, MUTED)
    return im


def main():
    frames = [make_frame(stage, tick) for stage in range(6) for tick in range(30)]
    # Paleta comum inclui todos os estados, evitando alteração de cor no GIF.
    atlas = Image.new('RGB', (WIDTH, HEIGHT * 6))
    for stage in range(6):
        atlas.paste(frames[stage * 30 + 15], (0, stage * HEIGHT))
    palette = atlas.quantize(colors=192)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    out = ROOT / 'assets' / 'pnud-fluxo-cypress.gif'
    indexed[0].save(out, save_all=True, append_images=indexed[1:], duration=100,
                    loop=0, optimize=False, disposal=1)
    frames[3 * 30 + 15].save(ROOT / 'assets' / 'pnud-fluxo-cypress.png')
    print(f'Animação gerada: {len(frames)} quadros, 18 s, {out.stat().st_size:,} bytes.')


if __name__ == '__main__':
    main()
