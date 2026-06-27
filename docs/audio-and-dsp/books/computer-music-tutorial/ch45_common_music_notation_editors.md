# Ch 45: Common Music Notation Editors

## Table of Contents

- [1. The Complexity of Music Notation](#1-the-complexity-of-music-notation)
- [2. Historical Development of Music Editors](#2-historical-development-of-music-editors)
- [3. Rule-Based versus Graphics-Based Editors](#3-rule-based-versus-graphics-based-editors)
- [4. Functionality and Output of CMN Editors](#4-functionality-and-output-of-cmn-editors)
- [5. Automatic Transcription from MIDI](#5-automatic-transcription-from-midi)
- [6. Interchange Standards: MusicXML and IEEE 1599](#6-interchange-standards-musicxml-and-ieee-1599)

## 1. The Complexity of Music Notation

- **Common music notation (CMN)** — the standard Western notation system originating in Europe in the early seventeenth century; this chapter covers software for its traditional uses: score editing, printing, and file export
- **Why notation is hard** — far more complex than text or math; in a single chord, note heads, stems, augmentation dots, flags, accidentals, and markings must make room for one another, inter-note spacing varies with duration, and many staves must align vertically in polyphony — all involving context-sensitive decisions
- **Little abstraction** — apart from "macro" markings like *accelerando* and repeat signs such as *D.S.* (*dal segno*), CMN has no abstractions for time order; *music engraving* expertise is a deep skill rarely taught in music schools
- **Code-base scale** — the complexity shows in source size: LilyPond exceeds one million lines across nineteen languages (led by C++, Scheme, Python, MetaFont)
- **Entry-level vs professional split** — the main way to simplify an editor is to limit the music it handles (e.g. a simple editor may forbid mid-piece time-signature changes); professional engravers (Finale, Sibelius, Dorico, MuseScore) trade ease for flexibility
- **LilyPond** — a music *engraving* / score-input language closer to LaTeX than to graphical editors: one types text that is compiled into high-quality sheet music rather than dragging notes from a toolbar

## 2. Historical Development of Music Editors

- **Printing background** — movable type arrived in 1450; first printed music notation appeared in 1473, but it took a full century after Gutenberg's invention for the first collection of polyphonic music notation using movable type — Petrucci's volumes at Venice — to appear; CMN stabilized around 1600 and printing changed little for \~360 years
- **First programs** — Hiller and Baker ran the first music-printing experiments (1961, University of Illinois) on a modified Musicwriter typewriter; the National Research Council (Ottawa, late 1960s) built an early graphical editor using a clavier and "positioning wheel"
- **Mainframe editors (1970s)** — Leland Smith's *MS* (Stanford, PDP-10), where each symbol had a textual representation, allowed custom symbols and layout (leading to SCORE and WinScore, long favored by publishers); Donald Byrd's batch-oriented *SMUT* emphasized device independence; early commercial systems included Musicomp and Dataland's Scan-Note
- **Minicomputer editors (late 1970s)** — UNIX prototypes Ludwig, Scriva (Toronto), and MIT's Nedit explored note-entry methods (keyboard, menu/mouse, command, stylus) — no single best way emerged; they ran on slow *vector displays* (refresh under 5 Hz) versus today's *bit-mapped raster* displays at 60 Hz+
- **Workstation editors (early 1980s)** — MUZACS (MIT AI Lab LISP Machine), and Xerox PARC's *Mockingbird* (Dorado workstation, 1981) for piano notation via piano-roll entry then menu editing; the commercial Synclavier Music Engraving System offered high-quality printing at tens of thousands of dollars
- **Personal computers** — first generation in 1985 (Professional Composer, Score, Personal Composer, Deluxe Music Construction Set); 1988 brought Finale and NoteWriter with MIDI transcription; today over two hundred CMN applications exist

## 3. Rule-Based versus Graphics-Based Editors

- **Rule-based editors** — programs like Finale that *understand* notation rules, tracking pitch and duration to enable transposition, rhythmic error detection, automatic symbol positioning, and MIDI playback; automatic decisions speed conventional setting
- **Graphics-based editors** — treat notation as a collection of graphic symbols arrangeable freely (e.g. NoteWriter); not linked to MIDI, but the visual freedom suits new and experimental music — analogous to the *vector object* vs *bitmap* split in drawing programs
- **Hybrid practice** — some editors handle both and let users choose which rules apply and override automatic decisions; many professionals draft in a rule-based program (LilyPond, Sibelius) then export fragments as PDF or EPS for final layout in a graphics program like Adobe Illustrator

## 4. Functionality and Output of CMN Editors

- **Six operation classes** — interactive CMN editors divide into *setup* (clef, time/key signature, layout), *raw note entry*, *editing music data*, *text data entry*, *printing*, and *playback*; a scripted editor like LilyPond achieves equivalent effects through text commands
- **Note-entry methods** — alphanumeric keyboard, menus, command keys, optical score reader, MIDI input device, or MIDI files from sequencers/algorithmic programs; raw note data is only the starting point before editing into a finished score
- **Stylus and optical input** — *optical music recognition* (OMR) reads scanned scores; apps like StaffPad and MyScript (in Presonus Notion) typeset handwritten stylus input in real time, even taking voice commands
- **Advantages** — memorized, freely recombined score fragments; MIDI dictation; one-step part extraction from a full score (replacing days of manual copying); engraving-quality print; and MIDI playback that reveals notation errors by ear
- **Music font resolution** — Adobe's PostScript font *Sonata* (Cleo Huggins, 1986) hugely improved quality; PostScript fonts are *scalable* outlines (mathematical curves) adapting to device *resolution* in dpi/ppi; clean angled beams need \~1,200 dpi printing

## 5. Automatic Transcription from MIDI

- **Automatic transcription** — converts a performance (usually on a MIDI keyboard played to a metronome, or any standard MIDI file) into notation by segmenting control data into beats and measures
- **Quantization factor** — because human performance is not metrically perfect, this setup parameter sets the minimum transcribed note duration, ignoring small timing variations; literal transcription of imperfect timing is unreadable
- **Reference beat** — accurate transcription needs a beat source; some programs let users tap their own; beatless transcription (the computer must "find the beat") is a hard, still-researched problem
- **Inevitable manual cleanup** — even with a beat and quantization, results need editing for colliding symbols, rhythmic-parsing errors, missed key/meter changes, missing dynamics and slurs, and poor justification
- **Custom symbols** — most editors import graphic-program images for custom or unconventional elements (e.g. tape-sound icons), or export EPS/PDF fragments for arrangement in Adobe Illustrator
- **Browser-based education apps** — NoteFlight and Flat let students on any device share one app, edit a composition collaboratively in real time, and keep a cloud-stored edit history

## 6. Interchange Standards: MusicXML and IEEE 1599

- **MusicXML** — an XML-based notation *interchange* language (first proposed 2000, Good) representing common notation from the seventeenth century onward; not meant to supersede application-specific languages but to share data, it is today the universal sheet-music exchange format across MuseScore, Sibelius, Finale, Dorico, and 200+ others
- **IEEE 1599** — a music representation standard encoding *all* music-related dimensions (audio, performance, score, metadata) in XML, integrating the layers so one can, for instance, follow score notation while listening to the corresponding audio or compare different graphical representations and performances in real time
