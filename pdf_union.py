import base64
import os
import sys
from io import BytesIO

from PyPDF2 import PdfFileMerger


class PdfUnion:
    """
    Classe para executar merge entre vários PDFs.
    """
    def __init__(self, *args):
        """
        Inializa a classe com o parâmetro args.
        :args: Recebe os nomes dos arquivos sem a extensão 'pdf'.
               O primeiro argumento é o nome do arquivo de saída.
               Os outros argumentos são arquivos de entrada.
        """
        self.is_generate_output_file = args[1].title() != 'None'
        self.is_input_base64 = args[0] == 'input_base64'
        self.output_file = args[1] + '.pdf'
        self.pdfs = args[2:]
        self._stream = None

    @property
    def stream(self):
        return self._stream

    def _add_files(self, merger):
        """
        Adiciona os nomes dos arquivos para o merger.
        :merger: Objeto de PdfMerger.
        """
        for pdf in self.pdfs:
            input_file = pdf + '.pdf'
            # Verifica se o arquivo de entrada existe.
            if not os.path.isfile(input_file):
                raise FileNotFoundError()
            # Executa o merge dos arquivos.
            merger.append(input_file)
        return self

    def _add_files_from_base64(self, merger):
        """
        Adiciona os stream de cada PDF para o merger.
        :merger: Objeto de PdfMerger.
        """
        for pdf in self.pdfs:
            merger.append(base64.decodebytes(pdf.encode()))
        return self

    def _save_to_file(self, merger):
        """
        Executa a criação do arquivo unido.
        :merger: Objeto de PdfMerger.
        """
        # Verifica se o arquivo de saída já existe.
        if os.path.isfile(self.output_file):
            # Exclui o arquivo de saída.
            os.remove(self.output_file)

        # Executa o merge entre os arquivos informados.
        merger.write(self.output_file)
        return self

    def _convert_to_base64(self, merger):
        """
        Converte o arquivo criado para base64.
        :merger: Objeto de PdfMerger.
        """
        stream = BytesIO()
        merger.write(stream)
        self._stream = base64.b64encode(stream.getvalue()).decode()
        return self

    def execute(self):
        """
        Executa o merge entre os arquivos informados.
        """
        merger = PdfFileMerger()
        try:
            if self.is_input_base64:
                # Adiciona arquvios de base64.
                self._add_files_from_base64(merger)
            else:
                # Adiciona arquivos de um caminho.
                self._add_files(merger)

            if self.is_generate_output_file:
                # Salva a saída em um caminho.
                self._save_to_file(merger)
            else:
                # Criar uma string base 64.
                self._convert_to_base64(merger)
        finally:
            merger.close()
        return self


if __name__ == '__main__':
    # Faz a verificação dos parâmetros.
    if len(sys.argv) > 1:
        # Instância e executa o objeto para fazer o merge entre os documentos.
        PdfUnion(*sys.argv).execute()
