import {
  ArrowUturnLeftIcon,
  TrashIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
export const Icon = ({ name }) => {
  if (name === "Reiniciar") {
    return <ArrowUturnLeftIcon className="h-4 w-4" />;
  }
  if (name === "Limpiar chat") {
    return <TrashIcon className="h-4 w-4" />;
  }
  if (name === "Cerrar") {
    return <XMarkIcon className="h-4 w-4" />;
  }
};