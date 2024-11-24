"use client";
import {  use } from "react";
import { Box, Button, Text, Heading, Image, Flex } from "@chakra-ui/react";

import Ai from "@/app/components/ai";

export default function PatientPage({
  params,
}: {
  params: Promise<{ patientId: string }>;
}) {
  const { patientId } = use(params);
  return (
    <Ai params={{ userId: patientId, isDoctor: false }} />
  );
}
