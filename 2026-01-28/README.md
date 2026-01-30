# 🎵 Note Trainer

A simple, mobile-friendly web app for practicing music notation reading. Built for Charles who's learning cello and wants to improve his note-reading speed.

## Features

- **Treble & Bass Clef** - Toggle between treble clef, bass clef, or mixed mode
- **Visual Staff** - Clean SVG rendering with proper clef symbols and ledger lines
- **Instant Feedback** - Shows correct/wrong immediately with the right answer
- **Score Tracking** - Keeps track of correct answers and current streak
- **Auto-Advance** - Automatically moves to next note after correct answers
- **Keyboard Support** - Use 1-7 for notes C-B, Space/Enter for next

## How to Use

1. Open `index.html` in any browser
2. Select clef mode (Treble, Bass, or Mixed)
3. Look at the note on the staff
4. Click the note name (C through B) or press 1-7
5. See if you got it right - streak builds on consecutive correct answers
6. Press "Next Note" or Space to continue (auto-advances on correct)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| 1-7 | Guess note C through B |
| C-B | Also works for note names |
| Space/Enter | Next note (after answering) |

## Technical Notes

- Pure HTML/CSS/JS - no dependencies, no build step
- Works offline once loaded
- Responsive design works on mobile
- Dark theme for late-night practice sessions

## For Cello Players

The bass clef is your home! But don't neglect treble - you'll need it for higher positions (thumb position territory). The "Mixed" mode helps train switching between both.

Note range covers roughly 2 octaves in each clef, including ledger lines above and below the staff.

---

*Built during nightly build - January 28, 2026*
