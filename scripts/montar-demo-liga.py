"""Monta um tour em GIF a partir de capturas reais da Liga Enge.

Uso: python scripts/montar-demo-liga.py PASTA_DAS_CAPTURAS
Requer Pillow. As imagens de origem são capturadas no navegador; este script
apenas enquadra, redimensiona e acrescenta legendas fora da interface.
Não desenha telas do produto, não altera placares e não executa testes.
"""

from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1])
SCENES = [
    ('01-visao-geral.png', 'Visão geral', 'Uma plataforma para organizar a participação nos Happy Hours.'),
    ('03-chaveamento.png', 'Chaveamento', 'Campeonato fictício de Truco, com oito duplas e duas chaves.'),
    ('04-detalhes-partida.png', 'Detalhes da final', 'Participantes e origem dos classificados em uma final MD5.'),
    ('05-homologacao.png', 'Homologação', 'Exemplo pronto de um resultado que aguarda confirmação.'),
    ('06-regras.png', 'Regras de negócio', 'Critérios de participação, experiência e pontuação no próprio produto.'),
]


def font(size, bold=False):
    for path in [Path('C:/Windows/Fonts') / ('segoeuib.ttf' if bold else 'segoeui.ttf'),
                 Path('/usr/share/fonts/truetype/dejavu') /
                 ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise FileNotFoundError('Instale Segoe UI ou DejaVu Sans.')


def main():
    width = 1400
    source_images = [Image.open(SOURCE / file).convert('RGB') for file, _, _ in SCENES]
    assert len({image.size for image in source_images}) == 1, 'As capturas devem ter o mesmo tamanho.'
    screen_height = round(source_images[0].height * width / source_images[0].width)
    height = screen_height + 126
    shots = [im.resize((width, screen_height), Image.Resampling.LANCZOS) for im in source_images]
    frames = []
    for index, (shot, (_, title, caption)) in enumerate(zip(shots, SCENES)):
        for tick in range(16):
            canvas = Image.new('RGB', (width, height), '#f6f9fb')
            d = ImageDraw.Draw(canvas)
            d.text((22, 12), 'Liga Enge', font=font(24, True), fill='#123650')
            d.text((190, 15), title, font=font(20), fill='#526d80')
            d.text((971, 15), 'Capturas reais • dados de teste', font=font(20), fill='#526d80')
            canvas.paste(shot, (0, 54))
            d.text((22, height - 54), caption, font=font(22), fill='#123650')
            d.line((22, height - 12, width - 22, height - 12), fill='#dbe5ec', width=3)
            progress = (index + (tick + 1) / 16) / len(SCENES)
            d.line((22, height - 12, 22 + (width - 44) * progress, height - 12), fill='#194e70', width=3)
            frames.append(canvas)

    atlas = Image.new('RGB', (width, height * len(SCENES)))
    for index in range(len(SCENES)):
        atlas.paste(frames[index * 16], (0, index * height))
    palette = atlas.quantize(colors=256)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    gif_path = ROOT / 'assets/liga-enge-demo.gif'
    indexed[0].save(gif_path, save_all=True, append_images=indexed[1:],
                    duration=250, loop=0, optimize=False, disposal=1)
    frames[0].save(ROOT / 'assets/liga-enge-demo.png')
    metadata = {
        'projeto': 'Liga Enge',
        'origem': 'Capturas reais da aplicação local, com massas de teste',
        'branch': 'develop',
        'commit_aplicacao': '97c10300c435827c3fa53d0f60e490d020e0d461',
        'data_captura': '2026-10-18',
        'apresentacao': 'Cenários fictícios prontos; sem alteração de partidas',
        'largura': width,
        'altura': height,
        'duracao_ms': 20000,
        'cenas': [{'titulo': title, 'descricao': caption} for _, title, caption in SCENES],
    }
    (ROOT / 'assets/liga-enge-demo.json').write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Tour montado: {width}x{height}, 20 segundos, {gif_path.stat().st_size:,} bytes.')


if __name__ == '__main__':
    main()
