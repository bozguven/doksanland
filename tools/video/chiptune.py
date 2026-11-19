#!/usr/bin/env python3
"""Original 8-bit / chiptune loops for Doksanland Reels, synthesised from scratch (no samples, no downloads).

  python3 tools/video/chiptune.py <preset> <seconds> <out.wav>

Presets: paket (D01C, C major arcade arp + sparkle at 6.5 s), yazlik (D02A, G major, sparse then opens
up at 7.4 s), bulten (D03A, news-bulletin stabs + 3-note jingle). 120 BPM, 48 kHz stereo 16-bit,
gentle level (peak about -3 dBFS), fade-out at the end.
"""
import sys, wave
import numpy as np

SR = 48000
BPM = 120.0
BEAT = 60.0 / BPM          # 0.5 s
S16 = BEAT / 4             # 16th note
NAMES = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}


def hz(n):  # 'C4' -> Hz
    name, octv = n[:-1], int(n[-1])
    return 440.0 * 2 ** ((NAMES[name] + 12 * (octv + 1) - 69) / 12)


def env(n, a=0.004, d=0.08, s=0.55, r=0.03):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    rel = int(r * SR)
    if rel and n > rel:
        e[-rel:] *= np.linspace(1, 0, rel)
    return e


def square(f, n, duty=0.5):
    ph = (np.arange(n) * f / SR) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def triangle(f, n):
    ph = (np.arange(n) * f / SR) % 1.0
    return 4 * np.abs(ph - 0.5) - 1


rng = np.random.default_rng(90)  # seeded: the same track every build


def noise(n):
    return rng.uniform(-1, 1, n)


