// Íconos de Lucide (https://lucide.dev): línea fina, color y tamaño configurables.
import {
  ChartLine,
  CircleDollarSign,
  Factory,
  Landmark,
  PiggyBank,
  ShoppingCart,
  Users,
  Wallet,
  type LucideIcon,
  type LucideProps,
} from 'lucide-react-native';

const ICONOS: Record<string, LucideIcon> = {
  impacto: Wallet,
  bolsillo: ShoppingCart,
  deudas: Landmark,
  ahorro: PiggyBank,
  actividad: Factory,
  dolar: CircleDollarSign,
  animo: Users,
};

export function IconoTermometro({ id, ...props }: LucideProps & { id: string }) {
  const Icono = ICONOS[id] ?? ChartLine;
  return <Icono {...props} />;
}
