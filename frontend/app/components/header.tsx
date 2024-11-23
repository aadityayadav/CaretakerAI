import { Box, Image, Heading, Button, Select, Flex } from "@chakra-ui/react";
import { AddIcon, ViewIcon } from "@chakra-ui/icons";
import { FaUserInjured, FaUserMd } from "react-icons/fa";

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
    >
      {/* Left side buttons */}
      <Flex gap={2}>
        <Button size="sm" leftIcon={<AddIcon />}>
          Add Patient
        </Button>
        <Button size="sm" leftIcon={<ViewIcon />}>
          View Patient Summary
        </Button>
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
