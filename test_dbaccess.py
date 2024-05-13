import pytest
import main
def test_abrir_conexion_existe():
    main_attrs = dir(main)
    assert 'abrir_conexion' in main_attrs
def test_consulta_generica():
    main_attrs = dir(main)
    assert 'consulta_generica' in main_attrs
    
def test_jugadores_existe():
    main_attrs = dir(main)
    assert 'jugadores' in main_attrs
def test_jugadas_existe():
    main_attrs = dir(main)
    assert 'jugadas' in main_attrs
def test_palabras_existe():
    main_attrs = dir(main)
    assert 'palabras' in main_attrs

def test_jugador_existe():
    main_attrs = dir(main)
    assert 'jugador' in main_attrs    