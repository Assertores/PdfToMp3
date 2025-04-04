# PdfToMp3
This repository provids a Tool that can read in Pdf files and uses googles text to speach api to generate mp3 files.

## Install
### Bare Bones
1. enshure you have [Python](https://www.python.org/downloads/) installed
1. [clone](https://github.com/Assertores/PdfToMp3.git) this repository

### Optional
to be able to use the `--use Cloud` setting:

1. create a [google cloud project](https://console.cloud.google.com/welcome)
1. install the [gcloud-CLI](https://cloud.google.com/sdk/docs/install?hl=de)
1. setup [autentication](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=de) to youre google cloud project

## Usage
### Bare Bones
to convert a pdf file into mp3 run:
```
python PdfToMp3.py Path/To/File.pdf
```

### Optional

run `python PdfToMp3.py --help` to get a detailed explanation.

use `--at` and `--to` to only convert a range (in pages).
```
python PdfToMp3.py Path/To/File.pdf --at 5 --to 20
```

use `--patch` to replace special characters with discribing text, to make it apear in the mp3 (multiple values can be provided here).
```
python PdfToMp3.py Path/To/File.pdf --patch De
```

use `--use` to customice the output (multiple values can be provided here).
```
python PdfToMp3.py Path/To/File.pdf --use Cloud Text
```

use `--out` to chang the output folder
```
python PdfToMp3.py Path/To/File.pdf --out Path/To/SomewhereElse/
```
## Troubleshootung
### My convertion stops after about 30 pages or so
you are most likly using the `Translate` strategy (which is the default strategy). it is using a undocumented api from google translation, and it tents to block ip's if they do to many requests in a row.

consider setting up a [google cloud project](https://console.cloud.google.com/welcome) as it has no such restriction and has a better audio quality as well.

### I'm getting this error
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```
you most likly moved the script out of the file it came in, without also moving the `requirements.txt` as well. it is needed for the script to know which dependencies to install.

### I'm getting this error eventhough my pdf has content
```
ERROR The pdf was compleatly empty
```
your pdf seams to not have any **text** content. maybe it is scanned in and only a picture.

there is nothing here you can do. sorry.

## Thanks
- [lazycatcoder](https://github.com/lazycatcoder) for creating the spiritual predecessor of this project.