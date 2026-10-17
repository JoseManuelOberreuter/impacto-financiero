import { PaginaLegal } from '@/components/documento-legal';
import { PRIVACIDAD } from '@/constants/legal';

export default function PrivacidadScreen() {
  return <PaginaLegal documento={PRIVACIDAD} />;
}
