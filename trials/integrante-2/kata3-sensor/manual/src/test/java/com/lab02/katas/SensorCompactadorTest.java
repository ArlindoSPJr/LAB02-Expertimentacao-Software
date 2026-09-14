package com.lab02.katas;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Collections;
import java.util.List;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class SensorCompactadorTest {

    @ParameterizedTest(name = "[{index}] {3}")
    @MethodSource("casos")
    void compactarProduzFaixasEsperadas(int[] leituras, int tolerancia, List<String> esperado, String descricao) {
        assertEquals(esperado, SensorCompactador.compactar(leituras, tolerancia));
    }

    static Stream<Arguments> casos() {
        return Stream.of(
            Arguments.of(new int[] {}, 0, Collections.emptyList(), "array vazio"),
            Arguments.of(new int[] {5}, 0, List.of("0-0:5..5"), "leitura unica"),
            Arguments.of(new int[] {7, 7, 7}, 0, List.of("0-2:7..7"), "leituras estaveis tolerancia zero"),
            Arguments.of(new int[] {10, 11, 9, 10}, 2, List.of("0-3:9..11"), "todas dentro da tolerancia"),
            Arguments.of(new int[] {10, 20}, 2, List.of("0-0:10..10", "1-1:20..20"), "salto alem da tolerancia"),
            Arguments.of(new int[] {4, 4, 5, 4}, 0, List.of("0-1:4..4", "2-2:5..5", "3-3:4..4"), "tres faixas tolerancia zero"),
            Arguments.of(
                new int[] {1, 1, 10, 10, 10, 2},
                0,
                List.of("0-1:1..1", "2-4:10..10", "5-5:2..2"),
                "sequencia com 3+ faixas contiguas cobrindo todo o array"
            )
        );
    }

    @Test
    void compactarComToleranciaNegativaLancaExcecao() {
        assertThrows(IllegalArgumentException.class, () -> SensorCompactador.compactar(new int[] {1, 2, 3}, -1));
    }
}
