package com.lab02.katas;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PlacaNormalizerTest {

    @ParameterizedTest(name = "[{index}] {2}")
    @MethodSource("casos")
    void normalizarProduzResultadoEsperado(List<String> brutas, List<String> esperado, String descricao) {
        assertEquals(esperado, PlacaNormalizer.normalizar(brutas));
    }

    static Stream<Arguments> casos() {
        return Stream.of(
            Arguments.of(Collections.emptyList(), Collections.emptyList(), "lista vazia"),
            Arguments.of(List.of("ABC1234"), List.of("ABC1234"), "placa ja canonica formato antigo"),
            Arguments.of(List.of("abc 1234"), List.of("ABC1234"), "espacos e minusculas"),
            Arguments.of(List.of("ABC-1234"), List.of("ABC1234"), "placa com hifen"),
            Arguments.of(List.of("abc1d23"), List.of("ABC1D23"), "placa mercosul minuscula"),
            Arguments.of(Arrays.asList("ABC1234", "abc-1234"), List.of("ABC1234"), "mesma placa em dois formatos brutos"),
            Arguments.of(List.of("ABC123"), Collections.emptyList(), "placa invalida descartada"),
            Arguments.of(
                Arrays.asList("ABC1234", null, "", "xyz9999", "abc-1234"),
                List.of("ABC1234", "XYZ9999"),
                "mistura de validas invalidas null e duplicata"
            )
        );
    }
}
