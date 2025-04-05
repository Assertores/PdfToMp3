# PdfToMp3
This repository provides a tool that can read Pdf files and uses Google's text to speech API to generate .mp3 files.

## Install
### Bare Bones
1. Ensure you have [Python](https://www.python.org/downloads/) installed
1. [clone](https://github.com/Assertores/PdfToMp3.git) this repository

### Optional
To be able to use the `--use Cloud` setting:

1. Create a [Google cloud project](https://console.cloud.google.com/welcome)
1. Install [gcloud-CLI](https://cloud.google.com/sdk/docs/install?hl=de)
1. Setup [autentication](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=de) to your Google cloud project

## Usage
### Bare Bones
To convert a .pdf file into .mp3, run:
```
python PdfToMp3.py Path/To/File.pdf
```

### Optional

Run `python PdfToMp3.py --help` to get a detailed explanation.

Use `--at` and `--to` to only convert a range (in pages).
```
python PdfToMp3.py Path/To/File.pdf --at 5 --to 20
```

use `--patch` to replace special characters with discribing text, to make it apear in the mp3 (multiple values can be provided here).
to for example replace all ` ¨o` with the corresponding german character `ö` (and simular), you can run
```
python PdfToMp3.py Path/To/File.pdf --patch De
```

Use `--use` to customize the output (multiple values can be provided here).
```
python PdfToMp3.py Path/To/File.pdf --use Cloud Text
```

Use `--out` to change the output folder
```
python PdfToMp3.py Path/To/File.pdf --out Path/To/SomewhereElse/
```
## Troubleshootung
### My conversion stops after about 30 pages or so
You are most likly using the `Translate` strategy (which is the default strategy). It's using an undocumented API from Google translation, and it tends to block IPs if they do too many requests in a row.

Consider setting up a [Google cloud project](https://console.cloud.google.com/welcome) as it has no such restriction and has better audio quality.

### I'm getting this error
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```
You most likely moved the script out of the file it came in, without also moving the `requirements.txt` file as well. It is needed for the script to know which dependencies to install.

### I'm getting this error even though my pdf has content
```
ERROR The pdf was compleatly empty
```
your pdf seams to not have any **text** content. e.g. it is a picture of text, but not actual text in the sence of characters, that you can highlight and copy past out of the pdf.

There is nothing here you can do. Sorry.

## Thanks
- [lazycatcoder](https://github.com/lazycatcoder) for creating the spiritual predecessor of this project.