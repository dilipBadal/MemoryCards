import pygame
import numpy as np

# ── INIT AUDIO ────────────────────────────────────────────────
try:
    pygame.mixer.init(44100, -16, 2, 512)
    AUDIO_READY = True
except pygame.error:
    # Some school/demo computers do not expose an audio device.
    # The game should still run; it will just skip sound effects.
    AUDIO_READY = False

SAMPLE_RATE = 44100

# ── AUDIO SYNTHESIZERS ─────────────────────────────────────────
def to_stereo(mono, vol):
    s = (mono * vol * 32767).astype(np.int16)
    return np.column_stack([s, s])

def make_tone(freq=440, duration=0.1, vol=0.4, wave="sine", fade=True):
    if not AUDIO_READY:
        return None
    n = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    if wave == "sine":
        s = np.sin(2 * np.pi * freq * t)
    elif wave == "square":
        s = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave == "tri":
        s = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    elif wave == "noise":
        s = np.random.uniform(-1, 1, n)
    else:
        s = np.sin(2 * np.pi * freq * t)
    if fade:
        s = s * np.linspace(1, 0, n)
    return pygame.sndarray.make_sound(to_stereo(s, vol))

def make_sweep(f_start, f_end, duration=0.15, vol=0.4, fade=True):
    if not AUDIO_READY:
        return None
    n     = int(SAMPLE_RATE * duration)
    freqs = np.linspace(f_start, f_end, n)
    phase = np.cumsum(2 * np.pi * freqs / SAMPLE_RATE)
    s     = np.sin(phase)
    if fade:
        s = s * np.linspace(1, 0, n)
    return pygame.sndarray.make_sound(to_stereo(s, vol))

def make_multi_tone(tone_list, vol=0.4):
    if not AUDIO_READY:
        return None
    all_samples = []
    for freq, dur, wave in tone_list:
        n = int(SAMPLE_RATE * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        if wave == "sine":
            s = np.sin(2 * np.pi * freq * t)
        elif wave == "square":
            s = np.sign(np.sin(2 * np.pi * freq * t))
        else:
            s = np.sin(2 * np.pi * freq * t)
        all_samples.append(s * np.linspace(1, 0, n))
    mono = np.concatenate(all_samples)
    return pygame.sndarray.make_sound(to_stereo(mono, vol))

# ── PRE-SYNTHESIZED SOUND EFFECTS ──────────────────────────────
select_snd      = make_tone(880, 0.06, vol=0.3, wave="sine")
flip_snd        = make_sweep(300, 900, duration=0.12, vol=0.35)
no_match_snd    = make_multi_tone([(440, 0.10, "sine"), (330, 0.14, "sine")], vol=0.4)
match_snd       = make_multi_tone([(523, 0.08, "sine"), (659, 0.08, "sine"), (784, 0.10, "sine")], vol=0.45)
game_finish_snd = make_multi_tone([(523, 0.10, "sine"), (659, 0.10, "sine"),
                                    (784, 0.10, "sine"), (1047, 0.20, "sine")], vol=0.5)
restart_snd     = make_multi_tone([(600, 0.07, "sine"), (400, 0.07, "sine"), (700, 0.10, "sine")], vol=0.4)
auto_snd        = make_sweep(200, 1200, duration=0.3, vol=0.3)

# ── PLAY HELPER ───────────────────────────────────────────────
def play(sound):
    if sound:
        sound.play()
