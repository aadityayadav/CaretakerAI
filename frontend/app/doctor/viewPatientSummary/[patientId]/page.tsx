import { Box, Image, Heading } from "@chakra-ui/react";

export default function ViewPatientSummary({
  params,
}: {
  params: { patientId: string };
}) {
  return <>View Patient Summary {params.patientId}</>;
}
