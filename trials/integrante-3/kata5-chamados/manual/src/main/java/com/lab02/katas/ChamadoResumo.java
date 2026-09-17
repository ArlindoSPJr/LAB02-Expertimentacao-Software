package com.lab02.katas;

import java.util.ArrayList;
import java.util.List;

public final class ChamadoResumo {

    private ChamadoResumo() {
    }

    public static List<String> resumir(List<String> chamados) {

        int alta = 0;
        int media = 0;
        int baixa = 0;

        for (String chamado : chamados) {

            if (chamado == null) {
                continue;
            }

            int primeiro = chamado.indexOf(":");
            int ultimo = chamado.lastIndexOf(":");

            if (primeiro == -1 || primeiro != ultimo) {
                continue;
            }

            String prioridade = chamado.substring(0, primeiro).toUpperCase();
            String codigo = chamado.substring(primeiro + 1);

            if (codigo.isEmpty()) {
                continue;
            }

            if (prioridade.equals("ALTA")) {
                alta++;
            } else if (prioridade.equals("MEDIA")) {
                media++;
            } else if (prioridade.equals("BAIXA")) {
                baixa++;
            }
        }

        List<String> resultado = new ArrayList<>();

        if (alta > 0) {
            resultado.add("ALTA:" + alta);
        }

        if (media > 0) {
            resultado.add("MEDIA:" + media);
        }

        if (baixa > 0) {
            resultado.add("BAIXA:" + baixa);
        }

        return resultado;
    }
}
