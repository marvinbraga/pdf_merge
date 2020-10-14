import base64
import os
from io import BytesIO

import pytest

from PyPDF2 import PdfFileReader
from pdf_union import PdfUnion


@pytest.fixture
def file_input_base64_result():
    """
    Prepara os argumentos para:
        - Não receberá entradas em base64 e sim os nomes nos arquivos.
        - Informa que não irá gerar um arquivo de saída.
        - Informa os nomes dos arquivos PDFs de entrada.
    """
    args = ['', 'None', 'pg_01', 'pg_02', 'pg_03', 'pg_04', 'pg_05']
    pdf = PdfUnion(*args)
    return pdf


@pytest.fixture
def file_input_file_result():
    """
    Prepara os argumentos para:
        - Não receberá entradas em base64 e sim os nomes nos arquivos.
        - Informa o nome do arquivo de saída.
        - Informa os nomes dos arquivos PDFs de entrada.
    """
    args = ['', 'result', 'pg_01', 'pg_02', 'pg_03', 'pg_04', 'pg_05']
    pdf = PdfUnion(*args)
    return pdf


@pytest.fixture
def base64_input_base64_result():
    """
    Prepara os argumentos para:
        - Receberá entradas em base64.
        - Informa que não irá gerar um arquivo de saída.
        - Informa as strings em base64 dos pdfs pg_01 e pg02.
    """
    args_inputs = [['', 'None', 'pg_01'], ['', 'None', 'pg_02']]
    args = [PdfUnion(*x).execute().stream for x in args_inputs]
    args.insert(0, 'None')
    args.insert(0, 'input_base64')
    pdf = PdfUnion(*args)
    return pdf


@pytest.fixture
def base64_input_file_result():
    """
    Prepara os argumentos para:
        - Receberá entradas em base64.
        - Informa o nome do arquivo de saída.
        - Informa as strings em base64 dos pdfs pg_01 e pg02.
    """
    args_inputs = [['', 'None', 'pg_01'], ['', 'None', 'pg_02']]
    args = [PdfUnion(*x).execute().stream for x in args_inputs]
    args.insert(0, 'result')
    args.insert(0, 'input_base64')
    pdf = PdfUnion(*args)
    return pdf


@pytest.mark.usefixtures
def test_file_input_base64_result_init(file_input_base64_result):
    """
    Verifica se:
        - Não está gerando um arquivo de saída.
        - Não está recebendo como entrada valores em base64.
    """
    assert not file_input_base64_result.is_generate_output_file and not file_input_base64_result.is_input_base64


@pytest.mark.usefixtures
def test_file_input_file_result_init(file_input_file_result):
    """
    Verifica se:
        - Está gerando um arquivo de saída.
        - Não está recebendo como entrada valores em base64.
    """
    assert file_input_file_result.is_generate_output_file and not file_input_file_result.is_input_base64


@pytest.mark.usefixtures
def test_base64_input_base64_result_init(base64_input_base64_result):
    """
    Verifica se:
        - Não está gerando um arquivo de saída.
        - Não está recebendo como entrada valores em base64.
    """
    assert not base64_input_base64_result.is_generate_output_file and base64_input_base64_result.is_input_base64


@pytest.mark.usefixtures
def test_base64_input_file_result_init(base64_input_file_result):
    """
    Verifica se:
        - Está gerando um arquivo de saída.
        - Não está recebendo como entrada valores em base64.
    """
    assert base64_input_file_result.is_generate_output_file and base64_input_file_result.is_input_base64


@pytest.mark.usefixtures
def test_generate_base64_from_file(file_input_base64_result):
    """
    Teste para verificar se está gerando uma saída com string.
    O atributo stream é inicializado com None.
    """
    base64_text = file_input_base64_result.execute().stream
    stream = BytesIO(base64.decodebytes(base64_text.encode()))
    pages_count = PdfFileReader(stream).numPages
    assert base64_text is not None and pages_count == 5


@pytest.mark.usefixtures
def test_generate_file_from_file(file_input_file_result):
    """
    Gera o PDF de saída chamado result.pdf, depois faz sua exclusão.
    Verifica se o arquivo foi gerado e se não gerou nenhum stream.
    """
    file_input_file_result.execute()
    is_result_exists = os.path.isfile('result.pdf')
    pages_count = PdfFileReader('result.pdf').numPages
    if is_result_exists:
        os.remove('result.pdf')
    assert is_result_exists and file_input_file_result.stream is None and pages_count == 5


@pytest.mark.usefixtures
def test_generate_base64_from_base64(base64_input_base64_result):
    """
    Teste para verificar se está gerando uma saída com string a partir de um base64.
    O atributo stream é inicializado com None.
    """
    base64_text = base64_input_base64_result.execute().stream
    stream = BytesIO(base64.decodebytes(base64_text.encode()))
    pages_count = PdfFileReader(stream).numPages
    assert base64_text is not None and pages_count == 2


@pytest.mark.usefixtures
def test_generate_file_from_base64(base64_input_file_result):
    """
    Gera o PDF de saída chamado result.pdf, a partir de um base64, depois faz sua exclusão.
    Verifica se o arquivo foi gerado e se não gerou nenhum stream.
    """
    base64_input_file_result.execute()
    is_result_exists = os.path.isfile('result.pdf')
    pages_count = PdfFileReader('result.pdf').numPages
    if is_result_exists:
        os.remove('result.pdf')
    assert is_result_exists and base64_input_file_result.stream is None and pages_count == 2
