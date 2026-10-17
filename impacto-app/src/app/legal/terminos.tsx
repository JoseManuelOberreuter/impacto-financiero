import { PaginaLegal } from '@/components/documento-legal';
import { TERMINOS } from '@/constants/legal';

export default function TerminosScreen() {
  return <PaginaLegal documento={TERMINOS} />;
}
