# Form Submitter

A program that is purposed to do auto submit of online forms with captcha image reader built with python.

Required Python >= 3.12

Current captcha images (sample) that this program is able to read [link](https://github.com/williamluisan/form-submitter/tree/master/public/images/sample).

## Requirements
* With `pip` as the package installer.
* Refers to [requirements.txt](https://github.com/williamluisan/form-submitter/blob/master/readme.md) .

Highlighted packages:
* Dotenv
* Faker
* BeautifulSoup4
* EasyOCR
* PyTesseract

## Setup
1. Install requirements with `pip`
```python
pip install -r requirements.txt
```
2. Setup **.env** variables
* Copy `config/.env.sample` as `config/.env` 
* and filled in the `TARGER_URL`

3. ✅Done.

## Usage
```python
python -m cmmd.app
```
Brief on how the program run:

Lorem ipsum sir dolor amet, Lorem ipsum sir dolor amet.  