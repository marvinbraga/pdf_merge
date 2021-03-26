import base64
import os

from pikepdf import Pdf


class MergePdfs:

    def __init__(self, *pdfs):
        self._pdfs = pdfs
        self._pdf = None

    @property
    def pdf(self):
        return self._pdf

    def execute(self, output):
        self._pdf = Pdf.new()
        for file_pdf in self._pdfs:
            print(f'*** O arquivo {file_pdf} não existe.')
            if os.path.isfile(file_pdf):
                print(f'O arquivo {file_pdf} existe.')
                try:
                    src = Pdf.open(file_pdf)
                except Exception as e:
                    print('***** Erro: ', str(e))
                    raise
                else:
                    print(f'O arquivo {file_pdf} foi aberto com sucesso.')
                    self._pdf.pages.extend(src.pages)

        self._pdf.save(output, linearize=True)
        print(f'O arquivo {output} foi salvo com sucesso.')

        return self


pdf = MergePdfs(
    'D:\\delphi\\_TEMP\\01\\01.pdf',
    'D:\\delphi\\_TEMP\\01\\02.pdf'
).execute('D:\\delphi\\_TEMP\\01\\merged.pdf').pdf

b64 = base64.encodebytes(pdf.make_stream())
