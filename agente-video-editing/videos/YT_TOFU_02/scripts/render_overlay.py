#!/usr/bin/env python3
"""Disegna il livello grafico e lo riversa in RGBA grezzo su stdout.

Perche non un browser: questo ffmpeg non ha ne libass ne drawtext, quindi il
testo va comunque rasterizzato fuori. Un compositore headless su 24.500 frame
sarebbe lento e dipenderebbe dalla rete (GSAP da CDN); qui il livello si genera
in memoria e va dritto nella pipe di ffmpeg, senza file intermedi.

Ogni banda di sottotitolo viene disegnata una volta per parola attiva e tenuta
in cache: da un frame all'altro cambia solo quale delle varianti si incolla.
"""
import json, sys, time
sys.path.insert(0, 'scripts')
from PIL import Image, ImageDraw, ImageFont
import mobilitas_style as S

PLAN = json.load(open('data/overlay.json'))
FPS = S.FPS
NFRAMES = int(round(PLAN['duration'] * FPS))

_fonts = {}


def sans(size, weight=900):
    k = ('s', size, weight)
    if k not in _fonts:
        f = ImageFont.truetype(S.FONT_SANS, size)
        f.set_variation_by_axes([weight])
        _fonts[k] = f
    return _fonts[k]


def mono(size):
    k = ('m', size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(S.FONT_MONO, size)
    return _fonts[k]


def tracked_width(font, text, track_px):
    return sum(font.getlength(c) for c in text) + track_px * max(0, len(text) - 1)


def draw_tracked(d, xy, text, font, fill, track_px):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += font.getlength(c) + track_px
    return x


def rounded(size, radius, fill):
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1],
                                         radius=radius, fill=fill)
    return im


# ---------------------------------------------------------------- sottotitoli
CAP_PAD_X, CAP_PAD_Y = 34, 20
_capcache = {}


def caption_sprite(gi, active):
    key = (gi, active)
    if key in _capcache:
        return _capcache[key]
    g = PLAN['captions'][gi]
    f = sans(S.SIZE['caption'], 900)
    track = S.TRACK['caption'] * S.SIZE['caption']
    space = f.getlength(' ') + track
    widths = [tracked_width(f, w['t'], track) for w in g['words']]
    total = sum(widths) + space * (len(widths) - 1)
    h = int(S.SIZE['caption'] * 1.30)
    im = Image.new('RGBA', (int(total) + CAP_PAD_X * 2, h + CAP_PAD_Y * 2 + 10), (0, 0, 0, 0))
    scrim = rounded(im.size, 20, S.NAVY_DEEP + (196,))
    im.alpha_composite(scrim)
    d = ImageDraw.Draw(im)
    x = CAP_PAD_X
    y = CAP_PAD_Y - int(S.SIZE['caption'] * 0.10)
    for i, w in enumerate(g['words']):
        col = S.MINT if i == active else S.PAPER
        draw_tracked(d, (x, y), w['t'], f, col + (255,), track)
        if i == active:
            d.rounded_rectangle([x, CAP_PAD_Y + h - 6, x + widths[i], CAP_PAD_Y + h - 1],
                                radius=3, fill=S.MINT + (255,))
        x += widths[i] + space
    if len(_capcache) > 40:
        _capcache.clear()
    _capcache[key] = im
    return im


