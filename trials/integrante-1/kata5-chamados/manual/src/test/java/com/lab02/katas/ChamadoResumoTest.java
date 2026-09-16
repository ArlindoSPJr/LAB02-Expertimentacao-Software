package com.lab02.katas;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ChamadoResumoTest {

    @ParameterizedTest(name = "[{index}] {2}")
    @MethodSource("casos")
    void resumirProduzResultadoEsperado(List<String> chamados, List<String> esperado, String descricao) {
        assertEquals(esperado, ChamadoResumo.resumir(chamados));
    }

    static Stream<Arguments> casos() {
        return Stream.of(
            Arguments.of(Collections.emptyList(), Collections.emptyList(), "lista vazia"),
            Arguments.of(List.of("ALTA:A1"), List.of("ALTA:1"), "um chamado valido"),
            Arguments.of(
                Arrays.asList("ALTA:A1", "MEDIA:B1", "ALTA:A2"),
                List.of("ALTA:2", "MEDIA:1"),
                "mistura de prioridades, baixa ausente por contagem zero"
            ),
            Arguments.of(
                Arrays.asList("alta:A1", "ALTA:A2", "Alta:A3"),
                List.of("ALTA:3"),
                "prioridade case-insensitive agregada"
            ),
            Arguments.of(
                Arrays.asList("URGENTE:X1", "ALTA:A1"),
                List.of("ALTA:1"),
                "prioridade desconhecida descartada"
            ),
            Arguments.of(
                Arrays.asList("ALTAA1", "ALTA:A1:X", "ALTA:A2"),
                List.of("ALTA:1"),
                "formato malformado (sem ou com mais de um separador) descartado"
            ),
            Arguments.of(
                Arrays.asList("ALTA:", "MEDIA:B1"),
                List.of("MEDIA:1"),
                "codigo vazio descartado"
            ),
            Arguments.of(
                Arrays.asList(null, "", "ALTA:A1", "urgente:X", "MEDIA:B1:X", "media:B2", "BAIXA:C1", "BAIXA:"),
                List.of("ALTA:1", "MEDIA:1", "BAIXA:1"),
                "mistura completa: validos, invalidos, null e duplicata de regras de descarte"
            )
        );
    }
}
