package com.lab02.katas;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class ChamadoResumo {

    private static final List<String> ORDEM_PRIORIDADES = List.of("ALTA", "MEDIA", "BAIXA");

    private ChamadoResumo() {
    }

    public static List<String> resumir(List<String> chamados) {
        Map<String, Integer> contagens = new LinkedHashMap<>();
        for (String prioridade : ORDEM_PRIORIDADES) {
            contagens.put(prioridade, 0);
        }

        for (String chamado : chamados) {
            if (chamado == null) {
                continue;
            }
            String[] partes = chamado.split(":", -1);
            if (partes.length != 2) {
                continue;
            }
            String codigo = partes[1];
            if (codigo.isEmpty()) {
                continue;
            }
            String prioridade = partes[0].toUpperCase();
            if (!contagens.containsKey(prioridade)) {
                continue;
            }
            contagens.put(prioridade, contagens.get(prioridade) + 1);
        }

        List<String> resultado = new ArrayList<>();
        for (String prioridade : ORDEM_PRIORIDADES) {
            int contagem = contagens.get(prioridade);
            if (contagem > 0) {
                resultado.add(prioridade + ":" + contagem);
            }
        }
        return resultado;
    }
}
