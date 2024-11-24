"use client";
import { Box, Image, Heading } from "@chakra-ui/react";
import { use } from "react";
import Ai from "@/app/components/ai";
import { Text, Divider } from "@chakra-ui/react";
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
        <Heading>Patient Summary: {patientId}</Heading>
        <Divider
          my={2}

          borderColor="blackAlpha.500"
        />

        <Text>
          This is a summary of the patient's medical history and current
          condition. Bla bla bla bla bla bla bla bla bla bla bla bla bla bla
          Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolore numquam
          libero mollitia dicta sit quidem veritatis animi quo, itaque,
          accusantium repellendus ea laborum beatae amet expedita nihil, autem
          veniam aperiam!
        </Text>
      </Box>
      <Box width={"50%"} pt={4}>
        <Ai params={Promise.resolve({ userId: patientId })} isDoctor={true} />
      </Box>
    </Box>
  );
}
