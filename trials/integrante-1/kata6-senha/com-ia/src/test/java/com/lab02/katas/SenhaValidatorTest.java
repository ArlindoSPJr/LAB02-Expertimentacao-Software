package com.lab02.katas;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SenhaValidatorTest {

    @ParameterizedTest(name = "[{index}] {2}")
    @MethodSource("casos")
    void classificarProduzResultadoEsperado(String senha, String esperado, String descricao) {
        assertEquals(esperado, SenhaValidator.classificar(senha));
    }

    static Stream<Arguments> casos() {
        return Stream.of(
            Arguments.of(null, "INVALIDA", "senha nula"),
            Arguments.of("", "INVALIDA", "senha vazia"),
            Arguments.of("Ab1", "INVALIDA", "senha curta (menos de 6 caracteres)"),
            Arguments.of("Abcdefghijklm", "INVALIDA", "senha longa (mais de 12 caracteres)"),
            Arguments.of("Abcdef1!", "INVALIDA", "caractere fora de letras/digitos"),
            Arguments.of("Abc123", "FORTE", "3 classes de caractere sem repeticao adjacente"),
            Arguments.of("Abc1123", "MEDIA", "3 classes com repeticao adjacente rebaixa para media"),
            Arguments.of("abcdef", "FRACA", "apenas uma classe de caractere (minusculas)")
        );
    }
}
