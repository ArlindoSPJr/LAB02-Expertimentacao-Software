package com.lab02.katas;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SkuValidatorTest {

    @ParameterizedTest(name = "[{index}] {0} -> {1}")
    @CsvSource(nullValues = "NULL", value = {
        "ABC-0000-6, OK",
        "ABC-1234-6, OK",
        "abc-0000-6, FORMATO",
        "ABC-000-6, FORMATO",
        "ABC00006, FORMATO",
        "ABC-0000-7, DV",
        "NULL, FORMATO",
        "'', FORMATO"
    })
    void validarProduzResultadoEsperado(String codigo, String esperado) {
        assertEquals(esperado, SkuValidator.validar(codigo));
    }
}
