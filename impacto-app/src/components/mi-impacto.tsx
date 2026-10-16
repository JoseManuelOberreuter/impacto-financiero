import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';
import { StyleSheet, TextInput, View } from 'react-native';

import type { ReferenciasMiImpacto } from '@/api/tipos';
import { Capacidad } from '@/components/capacidad';
import { Seccion } from '@/components/seccion';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta, mesYAnio } from '@/utils/fechas';
import { pesos, porcentaje } from '@/utils/numeros';

// Los datos del usuario se guardan solo en este dispositivo: no van a la API.
const CLAVE = 'impacto:mi-impacto';
const SEMANAS_POR_MES = 52 / 12;

type Datos = { dividendoUf: string; litrosSemana: string };

/** "12,5" o "12.5" → 12.5; "1.250,5" → 1250.5; vacío o inválido → null. */
function numero(texto: string): number | null {
  const limpio = texto.includes(',') ? texto.replace(/\./g, '').replace(',', '.') : texto;
  const valor = Number(limpio);
  return texto.trim() && Number.isFinite(valor) && valor > 0 ? valor : null;
}

function conSignoPesos(valor: number): string {
  const signo = valor > 0 ? '+' : valor < 0 ? '−' : '';
  return `${signo}${pesos(Math.abs(valor))}`;
}

export function MiImpacto() {
  const { estado } = useApi<ReferenciasMiImpacto>('/mi-impacto/referencias');
  const [datos, setDatos] = useState<Datos>({ dividendoUf: '', litrosSemana: '' });

  useEffect(() => {
    AsyncStorage.getItem(CLAVE)
      .then((guardado) => {
        if (guardado) setDatos(JSON.parse(guardado));
      })
      .catch(() => {});
  }, []);

  const cambiar = (campo: keyof Datos) => (texto: string) => {
    const nuevos = { ...datos, [campo]: texto };
    setDatos(nuevos);
    AsyncStorage.setItem(CLAVE, JSON.stringify(nuevos)).catch(() => {});
  };

  return (
    <Seccion titulo="Mi impacto">
      <Vidrio style={styles.tarjeta}>
        <ThemedText type="small" themeColor="textSecondary">
          Cuánto te afecta la economía, en pesos. Tus datos se guardan solo en este dispositivo.
        </ThemedText>
        <Campo
          etiqueta="Tu dividendo o crédito, en UF"
          ejemplo="15,5"
          valor={datos.dividendoUf}
          onCambiar={cambiar('dividendoUf')}
        />
        {estado.tipo === 'listo' && numero(datos.dividendoUf) !== null && (
          <Dividendo uf={numero(datos.dividendoUf)!} referencias={estado.datos} />
        )}
      </Vidrio>

      <Capacidad id="mi_impacto" descripcion="Tu gasto en bencina, tu sueldo y tu AFP, en pesos.">
        <Vidrio style={styles.tarjeta}>
          <Campo
            etiqueta="Litros de bencina que cargas a la semana"
            ejemplo="30"
            valor={datos.litrosSemana}
            onCambiar={cambiar('litrosSemana')}
          />
          {estado.tipo === 'listo' && numero(datos.litrosSemana) !== null && (
            <Bencina litros={numero(datos.litrosSemana)!} referencias={estado.datos} />
          )}
        </Vidrio>
      </Capacidad>
    </Seccion>
  );
}

function Campo({
  etiqueta,
  ejemplo,
  valor,
  onCambiar,
}: {
  etiqueta: string;
  ejemplo: string;
  valor: string;
  onCambiar: (texto: string) => void;
}) {
  const theme = useTheme();

  return (
    <View style={styles.campo}>
      <ThemedText type="smallBold">{etiqueta}</ThemedText>
      <TextInput
        value={valor}
        onChangeText={onCambiar}
        placeholder={ejemplo}
        placeholderTextColor={theme.textSecondary}
        keyboardType="decimal-pad"
        inputMode="decimal"
        accessibilityLabel={etiqueta}
        style={[
          styles.entrada,
          { color: theme.text, backgroundColor: theme.backgroundSelected, borderColor: theme.border },
        ]}
      />
    </View>
  );
}

function Resultado({ titulo, valor, detalle }: { titulo: string; valor: string; detalle?: string }) {
  return (
    <View style={styles.resultado}>
      <ThemedText type="small" themeColor="textSecondary">
        {titulo}
      </ThemedText>
      <ThemedText style={styles.valor}>{valor}</ThemedText>
      {detalle && (
        <ThemedText type="small" themeColor="textSecondary">
          {detalle}
        </ThemedText>
      )}
    </View>
  );
}

function Dividendo({ uf, referencias }: { uf: number; referencias: ReferenciasMiImpacto }) {
  const r = referencias.uf;
  const hoy = uf * r.hoy.valor;
  const proximo = uf * r.ultima_publicada.valor;
  const haceUnAnio = uf * r.hace_un_anio.valor;

  return (
    <View style={styles.resultados}>
      <Resultado titulo="Hoy pagas" valor={pesos(hoy)} detalle={`UF del ${fechaCorta(r.hoy.fecha)}`} />
      <Resultado
        titulo={`Con la UF del ${fechaCorta(r.ultima_publicada.fecha)}`}
        valor={pesos(proximo)}
        detalle={`${conSignoPesos(proximo - hoy)} frente a hoy (la UF ya está publicada)`}
      />
      <Resultado
        titulo="Hace un año pagabas"
        valor={pesos(haceUnAnio)}
        detalle={`Hoy pagas ${pesos(Math.abs(hoy - haceUnAnio))} ${hoy >= haceUnAnio ? 'más' : 'menos'} al mes`}
      />
      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        Calculado con la UF del {r.fuente}. No incluye seguros ni comisiones.
      </ThemedText>
    </View>
  );
}

function Bencina({ litros, referencias }: { litros: number; referencias: ReferenciasMiImpacto }) {
  const b = referencias.bencina95;
  const litrosMes = litros * SEMANAS_POR_MES;
  const hoy = litrosMes * b.hoy.valor;
  const haceUnAnio = litrosMes * b.hace_un_anio.valor;
  const cambio = (b.hoy.valor / b.hace_un_anio.valor - 1) * 100;

  return (
    <View style={styles.resultados}>
      <Resultado
        titulo="Gastas al mes en bencina"
        valor={pesos(hoy)}
        detalle={`${Math.round(litrosMes)} litros de bencina 95 a ${pesos(b.hoy.valor)}`}
      />
      <Resultado
        titulo="Frente a hace un año"
        valor={`${conSignoPesos(hoy - haceUnAnio)} al mes`}
        detalle={`La bencina ${cambio >= 0 ? 'subió' : 'bajó'} ${porcentaje(Math.abs(cambio)).replace('+', '')} desde ${mesYAnio(b.hace_un_anio.fecha)}`}
      />
      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        Precio de hoy: mediana de {b.estaciones} estaciones de la {b.region} ({b.fuente}). Hace un
        año: promedio mensual de la {b.fuente}.
      </ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  campo: {
    gap: Spacing.two,
  },
  entrada: {
    borderWidth: StyleSheet.hairlineWidth,
    borderRadius: Spacing.three,
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two + Spacing.half,
    fontSize: 16,
  },
  resultados: {
    gap: Spacing.three,
  },
  resultado: {
    gap: Spacing.half,
  },
  valor: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: 600,
  },
  nota: {
    fontSize: 12,
    lineHeight: 18,
  },
});
