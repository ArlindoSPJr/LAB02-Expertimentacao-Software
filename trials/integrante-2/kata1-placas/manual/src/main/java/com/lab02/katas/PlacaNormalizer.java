package com.lab02.katas;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.regex.Pattern;

public final class PlacaNormalizer {

    private static final Pattern ANTIGO = Pattern.compile("^[A-Z]{3}[0-9]{4}$");
    private static final Pattern MERCOSUL = Pattern.compile("^[A-Z]{3}[0-9][A-Z][0-9]{2}$");

    private PlacaNormalizer() {
    }

    public static List<String> normalizar(List<String> brutas) {
        LinkedHashSet<String> canonicas = new LinkedHashSet<>();
        for (String bruta : brutas) {
            if (bruta == null || bruta.isEmpty()) {
                continue;
            }
            String limpa = bruta.replace(" ", "").replace("-", "").replace(".", "").toUpperCase();
            if (ANTIGO.matcher(limpa).matches() || MERCOSUL.matcher(limpa).matches()) {
                canonicas.add(limpa);
            }
        }
        return new ArrayList<>(canonicas);
    }
}