class Track:
    def __init__(self, secs):
        self.n = int(secs * SR)
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)

    def add(self, t, sig, gain, pan=0.0):
        i = int(t * SR)
        if i >= self.n:
            return
        sig = sig[: self.n - i] * gain
        self.L[i:i + len(sig)] += sig * (1 - max(pan, 0))
        self.R[i:i + len(sig)] += sig * (1 + min(pan, 0))

    def tone(self, t, note, dur, kind='sq', gain=0.1, duty=0.5, pan=0.0, **e):
        n = int(dur * SR)
        f = hz(note)
        s = square(f, n, duty) if kind == 'sq' else triangle(f, n)
        self.add(t, s * env(n, **e), gain, pan)

    def kick(self, t, gain=0.5):
        n = int(0.16 * SR)
        tt = np.arange(n) / SR
        f = 150 * np.exp(-tt * 28) + 55
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 22)
        self.add(t, s, gain)

    def hat(self, t, gain=0.05, length=0.03):
        n = int(length * SR)
        s = noise(n)
        s = np.diff(np.concatenate([[0], s]))  # crude high-pass
        self.add(t, s * np.exp(-np.arange(n) / SR * 120), gain, pan=0.2)

    def snare(self, t, gain=0.14):
        n = int(0.14 * SR)
        tt = np.arange(n) / SR
        s = noise(n) * np.exp(-tt * 30) + 0.4 * triangle(190, n) * np.exp(-tt * 40)
        self.add(t, s, gain, pan=-0.1)

    def sweep(self, t, f0, f1, dur, gain=0.06):  # rising arcade sparkle
        n = int(dur * SR)
        f = np.geomspace(f0, f1, n)
        ph = np.cumsum(f) / SR % 1.0
        s = np.where(ph < 0.25, 1.0, -1.0) * np.linspace(0.3, 1, n) * env(n, d=dur, s=1, r=0.05)
        self.add(t, s, gain)

    def finish(self, path, fade=1.2):
        m = np.stack([self.L, self.R], 1)
        m -= m.mean(0)
        f = int(fade * SR)
        m[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
        m[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
        m *= 0.7 / max(1e-9, np.abs(m).max())  # peak about -3 dBFS
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((m * 32767).astype('<i2').tobytes())


def chord_arp(tr, start, end, chords, lead_oct=5, bass_oct=3, lead_gain=0.07, bass_gain=0.16, duty=0.25, pattern=(0, 1, 2, 1)):
    """chords: list of (root, [semitone offsets]) one per bar (4 beats)."""
    t, k = start, 0
    while t < end - 1e-6:
        root, iv = chords[(k // 16) % len(chords)]
        base = NAMES[root]
        step = pattern[k % len(pattern)] if len(pattern) else 0
        semi = base + iv[step % len(iv)] + (12 if k % 8 >= 4 and len(pattern) > 3 else 0)
        note = list(NAMES)[semi % 12] + str(lead_oct + semi // 12)
        tr.tone(t, note, S16 * 0.9, 'sq', lead_gain, duty=duty, pan=0.15, d=0.05, s=0.35)
        if k % 2 == 0:  # bass on 8ths
            bn = root + str(bass_oct + (1 if k % 4 == 2 else 0))
            tr.tone(t, bn, S16 * 1.8, 'tri', bass_gain, d=0.12, s=0.6)
        t += S16; k += 1


def drums(tr, start, end, kick=0.45, snare=0.13, hat=0.045, half=False):
    t, b = start, 0
    while t < end - 1e-6:
        if b % 4 == 0 or (not half and b % 4 == 2):
            tr.kick(t, kick)
        if b % 4 in (1, 3) and not half or (half and b % 4 == 2):
            tr.snare(t, snare)
        tr.hat(t + BEAT / 2, hat)
        t += BEAT; b += 1


MAJ, MIN = [0, 4, 7], [0, 3, 7]


def paket(secs):
    tr = Track(secs)
    prog = [('C', MAJ), ('A', MIN), ('F', MAJ), ('G', MAJ)]
    chord_arp(tr, 0, 6.5, prog, lead_gain=0.06)
    drums(tr, 2.0, 6.5, half=True)
    # 4.0-6.5: tension, a high pedal tick
    for i in range(10):
        tr.tone(4.0 + i * BEAT / 2, 'G6', 0.05, 'sq', 0.03, duty=0.125)
    tr.sweep(5.9, 400, 2400, 0.6)
    # 6.5: the TAZO reveal, fanfare + busier groove
    for j, nt in enumerate(['C5', 'E5', 'G5', 'C6']):
        tr.tone(6.5 + j * 0.08, nt, 0.5, 'sq', 0.06, duty=0.5, d=0.25, s=0.4)
    chord_arp(tr, 6.5, secs, [('F', MAJ), ('G', MAJ), ('C', MAJ), ('C', MAJ)], lead_gain=0.06, duty=0.125, pattern=(0, 1, 2, 3, 2, 1))
    drums(tr, 6.5, secs - 0.5)
    tr.finish(sys.argv[3])


def yazlik(secs):
    tr = Track(secs)
    prog = [('G', MAJ), ('E', MIN), ('C', MAJ), ('D', MAJ)]
    # quiet dawn: slow arp, no drums
    chord_arp(tr, 0, 2.0, prog, lead_gain=0.045, bass_gain=0.1, pattern=(0, 2, 1, 2))
    chord_arp(tr, 2.0, 7.4, prog, lead_gain=0.055, bass_gain=0.14)
    drums(tr, 2.0, 7.4, half=True, kick=0.35)
    tr.sweep(6.8, 300, 1800, 0.6, gain=0.05)
    # 7.4: the sea, music opens up (melody on top, full drums)
    chord_arp(tr, 7.4, secs, [('C', MAJ), ('D', MAJ), ('G', MAJ), ('G', MAJ)], lead_gain=0.045, duty=0.125)
    drums(tr, 7.4, secs - 0.5)
    mel = ['B5', 'D6', 'G6', 'F#6', 'E6', 'D6', 'B5', 'D6', 'E6', 'D6']
    for i, nt in enumerate(mel):
        tr.tone(7.4 + i * BEAT * 0.5 + (0 if i < 5 else BEAT), nt, BEAT * 0.45, 'sq', 0.05, duty=0.5, pan=-0.15, d=0.15, s=0.5)
    tr.finish(sys.argv[3])


def bulten(secs):
    tr = Track(secs)
    # 3-note news jingle
    for j, (nt, d) in enumerate([('D5', 0.18), ('A5', 0.18), ('F#6', 0.5)]):
        tr.tone(0.02 + j * 0.2, nt, d, 'sq', 0.07, duty=0.5, d=0.2, s=0.6)
        tr.tone(0.02 + j * 0.2, nt[:-1] + str(int(nt[-1]) - 1), d, 'tri', 0.1)
    # steady pulse bed: stabs on the off-beats, 16th bass
    prog = [('D', [0, 4, 7, 11]), ('B', [0, 3, 7, 10]), ('G', [0, 4, 7, 11]), ('A', [0, 4, 7])]
    t, k = 0.75, 0
    while t < secs:
        root, iv = prog[int((t - 0.75) // 2.0) % 4]
        if k % 2 == 1:
            for s in iv[:3]:
                semi = NAMES[root] + s
                tr.tone(t, list(NAMES)[semi % 12] + str(4 + semi // 12), 0.12, 'sq', 0.025, duty=0.25, d=0.06, s=0.3)
        bn = root + ('2' if k % 2 == 0 else '3')
        for q in range(2):
            tr.tone(t + q * S16, bn, S16 * 0.8, 'tri', 0.12, d=0.05, s=0.5)
        t += BEAT / 2; k += 1
    # ticker blips every beat
    for i in range(int((secs - 0.75) / BEAT)):
        tr.tone(0.75 + i * BEAT, 'D7', 0.02, 'sq', 0.012, duty=0.125)
    drums(tr, 0.75, secs - 0.5, kick=0.4, snare=0.1, hat=0.04)
    # sign-off sting at 11.3
    for j, nt in enumerate(['A5', 'D6']):
        tr.tone(11.3 + j * 0.15, nt, 0.4, 'sq', 0.06, d=0.2, s=0.5)
    tr.finish(sys.argv[3])


if __name__ == '__main__':
    {'paket': paket, 'yazlik': yazlik, 'bulten': bulten}[sys.argv[1]](float(sys.argv[2]))
