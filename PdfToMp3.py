#!/usr/bin/env python

import subprocess
import sys
import os

print("installing dependencies ...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"], cwd=os.path.dirname(__file__))

import argparse
import PyPDF2
from google.cloud import texttospeech
from gtts import gTTS

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def TTS(aText, aLanguage, aOutputFile):
    client = texttospeech.TextToSpeechClient()

    inputText = texttospeech.SynthesisInput(text=aText)

    voice = texttospeech.VoiceSelectionParams(
        language_code=aLanguage,
    )

    audioConfig = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": inputText, "voice": voice, "audio_config": audioConfig}
    )

    with open(aOutputFile + ".mp3", "wb") as out:
        out.write(response.audio_content)

def PatchGerman(text: str) -> str:
    text = text.replace(" ¨o", "ö")
    text = text.replace(" ¨u", "ü")
    text = text.replace(" ¨a", "ä")
    text = text.replace(" ¨A", "Ä")
    text = text.replace(" ¨O", "Ö")
    text = text.replace(" ¨U", "Ü")
    text = text.replace("¨o", "ö")
    text = text.replace("¨u", "ü")
    text = text.replace("¨a", "ä")
    text = text.replace("¨A", "Ä")
    text = text.replace("¨O", "Ö")
    text = text.replace("¨U", "Ü")
    text = text.replace("ß", "ss")
    return text

def PatchMathNotation(text: str) -> str:
    text = text.replace(":=", " ist die Menge aller ")
    text = text.replace("/braceleftigg", " mit den folgenden Fällen ")
    text = text.replace("∝⇕⊣√∫⊔≀→", " wird abgebildet auf ")
    text = text.replace("/summationdisplay", " Summe ")
    text = text.replace("ˆ =", " Entspricht ")
    text = text.replace('̸=', " Ungleich ")
    text = text.replace('̸∈', " nicht Element von ")

    text = text.replace('∈', " element von ")
    text = text.replace('→', " bildet ab auf ")
    #text = text.replace(':', " für die gilt ")
    text = text.replace('◦', " komposit ")
    text = text.replace('□', " ende des beweises ")
    text = text.replace('∅', " die leere Menge ")
    text = text.replace('∪', " Vereinigt mit ")
    text = text.replace('∩', " Geschnitten mit ")
    text = text.replace('×', " Kreuz ")
    text = text.replace('\\', " Ohne ")
    text = text.replace('∞', " unendlich ")
    text = text.replace('⊆', " teilmenge von ")
    text = text.replace('⇒', " impliziert ")
    text = text.replace('⇐', " wird impliziert durch ")
    text = text.replace('¬', " nicht ")
    text = text.replace('⇔', " ist äquivalent zu ")
    text = text.replace('∀', " für alle ")
    text = text.replace('∃', " es gibt ein ")
    text = text.replace('Σ', " Summe ")
    text = text.replace('≥', " Größer oder Gleich ")
    text = text.replace('≤', " Kleiner oder Gleich ")
    text = text.replace('∧', " Logisches und ")
    text = text.replace('∨', " Logisches oder ")
    text = text.replace('⊕', " Exklusiv oder ")
    return text

def main():
    argpars = argparse.ArgumentParser(
        description="this tool converts pdfs into mp3s using googles text to speech library"
    )
    argpars.add_argument("--out", type=str, help="the folder to put the mp3 files into. default = 'path' as folder")
    #argpars.add_argument("--language", type=str, default="de-DE", help="the language code (e.g. en-US) to be used for tts")
    argpars.add_argument("--language", type=str, help="the language code (e.g. en-US) to be used for tts. default = 'de-DE'")
    argpars.add_argument("--at", type=int, help="the page number to start from. default ='1'")
    argpars.add_argument("--to", type=int, help="the page number to end at. default = 'pdf pagecount'")
    argpars.add_argument("--use", choices=["Text", "Translate", "Cloud"], nargs='+', help="the strategy to use for the text from the pdf. default = '[Translate]'")
    argpars.add_argument("--patch", choices=["De", "DeMath"], nargs='*', help="specifies which text replacments shall happon. default = '[]'")
    argpars.add_argument("path", type=str, help="the path to the pdf to be converted")

    args = argpars.parse_args()

    # if you want to add debugging infos here again because the optional
    # argument isn't working, remember that the debug console quotes all
    # arguments once, that's why it is all ending up in path.

    if not os.path.isfile(args.path):
        eprint(args.path, "must be a valid file")
        sys.exit(1)

    if os.path.splitext(args.path)[1] != ".pdf":
        eprint(args.path, "must be a valid pdf")
        sys.exit(2)

    print("read in pdf:", os.path.abspath(args.path))
    pdfFile = open(args.path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFile, True)

    pageCount = len(pdfReader.pages)
    if not args.at:
        args.at = 1
        print("default value 'at':", args.at)
    if not args.to or args.to < args.at:
        args.to = pageCount
        print("default value 'to' to pageCount:", args.to)

    if not args.language:
        args.language = "de-DE"
        print("default value 'language':", args.language)

    if not args.patch:
        args.patch = []
        print("no patch is chosen")
    
    if len(args.language) != 5 or args.language[2] != '-' or any(c for c in args.language[:2] if c.isupper()) or any(c for c in args.language[3:] if c.islower()):
        print("invalid format of '" + args.language + "' using default value 'language':", "de-DE")
        args.language = "de-DE"

    if not args.use:
        args.use = ["Translate"]
        print("default value 'use':", args.use)

    if not args.out:
        filename = os.path.basename(args.path)
        subfoldername = os.path.splitext(filename)[0]
        dirname = os.path.dirname(args.path)
        args.out = os.path.join(dirname,subfoldername)
        print("default output to:", os.path.abspath(args.out))
    os.makedirs(args.out,exist_ok=True)

    hasDoneSomething = False
    print("start convertion:", args.at, ":", args.to)
    for pageNum in range(args.at, min(args.to, len(pdfReader.pages)) + 1):
        print("[", pageNum, ":", args.to, "]")
        page = pdfReader.pages[pageNum - 1].extract_text()
        text = page.strip().replace("\n", " ")
        if not text:
            continue
        hasDoneSomething = True

        if "De" in args.patch:
            text = PatchGerman(text)
        if "DeMath" in args.patch:
            text = PatchMathNotation(text)

        outPath = os.path.join(args.out, str(pageNum));
        if "Text" in args.use:
            with open(outPath + ".txt", "w", encoding="utf-8") as out:
                out.write(text)

        if "Translate" in args.use:
            tts = gTTS(text=text, lang=args.language[:2], slow=False)
            try:
                tts.save(outPath + ".mp3")
            except:
                eprint("code failed at page:", pageNum)
                os.remove(outPath + ".mp3")
                sys.exit(3)

        if "Cloud" in args.use:
            TTS(text, args.language, outPath)
    if not hasDoneSomething:
        eprint("ERROR The pdf was compleatly empty")

    print("DONE")

if __name__ == "__main__":
    sys.exit(main())
