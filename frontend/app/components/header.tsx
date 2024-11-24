"use client";
import { Box, Image, Heading, Button, Select, Flex } from "@chakra-ui/react";
import { AddIcon, ViewIcon } from "@chakra-ui/icons";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState("doctor");

  useEffect(() => {
    // Set initial role based on URL
    if (pathname?.startsWith("/patient")) {
      setRole("patient");
    } else if (pathname?.startsWith("/doctor")) {
      setRole("doctor");
    }
  }, [pathname]);

  const handleRoleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newRole = e.target.value;
    setRole(newRole);
    
    if (newRole === "doctor") {
      router.push("/doctor/addPatient");
    } else {
      router.push("/patient/1");
    }
  };

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
        <Link href="/doctor/addPatient">
          <Button size="sm" leftIcon={<AddIcon />}>
            Add Patient
          </Button>
        </Link>
        <Link href="/doctor/viewPatientSummary/1">
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
      <Select width="150px" size="sm" value={role} onChange={handleRoleChange}>
        <option value="patient">👤 Patient</option>
        <option value="doctor">👨‍⚕️ Doctor</option>
      </Select>
    </Box>
  );
}
