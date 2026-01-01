Sound Effects for BhashaMitra

Download FREE sound effects from [Mixkit](https://mixkit.co/free-sound-effects/) and save them here.

## Required Sound Files

| File Name | Mixkit Search Term | Suggested Sound |
|-----------|-------------------|-----------------|
| `correct.mp3` | "correct notification" | "Correct answer tone" |
| `wrong.mp3` | "wrong buzzer" | "Wrong answer fail tone" |
| `level-up.mp3` | "level up" | "Video game level up" |
| `badge.mp3` | "achievement unlock" | "Achievement bell" |
| `click.mp3` | "click" | "Simple click" |
| `page-turn.mp3` | "page flip" | "Book page flip" |
| `celebration.mp3` | "celebration" | "Happy kids cheer" |
| `meow.mp3` | "cat meow" | "Cute cat meow" |
| `streak.mp3` | "streak milestone" | "Game bonus" |
| `story-complete.mp3` | "story complete" | "Magical notification" |
| `pop.mp3` | "pop bubble" | "Bubble pop" |
| `whoosh.mp3` | "whoosh" | "Fast swoosh" |

## How to Download

1. Go to https://mixkit.co/free-sound-effects/
2. Search for the suggested term
3. Download the MP3 file
4. Rename it to match the file name above
5. Place it in this directory (`public/audio/sounds/`)

## Alternative Sources

- [Pixabay Sound Effects](https://pixabay.com/sound-effects/) - Free, no attribution required
- [Freesound](https://freesound.org/) - Free with attribution
- [Zapsplat](https://www.zapsplat.com/) - Free with attribution

## Volume Guidelines

- Keep sound files normalized to similar volume levels
- Recommended peak: -6dB to -3dB
- Use short sounds (< 2 seconds) for UI feedback
- Longer sounds (up to 5 seconds) for celebrations

## Testing

After adding sounds, test them by opening the browser console and running:
```javascript
import { soundService } from '@/lib/soundService';
soundService.preload();
soundService.onCorrect();
```
