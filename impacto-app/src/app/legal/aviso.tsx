import { PaginaLegal } from '@/components/documento-legal';
import { AVISO_LEGAL } from '@/constants/legal';

export default function AvisoLegalScreen() {
  return <PaginaLegal documento={AVISO_LEGAL} />;
}
