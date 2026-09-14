package com.lab02.katas;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class TarifaBicicletarioTest {

    @ParameterizedTest(name = "[{index}] {0} minutos -> {1} centavos")
    @CsvSource({
        "0, 0",
        "20, 0",
        "21, 300",
        "60, 300",
        "61, 450",
        "91, 600",
        "5000, 2000"
    })
    void calcularCentavosCasosNormais(int minutos, int esperado) {
        assertEquals(esperado, TarifaBicicletario.calcularCentavos(minutos));
    }

    @Test
    void calcularCentavosComMinutosNegativoLancaExcecao() {
        assertThrows(IllegalArgumentException.class, () -> TarifaBicicletario.calcularCentavos(-1));
    }
}