# ---------------------------------------------------------------------- card
def card_sprite(c):
    w = S.CARD_BOX[2]
    pad = 34
    f_eye, f_val, f_unit, f_sub = mono(S.SIZE['eyebrow']), sans(S.SIZE['card_value'], 900), \
        sans(S.SIZE['card_unit'], 800), sans(S.SIZE['card_sub'], 600)
    track_e = S.TRACK['eyebrow'] * S.SIZE['eyebrow']
    sub_lines, cur = [], ''
    for word in c['sub'].split():
        t = (cur + ' ' + word).strip()
        if f_sub.getlength(t) > w - pad * 2 and cur:
            sub_lines.append(cur); cur = word
        else:
            cur = t
    if cur:
        sub_lines.append(cur)
    h = pad + S.SIZE['eyebrow'] + 16 + 6 + 26 + S.SIZE['card_value'] + 18 \
        + len(sub_lines) * int(S.SIZE['card_sub'] * 1.35) + pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 26, S.NAVY + (238,)))
    d = ImageDraw.Draw(im)
    y = pad
    draw_tracked(d, (pad, y), c['eyebrow'], f_eye, S.MINT + (255,), track_e)
    y += S.SIZE['eyebrow'] + 16
    d.rounded_rectangle([pad, y, pad + 84, y + 5], radius=2, fill=S.MINT + (255,))
    y += 26
    vw = f_val.getlength(c['value'])
    d.text((pad, y - int(S.SIZE['card_value'] * 0.16)), c['value'], font=f_val,
           fill=S.MINT + (255,))
    d.text((pad + vw + 12, y + S.SIZE['card_value'] - S.SIZE['card_unit'] - 14),
           c['unit'], font=f_unit, fill=S.PAPER + (255,))
    y += S.SIZE['card_value'] + 18
    for ln in sub_lines:
        d.text((pad, y), ln, font=f_sub, fill=S.MUTED + (255,))
        y += int(S.SIZE['card_sub'] * 1.35)
    return im


# ------------------------------------------------------------------- stacchi
def chapter_sprite(c):
    im = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (238,))
    d = ImageDraw.Draw(im)
    f_eye = mono(S.SIZE['eyebrow'] + 6)
    f_t = sans(S.SIZE['chapter'], 900)
    track_e = S.TRACK['eyebrow'] * (S.SIZE['eyebrow'] + 6)
    ew = tracked_width(f_eye, c['eyebrow'], track_e)
    y = S.H // 2 - 150
    draw_tracked(d, ((S.W - ew) / 2, y), c['eyebrow'], f_eye, S.MINT + (255,), track_e)
    y += S.SIZE['eyebrow'] + 30
    d.rounded_rectangle([S.W / 2 - 60, y, S.W / 2 + 60, y + 6], radius=3, fill=S.MINT + (255,))
    y += 42
    for i, ln in enumerate((c['l1'], c['l2'])):
        tw = tracked_width(f_t, ln, S.TRACK['chapter'] * S.SIZE['chapter'])
        draw_tracked(d, ((S.W - tw) / 2, y), ln, f_t,
                     (S.PAPER if i == 0 else S.MINT) + (255,),
                     S.TRACK['chapter'] * S.SIZE['chapter'])
        y += int(S.SIZE['chapter'] * 1.16)
    return im


def wrap_to(font, text, track, maxw):
    lines, cur = [], ''
    for word in text.split():
        t = (cur + ' ' + word).strip()
        if tracked_width(font, t, track) > maxw and cur:
            lines.append(cur); cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def lockup_sprite(c):
    # il lockup non puo essere piu largo della fascia libera, o finisce sul viso
    f_eye, f_t = mono(S.SIZE['eyebrow']), sans(S.SIZE['hook'], 900)
    track_e = S.TRACK['eyebrow'] * S.SIZE['eyebrow']
    track_t = S.TRACK['chapter'] * S.SIZE['hook']
    maxw = S.CARD_BOX[2] - 68
    lines, mark = [], []
    for i, ln in enumerate((c['l1'], c['l2'])):
        for w_ in wrap_to(f_t, ln, track_t, maxw):
            lines.append(w_); mark.append(i)
    w = int(max(tracked_width(f_eye, c['eyebrow'], track_e),
                max(tracked_width(f_t, l, track_t) for l in lines))) + 68
    h = 34 + S.SIZE['eyebrow'] + 18 + 6 + 26 + len(lines) * int(S.SIZE['hook'] * 1.10) + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 26, S.NAVY_DEEP + (216,)))
    d = ImageDraw.Draw(im)
    y = 34
    draw_tracked(d, (34, y), c['eyebrow'], f_eye, S.MINT + (255,), track_e)
    y += S.SIZE['eyebrow'] + 18
    d.rounded_rectangle([34, y, 118, y + 5], radius=2, fill=S.MINT + (255,))
    y += 26
    for i, ln in enumerate(lines):
        draw_tracked(d, (34, y), ln, f_t, (S.PAPER if mark[i] == 0 else S.MINT) + (255,),
                     track_t)
        y += int(S.SIZE['hook'] * 1.10)
    return im


