"use client";
import { Box, Image, Heading } from "@chakra-ui/react";
import { use } from "react";
export default function ViewPatientSummary({
  params,
}: {
  params: Promise<{ patientId: string }>;
}) {
  const { patientId } = use(params);
  // return <>View Patient Summary {patientId}</>;

  return (
    <Box height={"100%"} display="flex" flexDirection="row" gap={4}>
      <Box
        width={"50%"}
        bg="whiteAlpha.500"
        padding={4}
        borderRadius="lg"
        boxShadow="sm"
      >
        <Heading>Patient Summary</Heading>
      </Box>
      <Box width={"50%"} pt={4}>
        <Heading>Patient Details</Heading>
      </Box>
    </Box>
  );
}
