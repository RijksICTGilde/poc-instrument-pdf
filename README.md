# How To

Steps to go from an instrument in the instrument registry (iama.yaml in this self contained example) through filling 
out a pdf to a filled out assessment card. 

1. Generate a PDF from an instrument:
    ```shell
    python generate.py iama.yaml iama.pdf 
    ```

2. Work in the PDF to answer questions and save the pdf.

3. Extract answers to an assessment card:
    ```shell
    python extract.py iama.pdf iama.out.yaml
    ```