def chip_sprite(c):
    f_n, f_r = sans(S.SIZE['chip_name'], 900), mono(S.SIZE['chip_role'])
    track_r = S.TRACK['eyebrow'] * S.SIZE['chip_role']
    w = int(max(f_n.getlength(c['name']), tracked_width(f_r, c['role'], track_r))) + 64
    h = 30 + S.SIZE['chip_name'] + 14 + S.SIZE['chip_role'] + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 20, S.NAVY_DEEP + (216,)))
    d = ImageDraw.Draw(im)
    d.text((32, 24), c['name'], font=f_n, fill=S.PAPER + (255,))
    draw_tracked(d, (32, 30 + S.SIZE['chip_name'] + 12), c['role'], f_r, S.MINT + (255,), track_r)
    return im


def closing_sprite(c):
    im = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (246,))
    d = ImageDraw.Draw(im)
    f_eye, f_t, f_cta, f_br = mono(S.SIZE['eyebrow'] + 6), sans(S.SIZE['chapter'], 900), \
        mono(S.SIZE['chapter_sub']), mono(S.SIZE['eyebrow'])
    tr = S.TRACK['eyebrow']
    y = S.H // 2 - 210
    ew = tracked_width(f_eye, c['eyebrow'], tr * (S.SIZE['eyebrow'] + 6))
    draw_tracked(d, ((S.W - ew) / 2, y), c['eyebrow'], f_eye, S.MINT + (255,),
                 tr * (S.SIZE['eyebrow'] + 6))
    y += S.SIZE['eyebrow'] + 34
    d.rounded_rectangle([S.W / 2 - 60, y, S.W / 2 + 60, y + 6], radius=3, fill=S.MINT + (255,))
    y += 46
    for i, ln in enumerate((c['l1'], c['l2'])):
        tw = tracked_width(f_t, ln, S.TRACK['chapter'] * S.SIZE['chapter'])
        draw_tracked(d, ((S.W - tw) / 2, y), ln, f_t, (S.PAPER if i == 0 else S.MINT) + (255,),
                     S.TRACK['chapter'] * S.SIZE['chapter'])
        y += int(S.SIZE['chapter'] * 1.16)
    y += 34
    cw = tracked_width(f_cta, c['cta'], tr * S.SIZE['chapter_sub'])
    box_w, box_h = cw + 96, S.SIZE['chapter_sub'] + 56
    d.rounded_rectangle([(S.W - box_w) / 2, y, (S.W + box_w) / 2, y + box_h],
                        radius=14, outline=S.MINT + (255,), width=4)
    draw_tracked(d, ((S.W - cw) / 2, y + 26), c['cta'], f_cta, S.MINT + (255,),
                 tr * S.SIZE['chapter_sub'])
    y += box_h + 46
    bw = tracked_width(f_br, c['brand'], tr * S.SIZE['eyebrow'])
    draw_tracked(d, ((S.W - bw) / 2, y), c['brand'], f_br, S.MUTED + (255,),
                 tr * S.SIZE['eyebrow'])
    return im


