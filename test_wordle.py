import pytest
import main
def test_abrir_conexion_existe():
    main_attrs = dir(main)
    assert 'abrir_conexion' in main_attrs