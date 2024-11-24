import { Box, Image, Heading, Button, Select, Flex } from "@chakra-ui/react";
import { AddIcon, ViewIcon } from "@chakra-ui/icons";
import Link from "next/link";

export default function Header() {
  return (
    <Box
      width="100%"
      display="flex"
      justifyContent="space-between"
      alignItems="center"
      background="rgba(255, 255, 255, 0.8)"
      padding={4}
      borderRadius="10px"
      backdropFilter="blur(10px)"
      boxShadow="0 4px 6px rgba(0, 0, 0, 0.1)"
    >
      {/* Left side buttons */}
      <Flex gap={2}>
        <Link href="/add-patient">
          <Button size="sm" leftIcon={<AddIcon />}>
            Add Patient
          </Button>
        </Link>
        <Link href="/patient-summary">
          <Button size="sm" leftIcon={<ViewIcon />}>
            View Patient Summary
          </Button>
        </Link>
      </Flex>

      {/* Center logo and title */}
      <Flex gap={2} position="absolute" left="50%" transform="translateX(-50%)">
        <Image src="/logo3.png" alt="CaretakerAI" width={35} />
        <Heading fontSize={"3xl"} fontWeight={"medium"}>
          CaretakerAI
        </Heading>
      </Flex>

      {/* Right side select */}
      <Select width="150px" size="sm">
        <option value="patient">👤 Patient</option>
        <option value="doctor">👨‍⚕️ Doctor</option>
      </Select>
    </Box>
  );
}
