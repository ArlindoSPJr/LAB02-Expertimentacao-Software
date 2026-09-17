package com.lab02.katas;

public final class SenhaValidator {

    private static final int TAMANHO_MINIMO = 6;
    private static final int TAMANHO_MAXIMO = 12;

    private SenhaValidator() {
    }

    public static String classificar(String senha) {

        if (!ehValida(senha)) {
            return "INVALIDA";
        }

        int classes = contarClasses(senha);
        boolean temRepeticaoAdjacente = possuiRepeticaoAdjacente(senha);

        int score = Math.max(1, classes - (temRepeticaoAdjacente ? 1 : 0));

        return mapearScore(score);
    }

    private static boolean ehValida(String senha) {

        if (senha == null) {
            return false;
        }

        int tamanho = senha.length();

        if (tamanho < TAMANHO_MINIMO || tamanho > TAMANHO_MAXIMO) {
            return false;
        }

        for (int i = 0; i < tamanho; i++) {
            if (!Character.isLetterOrDigit(senha.charAt(i))) {
                return false;
            }
        }

        return true;
    }

    private static int contarClasses(String senha) {

        boolean temMinuscula = false;
        boolean temMaiuscula = false;
        boolean temDigito = false;

        for (int i = 0; i < senha.length(); i++) {
            char c = senha.charAt(i);

            if (Character.isLowerCase(c)) {
                temMinuscula = true;
            } else if (Character.isUpperCase(c)) {
                temMaiuscula = true;
            } else if (Character.isDigit(c)) {
                temDigito = true;
            }
        }

        int classes = 0;
        if (temMinuscula) classes++;
        if (temMaiuscula) classes++;
        if (temDigito) classes++;

        return classes;
    }

    private static boolean possuiRepeticaoAdjacente(String senha) {

        for (int i = 1; i < senha.length(); i++) {
            if (senha.charAt(i) == senha.charAt(i - 1)) {
                return true;
            }
        }

        return false;
    }

    private static String mapearScore(int score) {

        switch (score) {
            case 3:
                return "FORTE";
            case 2:
                return "MEDIA";
            default:
                return "FRACA";
        }
    }
}