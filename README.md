## Form Submitter

A program that is purposed to do auto submit of an online form equipped with a CAPTCHA image-based reader using Optical Character Recognition (OCR).

Current captcha image samples that this program is able to read [(View Samples)](https://github.com/williamluisan/form-submitter/tree/master/public/images/sample).

### Requirements
* Python >= 3.12
* With `pip` as the package installer.
* Refers to [requirements.txt](https://github.com/williamluisan/form-submitter/blob/master/requirements.txt) for the full list of packages.

Featured packages:
* EasyOCR: *for Optical Character Recognition*.
* PyTesseract: *for Optical Character Recognition (option)*.
* BeautifulSoup4: *for web scraping*.
* Faker
* Dotenv

### Setup
1. Install required packages with `pip`
```python
pip install -r requirements.txt
```
2. Setup **.env** variables
* Copy `config/.env.sample` as `config/.env` 
* and filled in the `TARGER_URL`

3. ✅Done.

### Usage
```python
python -m cmmd.app
```
Brief on how the program works:

1. The program will try to make submission of an online form against the configured URL of `TARGET_URL`.
2. Regardless of whether the submission succeds or fails, the program will automatically retry submission at the specified time interval.
3. The auto-submission process will continue running until the user manually terminates the program.