def fade_paste(base, sprite, box, alpha):
    if alpha <= 2:
        return
    if alpha >= 253:
        base.alpha_composite(sprite, box)
        return
    a = sprite.getchannel('A').point(lambda v: v * alpha // 255)
    s = sprite.copy()
    s.putalpha(a)
    base.alpha_composite(s, box)


class Scene:
    """Tiene gli sprite gia disegnati: si costruiscono una volta sola."""

    def __init__(self):
        self.cards = [(c, card_sprite(c)) for c in PLAN['cards']]
        self.chapters = [(c, chapter_sprite(c)) for c in PLAN['chapters']]
        self.lock = (PLAN['opening'], lockup_sprite(PLAN['opening']))
        self.chip = (PLAN['chip'], chip_sprite(PLAN['chip']))
        self.close = (PLAN['closing'], closing_sprite(PLAN['closing']))
        self.caps = PLAN['captions']
        self.dur = PLAN['duration']
        self.ci = 0

    def frame(self, t):
        base = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(base)
        d.rectangle([0, S.H - S.PROGRESS_H, S.W, S.H], fill=S.PAPER + (46,))
        d.rectangle([0, S.H - S.PROGRESS_H, int(S.W * t / self.dur), S.H], fill=S.MINT + (232,))

        for c, sp, y0 in ((self.lock[0], self.lock[1], S.CARD_BOX[1]),
                          (self.chip[0], self.chip[1], S.CHIP_POS[1])):
            if c['s'] <= t < c['e']:
                a = min((t - c['s']) / 0.45, (c['e'] - t) / 0.45, 1.0)
                rise = int(S.CARD_RISE * (1 - S.ease_out_expo(min((t - c['s']) / S.CARD_IN, 1))))
                x = S.SAFE if c.get('side', 'left') == 'left' else S.W - S.SAFE - sp.width
                fade_paste(base, sp, (x, y0 + rise), int(255 * max(a, 0)))

        for c, sp in self.cards:
            if not (c['s'] <= t < c['e']):
                continue
            rev = S.ease_out_expo(min((t - c['s']) / S.CARD_IN, 1.0))
            rise = int(S.CARD_RISE * (1 - rev))
            a = 255 if t < c['e'] - S.CARD_OUT else int(255 * max(0.0, (c['e'] - t) / S.CARD_OUT))
            wv = max(1, int(sp.width * rev))
            if c.get('side', 'left') == 'left':
                fade_paste(base, sp.crop((0, 0, wv, sp.height)),
                           (S.SAFE, S.CARD_BOX[1] + rise), a)
            else:
                fade_paste(base, sp.crop((sp.width - wv, 0, sp.width, sp.height)),
                           (S.W - S.SAFE - wv, S.CARD_BOX[1] + rise), a)

        for c, sp in self.chapters + [self.close]:
            if not (c['s'] <= t < c['e']):
                continue
            a = min(S.ease_out_cubic((t - c['s']) / S.CHAPTER_IN),
                    S.ease_out_cubic((c['e'] - t) / S.CHAPTER_OUT), 1.0)
            fade_paste(base, sp, (0, 0), int(255 * max(a, 0)))

        caps = self.caps
        while self.ci + 1 < len(caps) and caps[self.ci]['e'] < t:
            self.ci += 1
        while self.ci > 0 and caps[self.ci]['s'] > t:
            self.ci -= 1
        g = caps[self.ci]
        if g['s'] - 0.05 <= t < g['e']:
            active = -1
            for i, w in enumerate(g['words']):
                if w['s'] - 0.02 <= t < w['e'] + 0.06:
                    active = i
                    break
                if t >= w['e']:
                    active = i
            sp = caption_sprite(self.ci, active)
            p = min(max((t - g['s']) / S.CAP_IN, 0.0), 1.0)
            rise = int(S.CAP_RISE * (1 - S.ease_out_cubic(p)))
            fade_paste(base, sp, ((S.W - sp.width) // 2,
                                  S.CAPTION_BOT - sp.height + rise), int(255 * p))
        return base


def main():
    scene = Scene()
    out = sys.stdout.buffer
    t0 = time.time()
    for n in range(NFRAMES):
        out.write(scene.frame(n / FPS).tobytes())
        if n % 900 == 0 and n:
            el = time.time() - t0
            sys.stderr.write(f"  frame {n}/{NFRAMES}  {n/el:.1f} fps  "
                             f"restano {(NFRAMES-n)/(n/el)/60:.1f} min\n")
            sys.stderr.flush()
    out.flush()


if __name__ == '__main__':
    main()
